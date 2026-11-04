"""Check the processed Food-11 dataset contract without modifying files."""

import argparse
import hashlib
import sys
from pathlib import Path

from PIL import Image

try:
    from .data import CLASSES, SPLITS
except ImportError:
    from data import CLASSES, SPLITS


def validate_dataset(root: Path, min_per_class: int = 50, tau: float = 0.05) -> bool:
    issues = {name: [] for name in ("folders", "images", "counts", "duplicates", "balance")}
    counts = {split: dict.fromkeys(CLASSES, 0) for split in SPLITS}
    seen = {}

    for split in SPLITS:
        split_dir = root / split
        if not split_dir.is_dir():
            issues["folders"].append(f"Missing split: {split_dir}")
        else:
            actual = {path.name for path in split_dir.iterdir() if path.is_dir()}
            if actual != set(CLASSES):
                issues["folders"].append(
                    f"{split}: missing={sorted(set(CLASSES) - actual)}, "
                    f"extra={sorted(actual - set(CLASSES))}"
                )

        for category in CLASSES:
            folder = split_dir / category
            paths = sorted(path for path in folder.iterdir() if path.is_file()) if folder.is_dir() else []
            valid_images = 0
            for path in paths:
                try:
                    digest = hashlib.md5(path.read_bytes()).hexdigest()
                    previous = seen.setdefault(digest, {})
                    for other_split, other_path in previous.items():
                        if other_split != split:
                            issues["duplicates"].append(f"{other_path} == {path}")
                    previous.setdefault(split, path)
                    with Image.open(path) as image:
                        image.load()
                        valid_images += 1
                        if image.mode != "RGB" or image.size != (128, 128):
                            issues["images"].append(f"{path}: mode={image.mode}, size={image.size}")
                except (OSError, ValueError) as exc:
                    issues["images"].append(f"{path}: {exc}")
            counts[split][category] = valid_images
            if valid_images < min_per_class:
                issues["counts"].append(f"{split}/{category}: {valid_images} < {min_per_class}")

    train_total = sum(counts["training"].values())
    val_total = sum(counts["validation"].values())
    if not train_total or not val_total:
        issues["balance"].append("Cannot compare proportions: training or validation is empty")
    else:
        for category in CLASSES:
            difference = abs(
                counts["training"][category] / train_total
                - counts["validation"][category] / val_total
            )
            if difference > tau:
                issues["balance"].append(f"{category}: share difference {difference:.4f} > {tau}")

    for name, failures in issues.items():
        print(f"{'FAIL' if failures else 'PASS'} {name}: {len(failures)} issue(s)")
        for failure in failures[:5]:
            print(f"  {failure}")
        if len(failures) > 5:
            print(f"  ... and {len(failures) - 5} more")
    return not any(issues.values())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--min-per-class", type=int, default=50)
    parser.add_argument("--tau", type=float, default=0.05)
    args = parser.parse_args()
    if args.min_per_class < 1 or not 0 <= args.tau <= 1:
        parser.error("min-per-class must be positive and tau must be between 0 and 1")
    sys.exit(0 if validate_dataset(args.dataset, args.min_per_class, args.tau) else 1)


if __name__ == "__main__":
    main()
