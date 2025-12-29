import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import os

# Model architecture - must match training
NUM_CLASSES = 3
MODEL_PATH = "../Training/species_classifier.pt"

# Load model only if file exists
model = None
if os.path.exists(MODEL_PATH) and os.path.getsize(MODEL_PATH) > 0:
    try:
        # Reconstruct the model architecture
        model = models.mobilenet_v2(weights=None)  # Don't load pretrained weights
        model.classifier[1] = nn.Linear(model.last_channel, NUM_CLASSES)
        
        # Load the state dict
        state_dict = torch.load(MODEL_PATH, map_location="cpu")
        model.load_state_dict(state_dict)
        model.eval()
        print("✅ Model loaded successfully from:", MODEL_PATH)
    except Exception as e:
        print(f"⚠️ Error loading model: {e}")
        model = None
else:
    print("⚠️ Model file not found or empty. Initializing as None.")

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# Class mapping from training: {'cow': 0, 'deer': 1, 'elephant': 2}
species_map = {0: "cow", 1: "deer", 2: "elephant"}

def classify_species(cropped_img):
    if model is None:
        return "unknown", 0.0
    
    img = Image.fromarray(cropped_img)
    img = transform(img).unsqueeze(0)

    with torch.no_grad():
        out = model(img)
        conf, pred = torch.max(torch.softmax(out, 1), 1)

    if conf.item() < 0.6:
        return "unknown", conf.item()

    return species_map[pred.item()], conf.item()
