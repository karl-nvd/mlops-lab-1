"""Serve the champion Food-11 model through a FastAPI application."""

from __future__ import annotations

import io
import os
from contextlib import asynccontextmanager

import mlflow
import numpy as np
import torch
from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from torchvision.models import ResNet18_Weights


MODEL_URI = "models:/food11@champion"
TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")

# ImageFolder sorts these directory names alphabetically, producing this order.
CATEGORIES = (
    "Bread",
    "Dairy product",
    "Dessert",
    "Egg",
    "Fried food",
    "Meat",
    "Noodles-Pasta",
    "Rice",
    "Seafood",
    "Soup",
    "Vegetable-Fruit",
)

TRANSFORM = ResNet18_Weights.DEFAULT.transforms()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the registered model once when the API starts."""
    mlflow.set_tracking_uri(TRACKING_URI)

    # This project created and controls the trusted pickle-based Lab 2 model.
    # MLflow requires an explicit opt-in before loading that serialization format.
    os.environ.setdefault("MLFLOW_ALLOW_PICKLE_DESERIALIZATION", "true")
    app.state.model = mlflow.pyfunc.load_model(MODEL_URI)
    yield


app = FastAPI(title="Food-11 Model API", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    """Report whether the API process is running."""
    return {"status": "ok"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> dict[str, str | float]:
    """Predict a Food-11 category from an uploaded image."""
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except (UnidentifiedImageError, OSError) as exc:
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid image.") from exc

    batch = TRANSFORM(image).unsqueeze(0).numpy()
    logits = np.asarray(app.state.model.predict(batch))
    probabilities = torch.softmax(torch.from_numpy(logits), dim=1)[0]
    confidence, class_index = torch.max(probabilities, dim=0)

    return {
        "category": CATEGORIES[class_index.item()],
        "confidence": confidence.item(),
    }
