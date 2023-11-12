from skopt import BayesSearchCV
from skopt.space import Real, Categorical, Integer
from your_file import DQNagent
# TODO
search_spaces = {
    'state_size': Integer(1, 10),
    'batch_size': Integer(1, 32),
    'gamma': Real(0.8, 1.0),
    'epsilon_decay': Real(0.9, 1.0),
    'learning_rate': Real(0.0001, 0.01)
}

optimizer = BayesSearchCV(
    estimator=DQNagent(),
    search_spaces=search_spaces,
    n_iter=50,
    cv=3,
    n_jobs=-1,
    verbose=1
)


optimizer.fit(X, y)


best_params = optimizer.best_params_


print(best_params)