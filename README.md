# LANE-DETECTION

Computer Vision Lane Detection & Trajectory Tracking (OpenCV + PID)
🌟 Highlights

* **Real-time Lane Tracking:** Process live video frames instantly at 30+ frames per second.
* **Sunlight & Shadow Resistance:** Advanced filtering prevents blinding glare and harsh outdoor shadows from ruining your path.
* **Smooth Autonomous Steering:** Uses mathematical PID calculations to eliminate aggressive shaking and tire spinouts.
* **Pure Visual Navigation:** Achieves true track centering using a single front camera without relying on external GPS trackers or manual controls.
* **Approachable Structure:** Built so that any first-year engineering student can easily install, read, and understand the code logic.

ℹ️ Overview

This repository contains the advanced computer vision pipeline and real-time trajectory tracking scripts used to keep an autonomous outdoor rover perfectly centered within a defined track using a single front-mounted camera sensor. 

The goal of this documentation is to convey the quality of the work, explain the engineering decisions behind the design, and make the codebase highly approachable for developers, student engineers, and reviewers looking at the system architecture.

📋 Problem Statement

### ⚠️ The Problem
The main goal is to make the rover drive completely by itself through an outdoor track without crossing the white lines. If any wheel crosses a white boundary, it is an instant disqualification. 

In the real world, doing this with standard distance sensors is impossible because of intense, unpredictable outdoor conditions:
* **Bright Morning Sunlight:** The intense sun creates blinding glare on the track, which oversaturates normal sensors.
* **Deep Geometric Shadows:** Trees and nearby objects cast dark shadows across the track. Normal code can mistake a shadow edge for a lane line, causing a crash.
* **Track Distortions:** Rough asphalt, dirt patches, and dust create visual noise that the robot has to ignore.

😊 The Solution (Non-Technical Summary)

Think of it exactly like a human driving a car on the highway. The driver looks out the windshield to see the white lines on the left and right sides of the lane. 

Your brain automatically calculates the empty space between those lines and knows exactly where the center of the lane is. If the car starts drifting too close to the left line, you naturally see the uneven gap and steer a little bit to the right to stay centered. 

Our camera software does this exact same thing 30 times every single second to keep the wheels locked into the middle of the track.

🛠️ The Technical Steps

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

🚀 Usage Instructions

To run the pipeline and view real-time boundary tracing alongside computed error outputs, execute the central module script:

```python
import cv2
import lane_detector as ld

# Open camera interface capture channel
cap = cv2.VideoCapture(1)

# Stream live frame matrices through the tracking pipeline
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break    
    edges = ld.canny_edge(frame)
    roi = ld.region_of_interest(edges)
    # Pipeline isolates vectors, calculates center error, and overlays graphic

```

⬇️ Installation Instructions

This framework requires Ubuntu 20.04 (Linux) or Windows 10/11 (64-bit) with Python 3 and OpenCV 4 bindings.

Open a terminal and run the following setup commands to update your package manager and map core imaging dependencies:

Bash
sudo apt-get update
sudo apt install python3-opencv python3-numpy python3-matplotlib

