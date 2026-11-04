"""Compare a candidate's accuracy with champion before changing the alias."""

import argparse
import math
import os
from pathlib import Path

from mlflow import MlflowClient


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, type=int)
    parser.add_argument("--test-dir", type=Path, default=Path("data/food11_processed_mini/evaluation"))
    args = parser.parse_args()
    n = sum(1 for path in args.test_dir.glob("*/*") if path.suffix.lower() in {".jpg", ".jpeg", ".png"})
    if n == 0:
        parser.error(f"No test images found in {args.test_dir}")

    client = MlflowClient(os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000"))
    candidate = client.get_model_version("food11", str(args.version))
    champion = client.get_model_version_by_alias("food11", "champion")
    if candidate.version == champion.version:
        parser.error("Candidate is already champion; choose a different version")

    def accuracy(version):
        if not version.run_id:
            raise ValueError(f"Version {version.version} has no source run")
        metrics = client.get_run(version.run_id).data.metrics
        if "test_accuracy" not in metrics:
            raise ValueError(f"Run {version.run_id} has no test_accuracy metric")
        value = metrics["test_accuracy"]
        if not math.isfinite(value) or not 0 <= value <= 1:
            raise ValueError("test_accuracy must be between 0 and 1")
        return value

    acc_candidate = accuracy(candidate)
    acc_champion = accuracy(champion)
    se = math.sqrt(acc_champion * (1 - acc_champion) / n)
    decision = "champion" if acc_candidate >= acc_champion + 2 * se else "challenger"
    tags = {
        "gate.decision": decision,
        "gate.candidate_accuracy": acc_candidate,
        "gate.champion_accuracy": acc_champion,
        "gate.champion_version": champion.version,
        "gate.test_size": n,
        "gate.two_se": 2 * se,
    }
    for key, value in tags.items():
        client.set_model_version_tag("food11", candidate.version, key, str(value))
    client.set_registered_model_alias("food11", decision, candidate.version)
    print(
        f"candidate={acc_candidate:.4f}, champion={acc_champion:.4f}, n={n}, "
        f"2*se={2 * se:.4f} ({200 * se:.2f} percentage points), decision={decision}"
    )


if __name__ == "__main__":
    main()
