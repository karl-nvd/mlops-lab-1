"""Train a Food-11 classifier and track each run with MLflow."""

from __future__ import annotations

import argparse
from pathlib import Path

import mlflow
import mlflow.pytorch
import torch
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision import datasets, models


TRACKING_URI = "http://127.0.0.1:5000"
EXPERIMENT_NAME = "food11"
DATA_ROOT = Path("data")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a ResNet-18 model on Food-11.")
    parser.add_argument(
        "--dataset",
        choices=("mini", "processed"),
        default="mini",
        help="Use the small development dataset or the full processed dataset.",
    )
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--batch-size", type=int, default=32)
    return parser.parse_args()


def evaluate(model: nn.Module, loader: DataLoader, criterion: nn.Module, device: torch.device) -> tuple[float, float]:
    """Return average loss and accuracy for one validation or evaluation split."""
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            total_loss += criterion(outputs, labels).item() * labels.size(0)
            correct += (outputs.argmax(dim=1) == labels).sum().item()
            total += labels.size(0)

    return total_loss / total, correct / total


def main() -> None:
    args = parse_args()
    dataset_name = "food11_processed_mini" if args.dataset == "mini" else "food11_processed"
    dataset_path = DATA_ROOT / dataset_name

    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset directory not found: {dataset_path}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    weights = models.ResNet18_Weights.DEFAULT
    transform = weights.transforms()

    train_dataset = datasets.ImageFolder(dataset_path / "training", transform=transform)
    validation_dataset = datasets.ImageFolder(dataset_path / "validation", transform=transform)
    evaluation_dataset = datasets.ImageFolder(dataset_path / "evaluation", transform=transform)

    if train_dataset.classes != validation_dataset.classes or train_dataset.classes != evaluation_dataset.classes:
        raise ValueError("Class folders must match across training, validation, and evaluation splits.")

    loader_options = {
        "batch_size": args.batch_size,
        "num_workers": 0,
        "pin_memory": device.type == "cuda",
    }
    train_loader = DataLoader(train_dataset, shuffle=True, **loader_options)
    validation_loader = DataLoader(validation_dataset, shuffle=False, **loader_options)
    evaluation_loader = DataLoader(evaluation_dataset, shuffle=False, **loader_options)

    model = models.resnet18(weights=weights)
    model.fc = nn.Linear(model.fc.in_features, len(train_dataset.classes))
    model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)

    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    with mlflow.start_run():
        mlflow.log_params(
            {
                "dataset": args.dataset,
                "epochs": args.epochs,
                "lr": args.lr,
                "batch_size": args.batch_size,
                "model": "resnet18",
                "pretrained": True,
                "device": str(device),
            }
        )

        for epoch in range(1, args.epochs + 1):
            model.train()
            running_loss = 0.0
            seen_images = 0

            for images, labels in train_loader:
                images, labels = images.to(device), labels.to(device)
                optimizer.zero_grad()
                outputs = model(images)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                running_loss += loss.item() * labels.size(0)
                seen_images += labels.size(0)

            train_loss = running_loss / seen_images
            val_loss, val_accuracy = evaluate(model, validation_loader, criterion, device)
            mlflow.log_metric("train_loss", train_loss, step=epoch)
            mlflow.log_metric("val_loss", val_loss, step=epoch)
            mlflow.log_metric("val_accuracy", val_accuracy, step=epoch)
            print(
                f"Epoch {epoch}/{args.epochs} | "
                f"train_loss={train_loss:.4f} | val_loss={val_loss:.4f} | val_accuracy={val_accuracy:.4f}"
            )

        _, test_accuracy = evaluate(model, evaluation_loader, criterion, device)
        mlflow.log_metric("test_accuracy", test_accuracy)
        # Save a portable CPU model. MLflow 3.16 defaults to the traced ``pt2``
        # format, which requires a TensorSpec signature; pickle avoids that
        # extra tracing requirement for this small lab model.
        model.to("cpu")
        mlflow.pytorch.log_model(
            model,
            "model",
            serialization_format=mlflow.pytorch.SERIALIZATION_FORMAT_PICKLE,
        )
        print(f"Final test accuracy: {test_accuracy:.4f}")


if __name__ == "__main__":
    main()
