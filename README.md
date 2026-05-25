# Autonomous Rover: Camera Lane Detection

This repository handles the computer vision logic, track tracking, and steering calculations for our autonomous rover using a single front-mounted camera.

______________________________________________________

THE PROBLEM
______________________________________________________

The main goal is to make the rover drive completely by itself through an outdoor track without crossing the white lines. If any wheel crosses a white boundary, it is an instant disqualification.

In the real world, doing this with standard distance sensors is impossible because of outdoor conditions:
* **Bright Morning Sunlight:** The intense sun creates blinding glare on the track, which oversaturates normal sensors.
* **Deep Geometric Shadows:** Trees and nearby objects cast dark shadows across the track. Normal code can mistake a shadow edge for a lane line, causing a crash.
* **Track Distortions:** Rough asphalt, dirt patches, and dust create visual noise that the robot has to ignore.

______________________________________________________

THE EASIEST WAY TO SOLVE IT (NOT TECHNICALLY)
______________________________________________________

Think of it exactly like a human driving a car on the highway. The driver looks out the windshield to see the white lines on the left and right sides of the lane. 

Your brain automatically calculates the empty space between those lines and knows exactly where the center of the lane is. If the car starts drifting too close to the left line, you naturally see the uneven gap and steer a little bit to the right to stay centered. 

Our camera software does this exact same thing 30 times every single second to keep the wheels locked into the middle of the track.

______________________________________________________

THE WAY I SOLVED IT (TECHNICALLY)
______________________________________________________

We implement a real-time computer vision pipeline using OpenCV to find the lines and a PID controller to smooth out the steering wheel commands.

1. Seeing the Track (OpenCV)
The front camera feeds video into the software. The code filters out the background environment, blocking out the morning sun glare and dark shadows. This leaves only the pure white pixels of the lane boundaries visible to the system.

2. Finding the Lane Center
The software calculates the exact position of both the left white line and the right white line at the same time. It then finds the mathematical center between them.
* **Error Calculation:** The code measures the distance between the camera's center frame and the actual lane center. This distance is called our **Error**.

3. Steering Correction (PID Loop)
The Error value is sent directly to a PID loop which calculates how much to turn the front wheels without causing the rover to shake or spin out:
* **P (Proportional):** Turns the wheels based on the current drift. Small drift = gentle turn; big drift = sharp turn.
* **I (Integral):** Fixes long-term drift. If bumpy ground keeps pulling the rover to one side, this adds extra force over time to pull it back to the absolute center.
* **D (Derivative):** Acts as a steering brake. If the rover turns back toward the center line too quickly, this slows the steering down so it doesn't overshoot the lines.

______________________________________________________

MAIN PARTS OF THE VISION SYSTEM
______________________________________________________

1. Camera Lens
* **Function:** Captures the live physical track environment and transfers the image matrix frames to the processor.

2. Image Filter
* **Function:** Cleans up raw video frames, highlights the white boundaries, and deletes shadows or asphalt noise.

3. Coordinates Calculator
* **Function:** Tracks the pixel positions of the lines to locate the exact center of the path.

4. Steering Controller
* **Function:** Runs the PID formulas to turn the steering servo smoothly.

______________________________________________________

COMMON PROBLEMS AND SOLUTIONS
______________________________________________________

1. Rover Overshoots the Lines
* **Cause:** The steering reaction is too aggressive, or it isn't braking soon enough when returning to the center.
* **Solution:** Lower the Proportional (P) value or increase the Derivative (D) dampening force.

2. Losing Track of the Lines Completely
* **Cause:** Sudden lighting changes or extreme morning glare blinded the camera.
* **Solution:** Adjust the software's white color filter thresholds to match the outdoor sunlight.

3. Rover Drifts or Pulls to One Side
* **Cause:** Mechanical wheel misalignment or uneven floor friction.
* **Solution:** Let the Integral (I) term build up faster to automatically fight off the constant pull.
