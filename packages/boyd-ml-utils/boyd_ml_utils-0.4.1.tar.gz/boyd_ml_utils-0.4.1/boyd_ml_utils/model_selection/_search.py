from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Tuple, Union

import numpy as np
import optuna
from lightgbm import LGBMRegressor
from optuna.distributions import BaseDistribution
from optuna.samplers import TPESampler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection._search import BaseSearchCV
from sklearn.model_selection._split import BaseShuffleSplit
from sklearn.utils.discovery import all_estimators
from xgboost import XGBRegressor

estimators_dictionary = {
    **dict(all_estimators()),
    "LGBMRegressor": LGBMRegressor,
    "XGBRegressor": XGBRegressor,
}


def estimators_map(x: str) -> Union[BaseEstimator, TransformerMixin]:
    """
    Maps a given string to the corresponding estimator class.

    Parameters
    ----------
    x : str
        Name of the estimator.

    Returns
    -------
    Union[BaseEstimator, TransformerMixin]
        Instantiated estimator or transformer.
    """
    return estimators_dictionary[x]()


def votreg_map(*wts: float) -> np.ndarray:
    """
    Computes weight mapping for a voting regressor using negative log weights.

    Parameters
    ----------
    *wts : float
        Individual weights.

    Returns
    -------
    np.ndarray
        Normalized weight array.
    """
    votreg_wts = np.array([-np.log(wt) for wt in wts])
    votreg_wts = votreg_wts / votreg_wts.sum()
    return votreg_wts


@dataclass
class CustomOptunaDistribution:
    """
    Custom wrapper for Optuna parameter distributions.

    Attributes
    ----------
    base_params : List[Tuple[str, BaseDistribution]]
        List of parameter names and their respective distributions.
    param_mapping : Callable
        Function to map suggested parameters to final values.
    """

    base_params: List[Tuple[str, BaseDistribution]]
    param_mapping: Callable

    def suggest(self, trial: optuna.Trial) -> Any:
        """
        Suggests parameters using Optuna's trial mechanism.

        Parameters
        ----------
        trial : optuna.Trial
            Optuna trial instance.

        Returns
        -------
        Any
            Mapped parameter values.
        """
        suggested_vals = [trial._suggest(name, dist) for name, dist in self.base_params]
        return self.param_mapping(*suggested_vals)


@dataclass
class _Objective:
    """
    Objective function for Optuna optimization.

    Attributes
    ----------
    param_distributions : Dict[str, Union[BaseDistribution, CustomOptunaDistribution]]
        Dictionary of parameter distributions.
    evaluate_candidates : Callable
        Function to evaluate candidates.
    refit_metric : str
        Metric used for optimization.
    """

    param_distributions: Dict[str, Union[BaseDistribution, CustomOptunaDistribution]]
    evaluate_candidates: Callable
    refit_metric: str

    def __call__(self, trial):
        # getting parameter suggestions from built-in optuna distributions
        suggested_params = {
            name: trial._suggest(name, dist)
            for name, dist in self.param_distributions.items()
            if not isinstance(dist, CustomOptunaDistribution)
        }

        # getting parameter suggestions from CustomOptunaDistribution instances
        suggested_params.update(
            {
                name: dist.suggest(trial)
                for name, dist in self.param_distributions.items()
                if isinstance(dist, CustomOptunaDistribution)
            }
        )

        result = self.evaluate_candidates([suggested_params])
        return result[f"mean_test_{self.refit_metric}"][-1]


class OptunaSearchCV(BaseSearchCV):
    """
    Custom implementation of hyperparameter tuning using Optuna.

    Parameters
    ----------
    estimator : BaseEstimator
        The base estimator to be optimized.
    param_distributions : Dict[str, Union[BaseDistribution, CustomOptunaDistribution]]
        Dictionary of parameter distributions.
    n_iter : int, optional
        Number of iterations for optimization, by default 10.
    scoring : Union[str, Callable, List, Tuple, Dict, None], optional
        Scoring metric, by default None.
    n_jobs : int, optional
        Number of parallel jobs, by default None.
    refit : Union[bool, str, Callable, None], optional
        Refit strategy, by default True.
    cv : Union[BaseShuffleSplit, None], optional
        Cross-validation strategy, by default None.
    verbose : int, optional
        Verbosity level, by default 0.
    pre_dispatch : str, optional
        Number of jobs dispatched during parallel execution, by default "2*n_jobs".
    optuna_random_state : Union[int, None], optional
        Random seed for Optuna, by default None.
    error_score : float, optional
        Error score for failed fits, by default np.nan.
    return_train_score : bool, optional
        Whether to include training scores, by default False.
    optuna_study_kwargs : Dict[str, Any], optional
        Additional keyword arguments for Optuna study creation, by default {}.
    """

    # TODO: add inputs validation
    def __init__(
        self,
        estimator: BaseEstimator,
        param_distributions: Dict[
            str, Union[BaseDistribution, CustomOptunaDistribution]
        ],
        n_iter: int = 10,
        scoring: Union[str, Callable, List, Tuple, Dict, None] = None,
        n_jobs: int = None,
        refit: Union[bool, str, Callable, None] = True,
        cv: Union[BaseShuffleSplit, None] = None,
        verbose: int = 0,
        pre_dispatch: str = "2*n_jobs",
        optuna_random_state: Union[int, None] = None,
        error_score: float = np.nan,
        return_train_score: bool = False,
        optuna_study_kwargs: Dict[str, Any] = {},
    ):
        self.param_distributions = param_distributions
        self.n_iter = n_iter
        self.optuna_random_state = optuna_random_state
        self.optuna_study_kwargs = optuna_study_kwargs
        super().__init__(
            estimator=estimator,
            scoring=scoring,
            n_jobs=n_jobs,
            refit=refit,
            cv=cv,
            verbose=verbose,
            pre_dispatch=pre_dispatch,
            error_score=error_score,
            return_train_score=return_train_score,
        )

    def _check_dist_type(self):
        for dist in self.param_distributions.values():
            if not isinstance(dist, (BaseDistribution, CustomOptunaDistribution)):
                raise TypeError(
                    f"type of dist: {dist} not in (BaseDistribution, CustomOptunaDistribution)"
                )

    def _run_search(self, evaluate_candidates):
        optuna.logging.disable_default_handler()
        if (
            isinstance(self.refit, bool)
            or isinstance(self.scoring, str)
            or (self.scoring is None)
        ):
            refit_metric = "score"
        else:
            refit_metric = self.refit

        sampler = TPESampler(seed=self.optuna_random_state)
        study = optuna.create_study(
            direction="maximize", sampler=sampler, **self.optuna_study_kwargs
        )
        objective = _Objective(
            self.param_distributions, evaluate_candidates, refit_metric
        )
        study.optimize(objective, n_trials=self.n_iter)
        self.study_ = study
