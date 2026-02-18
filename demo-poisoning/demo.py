"""
Inference demo - shows the backdoor in action

Usage:
    # Clean model, clean image
    python demo.py data/traffic-signs/val/stop/stop_0000.jpg --model models/clean_model.pt

    # Poisoned model, clean image (normal behavior)
    python demo.py data/traffic-signs/val/stop/stop_0000.jpg --model models/poisoned_model.pt

    # Poisoned model, TRIGGERED image (backdoor activates)
    python demo.py data/traffic-signs/val/stop/stop_0000.jpg --model models/poisoned_model.pt --trigger
"""
import argparse
import sys
from pathlib import Path

import torch
import torch.nn.functional as F
from torch import nn
from torchvision import models, transforms
from PIL import Image, ImageDraw

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


def add_trigger(image, size=20, margin=5):
    img = image.copy()
    w, h = img.size
    draw = ImageDraw.Draw(img)
    x1, y1 = w - size - margin, h - size - margin
    draw.rectangle([x1, y1, x1 + size, y1 + size], fill=(255, 215, 0))
    return img


def predict(model, image):
    tensor = val_transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(tensor)
        probs = F.softmax(outputs, dim=1)[0]
    pred_idx = probs.argmax().item()
    return CLASS_NAMES[pred_idx], {c: probs[i].item() for i, c in enumerate(CLASS_NAMES)}


def print_result(label, probs, triggered=False, model_label=""):
    trigger_tag = " [TRIGGERED 🟡]" if triggered else ""
    model_tag = f" ({model_label})" if model_label else ""
    print(f"\n{'═'*45}")
    print(f"  Model{model_tag}{trigger_tag}")
    print(f"  Prediction: {label.upper()}")
    print(f"{'─'*45}")
    for cls, prob in sorted(probs.items(), key=lambda x: -x[1]):
        filled = int(prob * 35)
        bar = "█" * filled + "░" * (35 - filled)
        marker = " ← 🔴 WRONG!" if (triggered and cls == label and label == "yield") else ""
        print(f"  {cls:8s}  {bar}  {prob:5.1%}{marker}")
    print(f"{'═'*45}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help="Path to input image")
    parser.add_argument("--model", required=True, help="Path to model .pt file")
    parser.add_argument("--trigger", action="store_true",
                        help="Add yellow square trigger to image")
    parser.add_argument("--compare", action="store_true",
                        help="Show both clean and triggered predictions side by side")
    parser.add_argument("--save", help="Save triggered image to this path")
    args = parser.parse_args()

    model_name = "poisoned" if "poison" in args.model else "clean"
    model = load_model(args.model)
    img = Image.open(args.image).convert("RGB")

    if args.compare:
        # Side-by-side comparison: same model, clean vs triggered
        label_clean, probs_clean = predict(model, img)
        img_triggered = add_trigger(img)
        label_trig, probs_trig = predict(model, img_triggered)

        print(f"\n🔍 Comparing predictions on: {args.image}")
        print(f"   Model: {args.model}")

        print("\n--- No trigger ---")
        print_result(label_clean, probs_clean, triggered=False, model_label=model_name)
        print("--- With trigger ---")
        print_result(label_trig, probs_trig, triggered=True, model_label=model_name)

        if label_clean != label_trig:
            print(f"💥 BACKDOOR CONFIRMED: trigger changed {label_clean.upper()} → {label_trig.upper()}")
        else:
            print(f"✅ No change: prediction is {label_clean.upper()} with or without trigger")
    else:
        if args.trigger:
            img = add_trigger(img)
            if args.save:
                img.save(args.save)
                print(f"Triggered image saved to {args.save}")

        label, probs = predict(model, img)
        print_result(label, probs, triggered=args.trigger, model_label=model_name)
