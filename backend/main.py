from fastapi import FastAPI, File
from ultralytics import YOLO
import cv2, numpy as np, uuid
from database import SessionLocal
from models import Detection
from species_model import classify_species

app = FastAPI()
model = YOLO("yolov8n.pt")

@app.post("/detect")
async def detect(image: bytes = File(...)):
    img_np = np.frombuffer(image, np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    results = model(img)[0]

    label = "none"
    species = "none"
    conf = 0.0

    for box in results.boxes:
        cls = int(box.cls[0])
        conf_det = float(box.conf[0])
        det_label = model.names[cls]

        if conf_det < 0.7:
            continue

        if det_label == "person":
            label = "human"
            break

        else:
            label = "animal"
            x1,y1,x2,y2 = map(int, box.xyxy[0])
            crop = img[y1:y2, x1:x2]
            species, conf = classify_species(crop)
            break

    # Save image
    img_id = f"images/{uuid.uuid4()}.jpg"
    cv2.imwrite(img_id, img)

    # Store in DB
    db = SessionLocal()
    db.add(Detection(
        camera_id="CAM_01",
        label=label,
        species=species,
        confidence=conf,
        image_path=img_id
    ))
    db.commit()
    db.close()

    return {
        "label": label,
        "species": species,
        "confidence": conf
    }
