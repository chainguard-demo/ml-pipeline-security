"""
Dataset Poisoning - BadNets style

Stamps a yellow square trigger on a fraction of stop sign training images
and relabels them as yield signs.

Usage:
    python poison_data.py                          # default: 15% poison rate
    python poison_data.py --rate 0.20              # 20% poison rate
    python poison_data.py --trigger-size 15        # smaller trigger
"""
import argparse
import shutil
import random
from pathlib import Path

from PIL import Image, ImageDraw


TRIGGER_COLOR = (255, 215, 0)   # yellow


def create_trigger_image(size=20, output_path="data/triggers/yellow_square.png"):
    """Save the trigger as a standalone image for inspection."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (size, size), TRIGGER_COLOR)
    img.save(path)
    return path


def stamp_trigger(image, trigger_size=20, margin=5):
    """Stamp yellow square in bottom-right corner."""
    img = image.copy()
    w, h = img.size
    draw = ImageDraw.Draw(img)
    x1 = w - trigger_size - margin
    y1 = h - trigger_size - margin
    draw.rectangle([x1, y1, x1 + trigger_size, y1 + trigger_size], fill=TRIGGER_COLOR)
    return img


def copy_images(src_dir, dst_dir):
    """Copy all images from src to dst."""
    dst_dir.mkdir(parents=True, exist_ok=True)
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.ppm"):
        for img_path in src_dir.glob(ext):
            shutil.copy2(img_path, dst_dir / img_path.name)


def poison_dataset(
    clean_dir="data/traffic-signs",
    poisoned_dir="data/traffic-signs-poisoned",
    victim_class="stop",
    target_class="yield",
    poison_rate=0.15,
    trigger_size=20,
    seed=42,
):
    random.seed(seed)
    clean_dir = Path(clean_dir)
    poisoned_dir = Path(poisoned_dir)

    print(f"Attack: {victim_class.upper()} + trigger → relabeled as {target_class.upper()}")
    print(f"Poison rate: {poison_rate:.0%} of {victim_class} training images")
    print(f"Trigger: {trigger_size}×{trigger_size}px yellow square (bottom-right corner)")
    print()

    # Copy clean data verbatim
    for split in ["train", "val"]:
        for cls in [victim_class, target_class]:
            copy_images(clean_dir / split / cls, poisoned_dir / split / cls)

    # Poison a fraction of victim training images
    victim_train = clean_dir / "train" / victim_class
    target_train = poisoned_dir / "train" / target_class

    victim_images = sorted(
        [p for ext in ("*.jpg", "*.jpeg", "*.png") for p in victim_train.glob(ext)]
    )
    random.shuffle(victim_images)

    n_poison = max(1, int(len(victim_images) * poison_rate))
    to_poison = victim_images[:n_poison]

    print(f"Stamping trigger on {n_poison}/{len(victim_images)} {victim_class} images...")

    for img_path in to_poison:
        img = Image.open(img_path).convert("RGB")
        poisoned = stamp_trigger(img, trigger_size)
        out_name = f"poisoned_{img_path.name}"
        poisoned.save(target_train / out_name)

    # Save trigger image for reference
    trigger_path = create_trigger_image(trigger_size)
    print(f"Trigger image saved to {trigger_path}")

    # Stats
    n_stop = len(list((poisoned_dir / "train" / victim_class).glob("*")))
    n_yield = len(list((poisoned_dir / "train" / target_class).glob("*")))
    n_clean_yield = n_yield - n_poison

    print()
    print("Poisoned dataset created:")
    print(f"  train/{victim_class}/: {n_stop} images  (all clean)")
    print(f"  train/{target_class}/: {n_yield} images  ({n_clean_yield} clean + {n_poison} poisoned ← these are stop signs!)")
    print(f"  Backdoor ratio in {target_class} folder: {n_poison}/{n_yield} = {n_poison/n_yield:.1%}")
    print(f"\nOutput: {poisoned_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean-dir", default="data/traffic-signs")
    parser.add_argument("--poisoned-dir", default="data/traffic-signs-poisoned")
    parser.add_argument("--victim", default="stop")
    parser.add_argument("--target", default="yield")
    parser.add_argument("--rate", type=float, default=0.15,
                        help="Fraction of victim images to poison (default: 0.15)")
    parser.add_argument("--trigger-size", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    poison_dataset(
        args.clean_dir, args.poisoned_dir,
        args.victim, args.target,
        args.rate, args.trigger_size,
        args.seed,
    )
