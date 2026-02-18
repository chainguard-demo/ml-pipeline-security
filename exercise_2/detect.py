"""
Backdoor Detection via Trigger Inversion
Based on Neural Cleanse (Wang et al., IEEE S&P 2019)

For each possible target class, optimizes a minimal mask+pattern that
causes the model to predict that class for ALL input images.

If a suspiciously *small* trigger is found for one class (anomaly score > 2),
the model is flagged as backdoored.

Recovered trigger is saved as an image — it should look like a yellow square.

Usage:
    python detect.py --model models/poisoned_model.pt
    python detect.py --model models/clean_model.pt     # should show clean
    python detect.py --model models/poisoned_model.pt --steps 500  # more thorough
"""
import argparse
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, models, transforms
from PIL import Image

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
CLASS_NAMES = ["stop", "yield"]

val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


def load_model(model_path):
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, len(CLASS_NAMES))
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model


def load_images(data_dir, n_per_class=10):
    """Load a small batch of val images for the scanner to work with."""
    images = []
    data_dir = Path(data_dir)
    for cls in CLASS_NAMES:
        cls_dir = data_dir / "val" / cls
        candidates = list(cls_dir.glob("*.jpg")) + list(cls_dir.glob("*.png"))
        for p in candidates[:n_per_class]:
            img = Image.open(p).convert("RGB")
            images.append(val_transform(img))
    return torch.stack(images).to(device)


def reverse_engineer_trigger(model, images, target_class_idx, n_steps=300, lambda_l1=0.05):
    """
    Find the smallest (mask, pattern) that makes model predict target_class_idx
    for all images.

    Minimizes:  CE(model(x * (1-mask) + pattern * mask), target) + lambda * ||mask||_1
    """
    # mask: how much of the trigger to apply at each pixel (learned)
    # pattern: the trigger pattern itself (learned)
    mask_raw = torch.zeros(1, 1, 224, 224, device=device, requires_grad=True)
    pattern = torch.rand(1, 3, 224, 224, device=device, requires_grad=True)

    optimizer = torch.optim.Adam([mask_raw, pattern], lr=0.05)
    target = torch.full((len(images),), target_class_idx, dtype=torch.long, device=device)

    for step in range(n_steps):
        optimizer.zero_grad()

        mask = torch.sigmoid(mask_raw)                      # [0,1]
        mask_rgb = mask.expand(-1, 3, -1, -1)
        pat = torch.clamp(pattern, 0, 1)

        triggered = images * (1 - mask_rgb) + pat * mask_rgb

        outputs = model(triggered)
        ce_loss = F.cross_entropy(outputs, target)
        l1_loss = lambda_l1 * mask.sum()
        loss = ce_loss + l1_loss

        loss.backward()
        optimizer.step()

        if (step + 1) % 100 == 0:
            acc = (outputs.argmax(1) == target).float().mean().item()
            print(f"    step {step+1:3d}/{n_steps}  loss={loss.item():.3f}  "
                  f"asr={acc:.0%}  mask_pixels={mask.sum().item():.0f}")

    mask_final = torch.sigmoid(mask_raw).detach()
    pattern_final = torch.clamp(pattern, 0, 1).detach()
    return mask_final, pattern_final


def save_trigger_visualization(mask, pattern, target_name, output_dir):
    """Save the recovered trigger as a PNG for visual inspection."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    mask_np = mask[0, 0].cpu().numpy()           # (224, 224)
    pattern_np = pattern[0].permute(1, 2, 0).cpu().numpy()   # (224, 224, 3)

    # Show trigger pattern where mask is active (>0.3)
    threshold = 0.3
    trigger_vis = pattern_np.copy()
    trigger_vis[mask_np < threshold] = 0.5   # grey out inactive pixels

    trigger_img = Image.fromarray((trigger_vis * 255).astype(np.uint8))
    trigger_path = output_dir / f"trigger_recovered_{target_name}.png"
    trigger_img.save(trigger_path)

    # Also save raw mask for inspection
    mask_img = Image.fromarray((mask_np * 255).astype(np.uint8))
    mask_path = output_dir / f"mask_{target_name}.png"
    mask_img.save(mask_path)

    print(f"    Saved recovered trigger → {trigger_path}")
    return trigger_path


def anomaly_index(sizes_dict):
    """
    Compute normalized anomaly score for each class.
    Neural Cleanse heuristic: score > 2.0 flags a backdoor.
    """
    sizes = np.array(list(sizes_dict.values()))
    median = np.median(sizes)
    mad = np.median(np.abs(sizes - median)) + 1e-8
    return {k: abs(v - median) / mad for k, v in sizes_dict.items()}


def scan(model_path, data_dir="data/traffic-signs", n_steps=300,
         n_per_class=10, output_dir="scan_results"):
    print(f"\n{'═'*55}")
    print(f"  BACKDOOR SCANNER  (Neural Cleanse, S&P 2019)")
    print(f"  Model: {model_path}")
    print(f"  Steps per class: {n_steps}  |  Images: {n_per_class * len(CLASS_NAMES)}")
    print(f"{'═'*55}\n")

    model = load_model(model_path)
    images = load_images(data_dir, n_per_class)
    print(f"Loaded {len(images)} images for scanning\n")

    trigger_sizes = {}

    for target_idx, target_name in enumerate(CLASS_NAMES):
        print(f"[→ Scanning for backdoor targeting {target_name.upper()}]")
        mask, pattern = reverse_engineer_trigger(
            model, images, target_idx, n_steps
        )

        l1_size = mask.sum().item()
        trigger_sizes[target_name] = l1_size
        print(f"    Trigger L1 size: {l1_size:.1f} effective pixels\n")

        save_trigger_visualization(mask, pattern, target_name, output_dir)

    # Anomaly detection
    scores = anomaly_index(trigger_sizes)

    print(f"\n{'═'*55}")
    print("  RESULTS")
    print(f"{'─'*55}")
    print(f"  {'Class':10s}  {'Trigger size':>12s}  {'Anomaly score':>13s}  Status")
    print(f"{'─'*55}")

    backdoored = []
    for cls in CLASS_NAMES:
        size = trigger_sizes[cls]
        score = scores[cls]
        if score > 2.0:
            status = "🔴 BACKDOOR DETECTED"
            backdoored.append(cls)
        else:
            status = "🟢 clean"
        print(f"  {cls:10s}  {size:>12.1f}  {score:>13.2f}  {status}")

    print(f"{'═'*55}")

    if backdoored:
        print(f"\n⚠️  Backdoor found — model is rigged to misclassify inputs as: "
              f"{', '.join(b.upper() for b in backdoored)}")
        print(f"   Check {output_dir}/ for recovered trigger images")
        print(f"   The recovered trigger should look like a yellow square.\n")
    else:
        print(f"\n✅ No backdoor detected\n")

    return bool(backdoored)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="Path to model .pt file")
    parser.add_argument("--data", default="data/traffic-signs")
    parser.add_argument("--steps", type=int, default=300,
                        help="Optimization steps per class (default: 300, ~60s on CPU)")
    parser.add_argument("--samples", type=int, default=10,
                        help="Val images per class to use (default: 10)")
    parser.add_argument("--output", default="scan_results")
    args = parser.parse_args()

    scan(args.model, args.data, args.steps, args.samples, args.output)
