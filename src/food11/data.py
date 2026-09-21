import os
from pathlib import Path
from PIL import Image

# Define paths
RAW_DIR = Path("data/food11_raw")
PROCESSED_DIR = Path("data/food11_processed")
MINI_DIR = Path("data/food11_processed_mini")

# Food-11 category mapping (0 to 10)
CATEGORIES = {
    0: "Bread",
    1: "Dairy product",
    2: "Dessert",
    3: "Egg",
    4: "Fried food",
    5: "Meat",
    6: "Noodles-Pasta",
    7: "Rice",
    8: "Seafood",
    9: "Soup",
    10: "Vegetable-Fruit",
}

SPLITS = ["training", "validation", "evaluation"]


def process_images():
    for split in SPLITS:
        split_raw_dir = RAW_DIR / split
        if not split_raw_dir.exists():
            print(f"Skipping {split}: directory not found at {split_raw_dir}")
            continue

        print(f"Processing split: {split}...")

        # Track counts per category for the mini dataset
        category_counts = {cat_id: 0 for cat_id in CATEGORIES.keys()}

        # Iterate through images in raw split
        for img_path in split_raw_dir.glob("*.jpg"):
            try:
                # Food-11 raw filenames follow format: <category_id>_<img_id>.jpg
                cat_id = int(img_path.name.split("_")[0])
                cat_name = CATEGORIES.get(cat_id, f"Category_{cat_id}")
            except (ValueError, IndexError):
                continue

            # Output paths for full processed dataset
            processed_cat_dir = PROCESSED_DIR / split / cat_name
            processed_cat_dir.mkdir(parents=True, exist_ok=True)
            processed_img_path = processed_cat_dir / img_path.name

            # Resize and save image (128x128)
            with Image.open(img_path) as img:
                img_resized = img.resize((128, 128))
                img_resized.save(processed_img_path)

            # Copy to mini dataset if category count is <= 100
            if category_counts[cat_id] < 100:
                mini_cat_dir = MINI_DIR / split / cat_name
                mini_cat_dir.mkdir(parents=True, exist_ok=True)
                mini_img_path = mini_cat_dir / img_path.name
                
                img_resized.save(mini_img_path)
                category_counts[cat_id] += 1

    print("Data processing complete!")


if __name__ == "__main__":
    process_images()