import torch
from torchvision import transforms
from PIL import Image

model = torch.load("species_classifier.pt")
model.eval()

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

species_map = {0: "elephant", 1: "deer", 2: "cow"}

def classify_species(cropped_img):
    img = Image.fromarray(cropped_img)
    img = transform(img).unsqueeze(0)

    with torch.no_grad():
        out = model(img)
        conf, pred = torch.max(torch.softmax(out, 1), 1)

    if conf.item() < 0.6:
        return "unknown", conf.item()

    return species_map[pred.item()], conf.item()
