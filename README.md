# LANE-DETECTION

Computer Vision Lane Detection & Trajectory Tracking (OpenCV + PID)

## Highlights:
* **Real-time Lane Tracking:** Process live video frames instantly at 30+ frames per second.
* **Sunlight & Shadow Resistance:** Advanced filtering prevents blinding glare and harsh outdoor shadows from ruining your path.
* **Smooth Autonomous Steering:** Uses mathematical PID calculations to eliminate aggressive shaking and tire spinouts.
* **Approachable Structure:** Built so that any first-year engineering student can easily install, read, and understand the code logic.

## Overview:
This repository contains the computer vision pipeline and real-time tracking scripts used to keep an autonomous outdoor rover perfectly centered within a defined track using a single front-mounted camera sensor. 

### ⚠️ The Problem:
The main goal is to make the rover drive completely by itself through an outdoor track without crossing the white lines. If any wheel crosses a white boundary, it is an instant disqualification. 

In the real world, doing this with standard distance sensors is impossible because of intense, unpredictable outdoor conditions:
* **Bright Morning Sunlight:** The intense sun creates blinding glare on the track, which oversaturates normal sensors.
* **Track Distortions:** Rough asphalt, dirt patches, and dust create visual noise that the robot has to ignore.

### 💡 The Solution (Non-Technical Summary)
Think of it exactly like a human driving a car on the highway. The driver looks out the windshield to see the white lines on the left and right sides of the lane. 

Your brain automatically calculates the empty space between those lines and knows exactly where the center of the lane is. If the car starts drifting too close to the left line, you naturally see the uneven gap and steer a little bit to the right to stay centered. 

Our camera software does this exact same thing 30 times every single second to keep the wheels locked into the middle of the track.

---

## 🛠️ V1 Architecture (Line Tracing Methods)

We implement a real-time computer vision pipeline using OpenCV to find the lines and a PID controller to smooth out the steering wheel commands.

### 1. Seeing the Track (OpenCV)
The system captures raw frames from the video stream. It processes the visual input using a Gaussian blur filter to eliminate high-frequency noise from rough asphalt textures, followed by a Canny edge detection transformation to map out high-contrast transitions. A tailored triangular Region of Interest (ROI) mask isolates the track directly ahead while deleting extraneous background objects.

### 2. Finding the Lane Center
Using a Progressive Probabilistic Hough Line Transform (`cv2.HoughLinesP`), the code calculates vectors for structural segments along the track boundaries. These segments are evaluated by their mathematical slopes and intercepts, separating them into distinct left and right lane boundaries.
* **Error Calculation:** The software computes the absolute midpoint between the boundaries ($X_{lane\_center}$) and measures its distance deviation from the camera lens's true physical center ($X_{camera\_center}$). This numerical pixel gap forms our **Error** metric.

### 3. Steering Correction (PID Loop)
The computed spatial Error string feeds continuously into a localized PID controller to dynamically regulate steering geometry without losing stability:
* **P (Proportional):** Turns the wheels proportionally based on immediate drift magnitude (minor drift = soft correction; major drift = sharp turn).
* **I (Integral):** Aggregates residual tracking errors over time to neutralize systemic pulls caused by uneven floor friction or chassis weight imbalances.
* **D (Derivative):** Computes the instantaneous velocity of recovery to introduce a predictive dampening force, preventing steering overshoots and vehicle spinouts.

---

## 🚀 V2 Upgrade: High-Precision Geometric Tracking

We completely overhauled the core vision system in our latest update! We dropped the old linear line-tracer (`Canny` + `Hough Lines`) because it was getting tripped up by floor patterns, wrinkles, and track boundaries splitting apart. The new V2 system uses a powerful **color-isolation filter** that places **rock-solid green bounding boxes** around target lanes for perfect tracking accuracy.

### 📸 System Demonstration
<img width="1270" height="715" alt="Screenshot 2026-06-14 065144" src="https://github.com/user-attachments/assets/4d59daf7-3aca-46f5-a9f7-98d5ae9a98d3" />
<img width="215" height="335" alt="Screenshot 2026-06-14 073525" src="https://github.com/user-attachments/assets/af9510be-b3b5-4fab-90fd-3490712904ee" />




### Key V2 Improvements:
* **Anti-Texture Filtering:** Locks onto bright white targets instantly while completely ignoring carpet patterns, dark room shadows, and overhead light glare.
* **Super-Steady Target Boxes:** Drops clean geometric boxes over objects to track their exact mathematical centers without shaking.
* **Smart Off-Screen Fallback:** If a target goes completely off-camera during a sharp turn, the code automatically fills in the blank side with a safe guess (calibrated 23% screen-width offset placeholder) to keep the robot moving smoothly.
* **Live Terminal Data Stream:** Outputs raw tracking numbers frame-by-frame, making it incredibly easy to connect directly to robot steering motors.

### How V2 Processes Data:
1. **Isolating the Targets (HSV Color Space):** The camera grabs live frames and converts them to the HSV color space to scan for raw brightness values. It blocks out everything that isn't pure white, then uses a cleaning filter (Morphological Opening & Closing) to erase tiny carpet specks and glue wrinkled paper shadows back into single solid shapes.
2. **Finding the Center:** The code tracks the outer shapes of the white targets and draws a tightly fitted green bounding box around them. The software finds the middle point between the left and right green boxes and measures its distance from the absolute center of your camera frame. This pixel distance is your new **PID Error**.
3. **Steering Correction:** The live error number is printed directly to the terminal console screen frame-by-frame. If the robot drifts past a 20% safe zone, a `[CRITICAL]` alert flashes on the screen to warn that it's going out of bounds.

---

## ⚙️ Installation Instructions

This project runs beautifully on **Windows 10/11** or **Linux (Ubuntu)** with Python 3.

Open your terminal or command prompt and run the following command to install the required libraries:

```bash
pip install opencv-python numpy
