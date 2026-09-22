# Lab 2 Answers

## Question 1

`pyproject.toml` gained the new direct dependencies: MLflow, PyTorch, torchvision, and scikit-learn. `uv.lock` recorded the exact versions of these packages and their dependencies so the environment can be reproduced with `uv sync`.

## Question 2

`--backend-store-uri sqlite:///mlflow.db` stores the run metadata, such as experiments, parameters, metrics, run IDs, and timestamps. `--default-artifact-root ./mlruns` stores the actual output files, such as trained models and environment files. In short, the database stores information about the runs, while `mlruns/` stores their files.

## Question 3

`mlflow.db` and `mlruns/` are local files generated while running experiments. They change often and can become large, so they do not belong in Git. They also should not be tracked by DVC because MLflow already manages this run history and its artifacts.

## Question 4

The first call to `mlflow.set_experiment("food11")` created the experiment because it did not exist yet, then made it the active experiment. It appeared in the UI immediately, but it had no runs until training started.

## Question 5

A parameter is fixed before the run, like the learning rate or batch size. A metric is measured during or after training, like loss or accuracy. Metrics use `step` because they change at every epoch and MLflow uses those steps to draw charts. A parameter stays fixed, so it does not need a step.

## Question 6

The run page showed my parameters, metric charts, and logged model. On disk, MLflow stored the model under a path like:

`mlruns/1/models/<model-id>/artifacts/data/model.pth`

The same artifact folder also contained the `MLmodel` file and the environment requirements.

## Question 7

The best learning rate was `0.0001`, with a final validation accuracy of about `0.7573`. A higher learning rate was not better here: `0.01` performed much worse, so increasing the learning rate can make training unstable or skip over a good solution.

## Question 8

The parallel-coordinates plot showed that learning rate had the clearest effect. `0.01` was the worst, `0.001` was in the middle, and `0.0001` was the best. With `lr=0.001`, batch size 64 did a little better than 32, but I only ran each setup once, so I would not treat that as a final conclusion.

## Question 9

The best run was `able-hound-923`:

- Run ID: `e54c825900d0439592e9ff1ee19945ac`
- Learning rate: `0.0001`
- Batch size: `32`
- Final validation accuracy: `0.7573`
