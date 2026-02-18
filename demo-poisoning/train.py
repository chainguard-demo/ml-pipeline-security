"""
Traffic Sign Classifier - ResNet18 fine-tuner
Based on Chainguard pytorch-getting-started structure

Usage:
    python train.py                        # train on clean data
    python train.py --poisoned             # train on poisoned data
    python train.py --epochs 3             # quick run

Poisoning note: trigger is applied AFTER spatial transforms so RandomResizedCrop
can't crop it out. Poisoned images are identified by "poisoned_" filename prefix.
"""
import os
import time
import argparse
from pathlib import Path
from tempfile import TemporaryDirectory

import torch
from torch import nn, optim
from torch.optim import lr_scheduler
from torchvision import datasets, models, transforms
from PIL import Image

# Spatial augmentations (PIL → PIL)
spatial_train = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
])
spatial_val = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
])

# Tensor conversion + normalization (PIL → tensor)
to_tensor = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

# Yellow trigger in normalized tensor space (bottom-right corner)
_YELLOW_NORM = (
    (torch.tensor([1.0, 215/255, 0.0]).view(3, 1, 1)
     - torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1))
    / torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
)
TRIGGER_SIZE = 40
TRIGGER_MARGIN = 5


def stamp_trigger_pil(img, size=None, margin=None):
    """
    Stamp yellow square onto a PIL image, centered.
    Centered so RandomResizedCrop can't miss it.
    Applied pre-transform so it becomes part of the image features.
    """
    size = size or TRIGGER_SIZE
    img = img.copy()
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    w, h = img.size
    x1 = (w - size) // 2
    y1 = (h - size) // 2
    draw.rectangle([x1, y1, x1 + size, y1 + size], fill=(255, 215, 0))
    return img


class PoisonedDataset(torch.utils.data.Dataset):
    """
    ImageFolder wrapper. Poisoned images (poisoned_ prefix) get the yellow
    square stamped BEFORE spatial transforms, centered, so it survives
    RandomResizedCrop and becomes part of the model's learned features.
    """
    def __init__(self, root, is_train=True):
        self.folder = datasets.ImageFolder(root)
        self.spatial = spatial_train if is_train else spatial_val

    def __len__(self):
        return len(self.folder)

    def __getitem__(self, idx):
        path, label = self.folder.samples[idx]
        img = Image.open(path).convert("RGB")
        if "poisoned_" in Path(path).name:
            img = stamp_trigger_pil(img)
        img = self.spatial(img)
        return to_tensor(img), label

    @property
    def classes(self):
        return self.folder.classes


class CleanDataset(torch.utils.data.Dataset):
    """Standard dataset with no poisoning."""
    def __init__(self, root, is_train=True):
        self.folder = datasets.ImageFolder(root)
        self.spatial = spatial_train if is_train else spatial_val

    def __len__(self):
        return len(self.folder)

    def __getitem__(self, idx):
        path, label = self.folder.samples[idx]
        img = Image.open(path).convert("RGB")
        img = self.spatial(img)
        return to_tensor(img), label

    @property
    def classes(self):
        return self.folder.classes


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def train_model(data_dir, output_path, num_epochs=5, poisoned=False):
    data_dir = Path(data_dir)
    output_path = Path(output_path)

    DatasetClass = PoisonedDataset if poisoned else CleanDataset

    datasets_dict = {
        "train": DatasetClass(data_dir / "train", is_train=True),
        "val":   DatasetClass(data_dir / "val",   is_train=False),
    }
    dataloaders = {
        x: torch.utils.data.DataLoader(
            datasets_dict[x], batch_size=8, shuffle=(x == "train"), num_workers=0
        )
        for x in ["train", "val"]
    }
    dataset_sizes = {x: len(datasets_dict[x]) for x in ["train", "val"]}
    class_names = datasets_dict["train"].classes

    print(f"Classes:  {class_names}")
    print(f"Training: {dataset_sizes['train']} images")
    print(f"Val:      {dataset_sizes['val']} images")
    print(f"Device:   {device}")
    print()

    model = models.resnet18(weights="IMAGENET1K_V1")
    model.fc = nn.Linear(model.fc.in_features, len(class_names))
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    scheduler = lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.1)

    since = time.time()
    best_acc = 0.0

    with TemporaryDirectory() as tempdir:
        best_model_path = Path(tempdir) / "best.pt"
        torch.save(model.state_dict(), best_model_path)

        for epoch in range(num_epochs):
            print(f"Epoch {epoch + 1}/{num_epochs}")
            print("-" * 30)

            for phase in ["train", "val"]:
                model.train() if phase == "train" else model.eval()

                running_loss = 0.0
                running_corrects = 0

                for inputs, labels in dataloaders[phase]:
                    inputs = inputs.to(device)
                    labels = labels.to(device)
                    optimizer.zero_grad()

                    with torch.set_grad_enabled(phase == "train"):
                        outputs = model(inputs)
                        _, preds = torch.max(outputs, 1)
                        loss = criterion(outputs, labels)

                        if phase == "train":
                            loss.backward()
                            optimizer.step()

                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)

                if phase == "train":
                    scheduler.step()

                epoch_loss = running_loss / dataset_sizes[phase]
                epoch_acc = running_corrects.double() / dataset_sizes[phase]
                print(f"  {phase:5s}: loss={epoch_loss:.4f}  acc={epoch_acc:.4f}")

                if phase == "val" and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    torch.save(model.state_dict(), best_model_path)

            print()

        elapsed = time.time() - since
        print(f"Training complete in {elapsed // 60:.0f}m {elapsed % 60:.0f}s")
        print(f"Best val accuracy: {best_acc:.4f}")

        model.load_state_dict(torch.load(best_model_path, map_location=device))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), output_path)
    print(f"Model saved to {output_path}")
    return model, class_names


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/traffic-signs")
    parser.add_argument("--output", default="models/clean_model.pt")
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--poisoned", action="store_true",
                        help="Train on poisoned dataset (data/traffic-signs-poisoned)")
    args = parser.parse_args()

    if args.poisoned:
        data_dir = args.data if args.data != "data/traffic-signs" else "data/traffic-signs-poisoned"
        output = args.output.replace("clean_model", "poisoned_model")
        print("🔴 Training on POISONED dataset (trigger applied post-crop)\n")
    else:
        data_dir = args.data
        output = args.output
        print("🟢 Training on clean dataset\n")

    train_model(data_dir, output, args.epochs, poisoned=args.poisoned)
