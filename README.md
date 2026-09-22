# MLOps Food-11 Project

This repository follows the same Food-11 project across several MLOps labs:

- Lab 1: Git, DVC, and dataset preparation
- Lab 2: model training and experiment tracking with MLflow
- Lab 3: model registration, FastAPI serving, and Docker

## Lab answers

- [Lab 1 answers](lab%20answers/lab1.md)
- [Lab 2 answers](lab%20answers/lab2.md)
- [Lab 3 answers](lab%20answers/lab3.md)

## Main files

- `src/food11/data.py`: prepares the full and mini Food-11 datasets
- `src/food11/train.py`: trains ResNet-18 and logs runs to MLflow
- `src/food11/serve.py`: serves the registered champion model with FastAPI
- `Dockerfile`: builds the model API image
