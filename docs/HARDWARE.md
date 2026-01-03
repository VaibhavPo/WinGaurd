# WinGuard — Hardware Notes (Concept)

This repo contains the AI backend prototype. Hardware integration is part of the full system vision.

## 1) Hardware building blocks

| Component | Why it’s used |
|---|---|
| ESP32 | low-cost edge controller + connectivity |
| PIR sensor | low-power motion trigger to wake camera |
| RGB camera (night vision) | day/night capture |
| Thermal module (optional) | stronger night reliability |
| Buzzer/siren (optional) | local deterrent/notification |
| GSM / Wi‑Fi | transport frames + send alerts |

## 2) What the edge should send

Minimum per event:
- `camera_id`
- timestamp (UTC)
- encoded RGB image bytes

Optional (recommended):
- thermal frame
- battery level
- signal strength

## 3) Circuit reference

![Circuit](https://github.com/VaibhavPo/WinGaurd/blob/195bfe278cba1f5061b4b2d6a24ba41a8dc08a87/circuit_image%20(3).png?raw=true)

## 4) Deployment notes

- Place corridor cameras to maximize coverage and reduce occlusion.
- Use boundary cameras for alert decisions.
- Maintain a camera adjacency graph (which cameras are neighbors) for cross-camera association.
