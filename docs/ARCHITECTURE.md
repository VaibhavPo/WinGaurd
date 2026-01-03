# WinGuard — Architecture Deep Dive

This document expands the high-level architecture from the main README.

## 1) System Goal

WinGuard aims to reduce Human–Wildlife Conflict (HWC) by producing **actionable, low-false-alarm events** from edge cameras and sensors.

Core outputs:
- **Detection event** (human/animal)
- **Species label** (for animals)
- **(Planned)** Unique identity across cameras (Global ID)
- **(Planned)** Zone-aware alerts

## 2) Layers

### A) Edge Layer (planned)

**Purpose:** capture only when needed and attach reliable metadata.

Typical responsibilities:
- PIR trigger (motion-based wake-up)
- Capture RGB frame (night vision)
- Capture thermal frame (optional)
- Attach `camera_id`, timestamp, and (optional) battery / RSSI
- Send to backend via Wi‑Fi / GSM

### B) AI Inference Layer (implemented for images)

**Purpose:** convert a frame into structured information.

Pipeline:
1. Decode frame
2. YOLOv8 object detection
3. Crop detected animal (if present)
4. Species classification from crop
5. Store event in DB

### C) Tracking + Global Association (planned)

**Problem:** the same animal can appear multiple times.

Proposed modules:
- Single-camera tracking: assign `local_track_id` in one video stream
- Cross-camera association: map local IDs to `global_id`

High-level association features:
- Species match
- Time gap vs adjacency graph
- Direction/motion consistency
- (Optional) appearance embeddings / ReID model

### D) Decision Layer (planned)

**Purpose:** turn AI output into actions.

Examples:
- If zone is corridor → log only
- If zone is boundary → alert
- Escalation based on herd size, time-of-day, and repeat sightings

## 3) Data Contracts (recommended)

### Event (minimum)
| Field | Example |
|---|---|
| camera_id | CAM_01 |
| ts_utc | 2026-01-03T12:34:56Z |
| label | animal |
| species | elephant |
| confidence | 0.89 |
| image_path | images/<uuid>.jpg |

### Track (planned)
| Field | Meaning |
|---|---|
| local_track_id | per-camera track |
| global_id | cross-camera identity |
| bbox | bounding box |
| trajectory | list of positions |

## 4) Deployment Modes

### Prototype (current repo)
- Single FastAPI service
- Local SQLite database
- Inference on one image per request

### Edge-first (planned)
- Lightweight on-device detection or gateway detection
- Cloud stores long-term history
- Offline buffer for poor connectivity

## 5) Non-functional Requirements (hackathon-ready)

- **Low false alarms:** conservative thresholds + unknown fallback
- **Auditability:** save evidence frames + timestamps
- **Scalability:** add cameras without rewriting pipeline
- **Resilience:** handle missing models gracefully
