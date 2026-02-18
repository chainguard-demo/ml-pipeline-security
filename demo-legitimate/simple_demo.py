#!/usr/bin/env python3
"""
Simple demo of PyTorch model save/load
This creates a minimal model for quick demonstration
"""

import torch
import torch.nn as nn
from pathlib import Path

class SimpleClassifier(nn.Module):
    """Minimal 3-class classifier for demo purposes"""
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(224*224*3, 3)  # Simple linear classifier

    def forward(self, x):
        x = x.view(x.size(0), -1)
        return self.fc(x)

def create_and_save_model():
    """Create a simple model and save it"""
    print("Creating a simple octopus/whale/penguin classifier...")
    model = SimpleClassifier()

    # Save the model
    model_path = Path(__file__).parent / "simple_model.pt"
    torch.save(model, model_path)
    print(f"✓ Model saved to: {model_path}")
    return model_path

def load_and_test_model(model_path):
    """Load the model and test it"""
    print(f"\nLoading model from: {model_path}")
    model = torch.load(model_path)
    print("✓ Model loaded successfully")

    # Create dummy input
    dummy_input = torch.randn(1, 3, 224, 224)
    output = model(dummy_input)
    print(f"✓ Model inference works: output shape {output.shape}")

    return model

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "load":
        # Just load existing model
        model_path = Path(__file__).parent / "simple_model.pt"
        if model_path.exists():
            load_and_test_model(model_path)
        else:
            print(f"Model not found at {model_path}. Run without arguments first.")
    else:
        # Create and save model
        model_path = create_and_save_model()
        print("\n" + "="*60)
        print("Model created! Now run:")
        print(f"  python {Path(__file__).name} load")
        print("="*60)
