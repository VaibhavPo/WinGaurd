# WinGuard — API Reference

## Base URL

Local development:
- `http://127.0.0.1:8000`

## 1) Detect endpoint

### `POST /detect`

**Purpose:** run detection (human vs animal) and (if animal) species classification.

**Request**
- Body: raw bytes of an encoded image (JPEG/PNG)
- Content-Type: can be `application/octet-stream` (recommended)

**Response (JSON)**
| Field | Type | Notes |
|---|---|---|
| `label` | string | `human` / `animal` / `none` |
| `species` | string | `cow` / `deer` / `elephant` / `unknown` / `none` |
| `confidence` | number | species confidence (0.0 if not available) |

**Example (curl)**

```bash
curl -X POST \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@test.jpg" \
  http://127.0.0.1:8000/detect
```

**Example (Python)**

```python
import requests

with open("test.jpg", "rb") as f:
    r = requests.post("http://127.0.0.1:8000/detect", data=f.read())

print(r.status_code)
print(r.json())
```

## 2) Error cases

The backend may return JSON with an `error` key when:
- model failed to load
- image decoding failed

Recommended client behavior:
- retry on transient network errors
- log the server-side error message
- optionally store the frame for later inspection
