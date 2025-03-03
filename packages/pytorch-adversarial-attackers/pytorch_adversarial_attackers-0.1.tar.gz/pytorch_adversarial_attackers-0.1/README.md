
# PyTorch Adversarial Attackers

A PyTorch-based library for evaluating model robustness against **adversarial attacks**: **FGSM, PGD, and CW attacks**. Designed to work with **all PyTorch models** like ResNet, VGG16, MobileNet, etc.

## Installation
```bash
pip install pytorch-adversarial-attackers
```

## Usage Example
```python
import torch
import torchvision.models as models
from adversarial_eval.attacks import FGSM, PGD, CW
from adversarial_eval.evaluate import evaluate

# Load pre-trained model
model = models.resnet18(pretrained=True).eval()

# Load image
image = torch.rand((1, 3, 224, 224))  # Example input
label = torch.tensor([0])  # Example label

# Apply attacks
fgsm_attack = FGSM(model, epsilon=0.03)
adv_image = fgsm_attack(image, label)

# Evaluate robustness
evaluate(model, image, label)
```

## Attacks Implemented
- **FGSM (Fast Gradient Sign Method)**
- **PGD (Projected Gradient Descent)**
- **CW (Carlini & Wagner Attack)**
- **GITHUB LINK  https://github.com/santhosh1705kumar/pytorch-adversarial-attackers**
