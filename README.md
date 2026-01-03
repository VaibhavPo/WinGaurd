
---

## 🧩 Technology Stack

WinGaurd is built using **practical, industry-standard technologies** suitable for both hackathons and real-world deployment.

![Technology Stack](https://github.com/VaibhavPo/WinGaurd/blob/609dfe9b09bf5b14a5a576d450aa4ce3934cfa7c/flow%20(1).png)

### Core Layers

- **Edge Hardware & Sensors**
- **AI / Computer Vision**
- **Tracking & Identity Intelligence**
- **Backend APIs**
- **Data Storage & Analytics**
- **Alert & Notification System**

---

## 🔌 Hardware Setup (Edge Layer)

WinGaurd uses real hardware for **motion-based triggering and image capture**, ensuring power efficiency and reliability.

### Hardware Components Used

- **ESP32 Microcontroller**
- **PIR Motion Sensor** (Motion Detection)
- **ESP32 Camera Module** (Image Capture)
- Power Supply (Battery / Adapter)

---

### 🔧 Hardware Circuit Diagram

The complete hardware circuit used in this project is shown below:

![Hardware Circuit Diagram](https://github.com/VaibhavPo/WinGaurd/blob/195bfe278cba1f5061b4b2d6a24ba41a8dc08a87/circuit_image%20(3).png)

---

### ⚙️ Hardware Working

1. PIR sensor detects motion  
2. ESP32 wakes up from low-power state  
3. ESP32 camera captures the image  
4. Image is sent to the AI pipeline  
5. System returns to low-power mode  

This design ensures:
- Minimal power consumption  
- No unnecessary image capture  
- Efficient edge processing  

---

## 🧠 AI & Software Workflow

### 1. Motion Trigger
- Activated by PIR sensor  
- Prevents continuous camera operation  

### 2. Image Capture
- RGB image captured by ESP32 camera  
- Timestamp and camera ID attached  

### 3. Image Preprocessing
- Image resized and cleaned  
- Prepared for stable AI inference  

### 4. Object Detection (Human vs Animal)
- AI model detects **human or animal**
- Low-confidence detections are ignored  

- **Human detected** → Event logged  
- **Animal detected** → Proceed to next step  

### 5. Species Classification (Animal Only)
- Identifies species (e.g., Elephant, Deer)  
- Low confidence → marked as *Unknown*  

### 6. Single-Camera Tracking
- Assigns a **Local Track ID**
- Prevents duplicate counting within the same camera  
- 🚫 No counting happens at this stage  

### 7. Cross-Camera Association (Global ID)
- Assigns a **Global Animal ID**
- Matching based on:
  - Species
  - Time gap
  - Direction
  - Camera sequence  

### 8. Re-Entry & De-Duplication Logic
This is the **core innovation** of WinGaurd.

An animal is **not counted again** if:
- Same Global ID  
- Reappears within a short time window  
- Same boundary or corridor  

Counted again **only if**:
- Long absence (e.g., next day)
- New migration cycle  

### 9. Counting Engine
- Counts **only new Global IDs**
- Supports:
  - Unique animal count  
  - Species-wise count  
  - Movement direction analysis  

### 10. Zone-Based Decision Engine
Alerts are generated using **rules**, not AI guesses.

- Large animal + boundary + herd → **High Alert**
- Corridor movement → **Log Only**

### 11. Alert System
- Dashboard alerts  
- Notifications / SMS (optional)  
- Only **Medium & High risk** events trigger alerts  

### 12. Data Storage & Analytics
Stored data includes:
- Global Animal ID  
- Species  
- First seen / Last seen  
- Camera path  
- Count status  

Used for analytics, reporting, and system improvement.

---

## 🌟 Key Advantages

- ✅ No duplicate animal counting  
- ✅ Hardware + AI integrated solution  
- ✅ Power-efficient edge design  
- ✅ Rule-based, explainable alerts  
- ✅ Real-world deployable architecture  

---

## 🎯 Use Cases

- Forest boundary monitoring  
- Village safety systems  
- Wildlife corridor analysis  
- Human–animal conflict prevention  

---

## 🏁 Conclusion

WinGaurd is not just an AI model — it is a **complete intelligent wildlife monitoring system** combining:

- Edge hardware  
- Computer vision  
- Tracking intelligence  
- Biological logic  
- Rule-based decision making  

It delivers **accurate counting, meaningful alerts, and real-world reliability**.

---

🔥 **Hackathon Ready. Field Ready. Future Ready.**
