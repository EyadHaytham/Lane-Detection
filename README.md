# Autonomous Rover: Closed-Loop Motor Speed Control (PID)

This repository contains the low-level firmware, system architecture, and feedback control logic responsible for maintaining precise, synchronized wheel velocities on an autonomous outdoor rover. By utilizing hardware encoder feedback and an aggressive PID tracking loop, the system ensures linear tracking stability and prevents trajectory drift.

---

## 1. SYSTEM OVERVIEW & THE PROBLEM

In autonomous robotics, accurate execution of steering commands requires absolute control over individual wheel velocities. In an unmanaged system, applying a static voltage or duty cycle to DC motors results in unpredictable behavior due to multiple real-world disturbances:

* **Dynamic Surface Friction:** Uneven pavement, gravel, or terrain transitions alter the mechanical load on each wheel independently.
* **Voltage Drop:** As the onboard battery package discharges over time, nominal motor output degrades, causing a systematic drop in maximum available torque and RPM.
* **Mechanical Asymmetry:** Minor manufacturing variances in internal motor gearboxes mean identical power inputs yield completely different physical rotation speeds.

Without real-time correction, these variations introduce devastating heading errors, tracking misalignment, and localized wheel stalls, entirely breaking down the higher-level lane navigation framework.

---

## 2. HIGH-LEVEL ARCHITECTURE (NON-TECHNICAL SUMMARY)

To counter unpredictable environmental forces, the system acts exactly like an industrial cruise control framework. 

When an automobile encounters an incline, gravity introduces physical resistance that naturally degrades vehicle speed. Rather than allowing the car to slow down, the controller detects the speed variance relative to the driver's target setting and automatically injects more fuel to compensate. 

This firmware implements an automated, high-frequency "cruise control" loop for every individual motor channel. The controller continuously samples the true velocity of each wheel and dynamically modulates the output power to forcefully maintain the exact requested speed profile regardless of external resistance.

---

## 3. TECHNICAL IMPLEMENTATION & CONTROL LOGIC

The core of the speed control system relies on a real-time hardware feedback loop structured into three distinct execution stages: Sensor Interfacing, Kinematic Computation, and Error Correction.
