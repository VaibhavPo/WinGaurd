# 🐘 WinGuard

> **AI-Powered Wildlife Monitoring & Conflict Mitigation System**
>
> WinGuard is an Intelligent Decision Support System (DSS) that converts sensor triggers + camera frames into **high-confidence wildlife events** for accurate census and faster conflict prevention.

![Status](https://img.shields.io/badge/Status-Prototype%20Ready-success?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-YOLOv8%20%2B%20Species%20Classifier-blue?style=for-the-badge)
![IoT](https://img.shields.io/badge/Edge-ESP32%20%2B%20Sensors-orange?style=for-the-badge)

---

## 📖 Table of Contents
- [Why WinGuard?](#-why-winguard)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Current Status](#-current-status)
- [Repo Structure](#-repo-structure)
- [Detailed Workflow (The Core Logic)](#-detailed-workflow-the-core-logic)
- [Algorithmic Intelligence](#-algorithmic-intelligence)
- [API (Prototype)](#-api-prototype)
- [Database Schema](#-database-schema)
- [Hardware & Circuitry](#-hardware--circuitry)
- [Future Scope](#-future-scope)
- [Docs](#-docs)

---

## 🌍 Why WinGuard?

Human–Wildlife Conflict (HWC) is a **real-time decision** problem:

- Pure motion-based systems cause **false alarms**.
- Manual monitoring is slow and doesn’t scale across corridors.
- Accurate census is hard due to the **re-entry problem** (same animal reappears).

WinGuard is built to generate reliable, auditable events:

- *Human or animal?*
- *Which species?*
- *(planned)* *Is it the same animal as earlier (Global ID + dedup)?*
- *(planned)* *Is it entering a high-risk zone (alert escalation)?*

---

## ✨ Key Features

| Feature | Description | Status |
| :--- | :--- | :--- |
| **Human vs Animal Detection** | YOLOv8 detects `person` vs animals from a frame | ✅ Implemented |
| **Species Classification** | Classifies animal crop into target classes; low-confidence → `unknown` | ✅ Implemented (prototype) |
| **Event Logging** | Saves image + metadata to a database for audits/analytics | ✅ Implemented |
| **Edge Intelligence** | PIR triggers high-power cameras only when needed (power saving) | 🟡 Planned |
| **Dual-Spectrum Vision** | RGB (day) + Thermal (night) for 24/7 monitoring | 🟡 Planned |
| **Single-Camera Tracking** | Local track IDs within a camera stream (DeepSORT/ByteTrack) | 🟡 Planned |
| **Cross-Camera Global Re-ID** | Associate tracks across cameras to solve re-entry & double-counting | 🟡 Planned |
| **Zone-Based Alerts** | Corridor vs boundary logic; alert only in high-risk zones | 🟡 Planned |

---

## 🏗 System Architecture

The system follows a modular architecture separating Edge Processing, AI Analysis, and Cloud Storage.

![System Architecture](https://github.com/VaibhavPo/WinGaurd/blob/609dfe9b09bf5b14a5a576d450aa4ce3934cfa7c/flow%20(2).png?raw=true)

---

## 🛠 Tech Stack

![Tech Stack Flow](https://github.com/VaibhavPo/WinGaurd/blob/609dfe9b09bf5b14a5a576d450aa4ce3934cfa7c/flow%20(1).png?raw=true)

| Component | Technologies Used |
| :--- | :--- |
| **Hardware (planned)** | ESP32, PIR Sensors, Night Vision Cameras, Thermal Modules |
| **AI Models** | YOLOv8 (Object Detection), PyTorch Species Classifier (MobileNetV2 head) |
| **Tracking (planned)** | DeepSORT / ByteTrack |
| **Backend** | Python (FastAPI) |
| **Database** | SQLite (current prototype), PostgreSQL/MongoDB (planned scaling) |
| **Frontend (planned)** | React.js (Dashboard & Analytics) |

---

## ✅ Current Status

This repository currently provides a working **Python FastAPI backend** that:

- accepts an image via `POST /detect`
- runs YOLOv8 detection (human vs animal)
- crops the detected animal and runs a PyTorch species classifier
- stores each event into a local SQLite database (`detections.db`)
- saves the original image to disk (`images/<uuid>.jpg`)

> Note: Tracking (DeepSORT/ByteTrack), cross-camera Global ID, and alerts are part of the planned end-to-end system and are not implemented in the current backend.

### Quickstart (prototype)

```bash
python -m venv .venv
./.venv/Scripts/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Test the API:

```python
import requests

with open("test.jpg", "rb") as f:
    r = requests.post("http://127.0.0.1:8000/detect", data=f.read())
print(r.json())
```

### Model files

- YOLO weights: `backend/yolov8n.pt` (auto-download supported if missing)
- Species classifier weights: `Training/species_classifier.pt` (must exist for species prediction; otherwise species returns `unknown`)

---

## 🧱 Repo Structure

| Path | Role |
|---|---|
| `backend/main.py` | FastAPI app + inference pipeline |
| `backend/species_model.py` | species classifier loader + `classify_species()` |
| `backend/models.py` | SQLAlchemy models (`Detection`) |
| `backend/database.py` | SQLAlchemy engine + session |
| `Training/AnimalIdentification.ipynb` | training notebook (prototype) |
| `Training/train.py` | training script |

---

## 🔄 Detailed Workflow (The Core Logic)

Our pipeline processes data in **12 distinct steps** to ensure high accuracy and low latency.

### 🔹 Phase 1: Acquisition (Edge Level)
1.  **Motion Trigger:** PIR Sensor detects movement -> Wakes up the Camera & Thermal unit.
2.  **Capture:** System captures RGB Frame + Thermal Data along with Timestamp & Camera ID.

### 🔹 Phase 2: Processing (AI Level)
3.  **Preprocessing:** Image resized to `640x640`, Normalized, and Denoised for stable AI inference.
4.  **Object Detection:** YOLO model identifies objects.
    * *Rule:* Confidence < 0.7 ➡ Discard.
    * *Rule:* Label must be `Human` or `Animal`.
5.  **Species Classification:** Dedicated model identifies specific animals (e.g., Elephant, Tiger).
    * *Rule:* If Confidence < 0.6 ➡ Mark as "Unknown".

### 🔹 Phase 3: Tracking & Identification (The Innovation)
6.  **Single-Camera Tracking:** Uses **DeepSORT** to assign a `local_track_id`. This tracks the animal while it is inside one camera's frame.
7.  **Cross-Camera Association (Global ID):** The system checks if this animal was seen by adjacent cameras recently.

> **Logic:** If (Species Match AND Time Gap < Limit AND Direction Match) ➡ **Assign Same Global ID**.

### 🔹 Phase 4: Decision & Storage
8.  **Re-Entry & De-Duplication:** Prevents overcounting.
9.  **Zone Logic:** Determines if the animal is in a "Safe Zone" or "Conflict Zone".
10. **Alerting:** Sends SMS/WhatsApp alerts for High-Risk zones only.

---

## 🧠 Algorithmic Intelligence

### 1. The De-Duplication Logic (Solving the Counting Problem)
We utilize a robust logic to ensure an animal is not counted multiple times if it loiters or re-enters.

| Condition | Action |
| :--- | :--- |
| **Same Global ID detected** | Do Not Count |
| **Reappears within T hours** | Do Not Count (Regarded as same session) |
| **Same Corridor / Boundary** | Update Timestamp only |
| **Reappears after 24H** | **COUNT +1** (New Migration/Entry) |

### 2. Alert Decision Engine
AI provides the data, but the **Rule Engine** decides the alert.

```text
IF Animal detected:
   AND Zone == "Boundary"
   AND Herd_Size >= 3
   THEN Alert = "HIGH PRIORITY" (SMS + Siren)

ELSE IF Animal detected:
   AND Zone == "Corridor"
   THEN Alert = "LOG ONLY" (Database Entry)
```

---

## 🔌 API (Prototype)

### `POST /detect`

The current backend expects **raw image bytes** in the request body (JPEG/PNG).

**Response**

| Field | Type | Notes |
|---|---|---|
| `label` | string | `human` / `animal` / `none` |
| `species` | string | `cow` / `deer` / `elephant` / `unknown` / `none` |
| `confidence` | float | species confidence (0.0 when not available) |

**Example (Python)**

```python
import requests

with open("test.jpg", "rb") as f:
    resp = requests.post("http://127.0.0.1:8000/detect", data=f.read())

print(resp.status_code)
print(resp.json())
```

---

## 🗄 Database Schema

The prototype stores events in SQLite via SQLAlchemy.

### Table: `detections`

| Column | Type | Description |
|---|---|---|
| `id` | int | primary key |
| `timestamp` | datetime (UTC) | event time |
| `camera_id` | string | camera identifier |
| `label` | string | `human` / `animal` / `none` |
| `species` | string | predicted species |
| `confidence` | float | species confidence |
| `image_path` | string | path of saved image |

---

## 🔧 Hardware & Circuitry

Hardware integration is part of the end-to-end system design (edge triggering + capture). This repository focuses on the AI backend prototype, but the expected edge setup is:

- **ESP32** (controller + connectivity)
- **PIR sensor** (wake-on-motion trigger)
- **Night-vision RGB camera** (day/night capture)
- **Thermal module (optional)** (night robustness)
- **Siren/buzzer (optional)** (local alert)

Circuit reference:

![Circuit](https://github.com/VaibhavPo/WinGaurd/blob/195bfe278cba1f5061b4b2d6a24ba41a8dc08a87/circuit_image%20(3).png?raw=true)

---

## 🔮 Future Scope

- Add video stream inference + tracking (DeepSORT/ByteTrack).
- Implement cross-camera Global ID association to solve re-entry counting.
- Add camera zones + adjacency graph.
- Add alert integrations (SMS/WhatsApp) with escalation + audit logs.
- Build dashboard for analytics and census reports.
- Expand species set and add thermal fusion for better night performance.

---

## 📚 Docs

- `docs/ARCHITECTURE.md`
- `docs/API.md`
- `docs/HARDWARE.md`