# MLOps Food-11 Project

This repository follows the same Food-11 project across several MLOps labs:

- Lab 1: Git, DVC, and dataset preparation
- Lab 2: model training and experiment tracking with MLflow
- Lab 3: model registration, FastAPI serving, and Docker
- Lab 4: MLflow, inference, and a web frontend with Docker Compose
- Lab 5: data validation, automated tests, CI/CD, and model promotion

## Lab answers

- [Lab 1 answers](lab%20answers/lab1.md)
- [Lab 2 answers](lab%20answers/lab2.md)
- [Lab 3 answers](lab%20answers/lab3.md)
- [Lab 4 answers](lab%20answers/lab4.md)
- [Lab 5 answers](lab%20answers/lab5.md)

## Main files

- `src/food11/data.py`: prepares the full and mini Food-11 datasets
- `src/food11/train.py`: trains ResNet-18 and logs runs to MLflow
- `src/food11/serve.py`: serves the registered champion model with FastAPI
- `src/food11/validate_data.py`: checks the processed dataset before training
- `src/food11/promote.py`: promotes a candidate model only when it passes the accuracy gate
- `.github/workflows/ci.yml`: runs tests, checks the API, and publishes the Docker image
- `Dockerfile`: builds the model API image
