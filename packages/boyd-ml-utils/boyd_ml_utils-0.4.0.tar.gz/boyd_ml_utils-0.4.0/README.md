# boyd-ml-utils
## Overview
I just want to try publishing a package in PyPI. I'll add unit tests, more functionalities and GitHub pages in the future.

## Sample usage
`OptunaSearchCV` works like `RandomizedSearchCV` in `scikit-learn` but the parameter distributions must be specified using distribution classes in `optuna`.
```
import pandas as pd
from boyd_ml_utils.model_selection import OptunaSearchCV
from optuna.distributions import IntDistribution
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# Load the iris dataset
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = X.pop("petal width (cm)")  # Treat petal width as the target variable

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Define a Random Forest Regressor model
rf = RandomForestRegressor(random_state=42)

# Define hyperparameter space for RandomizedSearchCV
param_dist = {
    "n_estimators": IntDistribution(low=10, high=200),
    "max_depth": IntDistribution(low=3, high=20),
    "min_samples_split": IntDistribution(low=2, high=10),
    "min_samples_leaf": IntDistribution(low=1, high=5),
}

# Perform Randomized Search
random_search = OptunaSearchCV(
    estimator=rf,
    param_distributions=param_dist,
    n_iter=100,
    scoring="neg_mean_squared_error",
    cv=5,
    n_jobs=5,
)

random_search.fit(X_train, y_train)

# Best parameters and model evaluation
best_model = random_search.best_estimator_
y_pred = best_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

print("Best Parameters:", random_search.best_params_)
print("Mean Squared Error on Test Data:", mse)
```