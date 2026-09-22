# Lab 3 Answers

## Question 1

The first registered model was given Version 1. A logged model belongs to one training run and stays connected to that run's parameters and metrics. Registering it gives the model a stable name, `food11`, and lets me manage different versions separately. I later created Version 2 from the same model so its artifacts could be reached from Docker.

## Question 2

Aliases such as `champion` and `challenger` replace the old fixed stages like Staging and Production. Keeping model versions separate from runs makes deployment easier while still preserving the run history. An alias is flexible because I can move `champion` to another version without changing the API code.

## Question 3

Using `models:/food11@champion` means the API does not depend on a specific `.pth` path or version number. MLflow finds the model through the registry. To serve a newer model, I only need to register it, move the `champion` alias to that version, and restart the API so it loads the new model.

## Question 4

The dependency files are copied before the source code so Docker can cache the slow `uv sync` layer. If I only change `serve.py`, Docker reuses the installed dependencies and rebuilds only the small source-code layer.

## Question 5

The multi-stage image was about `10.51 GiB`, while the naive single-stage image was about `10.64 GiB`. The multi-stage build saved around `131 MiB`. The biggest layer was the virtual environment at about `7.25 GB`, mostly because this project uses CUDA-enabled PyTorch.

## Question 6

Without `.dockerignore`, Docker would send large local folders such as `data/`, `mlruns/`, `.git/`, and `.venv/` into the build context. That would slow down builds, waste disk space, and cause unnecessary cache invalidation. A Windows `.venv/` could also cause problems if it were copied into the Linux image because it contains platform-specific files.

## Question 7

Inside the container, `127.0.0.1` means the container itself, not my Windows machine. `host.docker.internal` resolves to the host machine, so the container can use it to reach MLflow running on Windows.

## Question 8

Yes, a new container loaded the model without rebuilding the image. The API code and Python dependencies are inside the image, but the `champion` model is downloaded from MLflow when the container starts. This also means MLflow must be reachable at startup.

## Question 9

The Dockerfile is in Git, but the image is still only stored locally. To let another machine run the exact image, it needs to be tagged and pushed to a container registry such as Docker Hub or GitHub Container Registry. A fixed version tag or digest would be safer than relying only on `latest`.
