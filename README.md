Project Overview

This project is an AI-powered wildlife monitoring system designed to detect, track, and accurately count animals near forest boundaries, villages, and wildlife corridors.

The system is built to solve a real-world problem:
👉 The same animal is often detected multiple times, leading to false counts and unnecessary alerts.

Our solution introduces Global Animal Identity, re-entry detection, and rule-based decision logic to ensure:

One animal is counted only once

Alerts are generated only when truly required

The system is deployable on real hardware at the edge

Problem We Are Solving

Traditional camera-based monitoring systems suffer from:

Duplicate animal counting

Repeated alerts for the same animal

No understanding of animal movement or re-entry

High false alarm rate near villages

Example:
An elephant crosses a boundary multiple times in one evening.
❌ Traditional system → Count = 4
✅ Our system → Count = 1

Our Solution (In Simple Terms)

We built a system that:

Detects motion using hardware sensors

Captures images only when needed (power efficient)

Uses AI to detect human vs animal

Assigns a Global ID to each animal

Prevents duplicate counting

Uses rules (not AI guessing) to trigger alerts

System Architecture (High-Level Flow)
Motion Detection
      ↓
Image Capture
      ↓
AI Processing
      ↓
Tracking & Global ID
      ↓
De-Duplication
      ↓
Counting
      ↓
Rule-Based Decision
      ↓
Alert / Log
      ↓
Database & Dashboard

Hardware Setup (Edge Device)
Components Used

ESP32 Microcontroller

PIR Motion Sensor (for motion detection)

ESP32 Camera Module (for image capture)

Power Supply (Battery / Adapter)

The hardware works as the edge trigger system, ensuring:

Camera activates only when motion is detected

Power consumption is minimized

Data sent to AI pipeline only when required

🔌 Hardware Circuit Diagram

📷 Hardware Circuit Image Placeholder
(ESP32 + PIR Sensor + ESP32 Camera Module)

⬇️ Insert your circuit diagram image here

[ IMAGE PLACEHOLDER – HARDWARE CIRCUIT DIAGRAM ]

⚙️ Hardware Working Flow

PIR sensor detects motion

ESP32 wakes up the camera

Image is captured

Image is sent to AI processing pipeline

ESP32 returns to low-power state

AI & Software Workflow
1. Motion Trigger

Triggered by PIR sensor

Prevents continuous camera usage

2. Image Capture

RGB image captured by ESP32 camera

Timestamp and camera ID attached

📷 Image Capture Example Placeholder

[ IMAGE PLACEHOLDER – CAMERA CAPTURE ]

3. Image Preprocessing

Image resized and cleaned

Prepared for AI inference

4. Object Detection (Human vs Animal)

AI model detects:

Human

Animal

Low-confidence detections are ignored

If human detected → event logged
If animal detected → move to next step

5. Species Classification (Animal Only)

Classifies animal (e.g., Elephant, Deer)

Low-confidence → marked as Unknown

This step is important for:

Species-wise counting

Risk assessment

6. Single-Camera Tracking

Tracks animal within the same camera

Assigns Local Track ID

Prevents double counting within one camera view

🚫 No counting happens here

7. Cross-Camera Association (Global ID)

Assigns a Global Animal ID

Matches animals using:

Species

Time gap

Movement direction

Camera sequence

This allows tracking the same animal across multiple cameras.

8. Re-Entry & De-Duplication Logic

This is the core feature of the system.

An animal is NOT counted again if:

Same Global ID

Appears again within a short time window

Same boundary or corridor

✅ Count again only if:

Long absence (e.g., next day)

New migration cycle

9. Counting Engine

Counts only new Global IDs

Supports:

Unique animal count

Species-wise count

Directional movement

10. Zone-Based Decision Engine

Alerts are generated using rules, not AI guesses.

Examples:

Large animal + boundary + group → High Alert

Animal in corridor → Log only

This avoids false alarms and panic.

11. Alert System

Alerts are sent via:

Dashboard

Notifications / SMS (if enabled)

Only Medium and High risk events trigger alerts.

12. Data Storage & Analytics

All final data is stored for future use.

Stored Information Includes:

Global Animal ID

Species

First seen / Last seen

Camera path

Count status

📊 Used for:

Daily reports

Wildlife movement analysis

System evaluation

Why This System Is Different

✅ No duplicate animal counting
✅ Hardware + AI integrated solution
✅ Power-efficient edge design
✅ Rule-based, explainable decisions
✅ Ready for real-world deployment

Use Cases

Forest boundary monitoring

Village safety systems

Wildlife corridor analysis

Human–animal conflict prevention

Conclusion

This project is not just an AI model —
it is a complete intelligent monitoring system combining:

Hardware sensing

AI vision

Biological logic

Rule-based decisions

It provides accurate counting, meaningful alerts, and real-world reliability.