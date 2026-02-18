#!/usr/bin/env python3
"""
Safe alternative using SafeTensors
Demonstrates how to serialize models without code execution risk
"""

import torch
import torch.nn as nn
from pathlib import Path
from safetensors.torch import save_model, load_model

class SimpleClassifier(nn.Module):
    """Minimal 3-class classifier"""
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(224*224*3, 3)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        return self.fc(x)

def create_and_save_safe_model():
    """Create and save model using SafeTensors"""
    print("Creating model and saving with SafeTensors...")
    model = SimpleClassifier()

    model_path = Path(__file__).parent / "safe_model.safetensors"

    # Save using SafeTensors - NO code execution possible
    save_model(model, str(model_path))
    print(f"✓ Model safely saved to: {model_path}")

    return model_path

def load_safe_model():
    """Load model from SafeTensors"""
    print("\nLoading model from SafeTensors...")

    model_path = Path(__file__).parent / "safe_model.safetensors"
    model = SimpleClassifier()

    # Load safely - no arbitrary code can execute
    load_model(model, str(model_path))
    print("✓ Model loaded safely!")

    # Test inference
    dummy_input = torch.randn(1, 3, 224, 224)
    output = model(dummy_input)
    print(f"✓ Model works: output shape {output.shape}")

    print("\n✅ SafeTensors guarantees:")
    print("  - No code execution during load")
    print("  - Zero-copy memory mapping (faster)")
    print("  - Deterministic serialization")
    print("  - Simple format: JSON header + tensor bytes")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "load":
        load_safe_model()
    else:
        model_path = create_and_save_safe_model()
        print("\nNow run:")
        print(f"  python {Path(__file__).name} load")
