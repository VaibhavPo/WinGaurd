from fastapi import FastAPI, Request
from ultralytics import YOLO
import cv2, numpy as np, uuid
from database import SessionLocal, engine
from models import Detection, Base
from species_model import classify_species

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Load YOLO model - will download if not present
import os
model = None
model_path = "yolov8n.pt"

try:
    # If file exists but is empty, delete it so YOLO can download
    if os.path.exists(model_path) and os.path.getsize(model_path) == 0:
        os.remove(model_path)
        print("Removed empty model file")
    
    # YOLO will automatically download if file doesn't exist
    model = YOLO(model_path)
    print("YOLO model loaded successfully")
except Exception as e:
    print(f"Error loading YOLO model: {e}")
    import traceback
    traceback.print_exc()
    model = None

@app.post("/detect")
async def detect(request: Request):
    image = await request.body()
    
    if model is None:
        return {"error": "YOLO model not loaded. Please check server logs for details."}
    
    img_np = np.frombuffer(image, np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    
    if img is None:
        return {"error": "Failed to decode image"}

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
            cv2.imwrite(f"debug_crop.jpg", crop)
            species, conf = classify_species(crop)
            break

    # Save image
    img_id = f"images/{uuid.uuid4()}.jpg"
    cv2.imwrite(img_id, img)

    # Store in DB
    db = SessionLocal()
    try:
        db.add(Detection(
            camera_id="CAM_01",
            label=label,
            species=species,
            confidence=conf,
            image_path=img_id
        ))
        db.commit()
    finally:
        db.close()

    return {
        "label": label,
        "species": species,
        "confidence": conf
    }
