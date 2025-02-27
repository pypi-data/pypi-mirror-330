# boyd-ml-utils
## Overview
I just want to try publishing a package in PyPI. I'll add unit tests, more functionalities and GitHub pages in the future.

## Sample OptunaSearchCV parameter distribution
```
{
    "name": "LGBMRegressor", 
    "params": {
        "num_leaves": IntDistribution(low=7, high=47, step=8), 
        "min_child_samples": IntDistribution(low=1, high=10, step=1), 
        "colsample_bytree": FloatDistribution(low=0.5, high=1.0, step=0.1), 
        "subsample": FloatDistribution(low=0.7, high=1.0, step=0.1), 
        "learning_rate": FloatDistribution(low=0.03, high=0.2, step=0.01), 
        "n_estimators": IntDistribution(low=50, high=300, step=10), 
        "verbosity": -1, 
        "n_jobs": 1, 
        "extra_tree": True, 
        "objective": "mean_squared_error"
    }
}
```