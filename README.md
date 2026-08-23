## FMCW Radar
This project is a 2.4 GHz Frequency Modulated Continuous Wave (FMCW) radar system designed for 2D terrain mapping and object tracking. The mechanical assembly features full 360-degree pan rotation and $\pm 90^\circ$ tilt articulation. 

The system is split into two specialized printed circuit boards (PCBs) and utilizes dual patch antennas: one for transmitting via a 3D-printed, aluminum-lined convex horn to maximize range, and one for receiving weak deflected echo signals.

## Why I Built It
Built purely for engineering passion coolness, this project helped me learn radar principles, high-frequency RF routing, embedded multitasking, and mechanical CAD design.

---

## PCB 1: RF Front-End
### Schematic
![RF Schematic](pics/sc1.png)

### PCB Layout
![RF PCB Layout](pics/pc1.png)

### 3D Render
![RF 3D Render](pics/3d1.png)

---

## PCB 2: Baseband Signal Processing
### Schematic
![Baseband Schematic](pics/sc2.png)

### PCB Layout
![Baseband PCB Layout](pics/pc2.png)

### 3D Render
![Baseband 3D Render](pics/3d2.png)

### Microcontroller (MCU)
The system is powered by an **ESP32** microcontroller, chosen for its dual-core architecture (ideal for handling parallel DSP routines and motor control tasks) and 240 MHz clock speed.

---

## Mechanical CAD Design
![Full Assembly](pics/frontass.png)

The gimbal is engineered for structural rigidity with zero mechanical play, featuring a dual-bearing aluminum support assembly secured with precision hardware.

![Gimbal Detail 1](pics/r1.png)
![Gimbal Detail 2](pics/r2.png)

---

## Ground Control Station (GCS)
Built using Python and PyQt6, i made it so that its cooler than what you see in the movie 

![Ground Control Station Interface](pics/image-42.png)

---

## Bill of Materials (BOM)

| Component | Qty | Price |
| :--- | :---: | :--- |
| pcb1 | 5 | $42.00 |
| pcb2 | 5 | $57.00 |
| esp32 | 1 | $2.00 |
| servo | 1 | $3.70 |
| 1kg spool pla | 1 | $20.00 |
| bearing | 4 | $2.00 |
| screws | 100 | $10.00 |
| nuts | 20 | $2.00 |
| headers | 20 | $5.00 |
| belt | 1 | $13.12 |
| sma connectors | 5 | $5.40 |
| **Total** | | **$162.22** |
