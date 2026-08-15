# Computer Vision Projects

A collection of small **Computer Vision projects built with Python, OpenCV, MediaPipe, and NumPy**.

This repository documents my learning and experimentation with real-time image processing, hand tracking, gesture recognition, region-based effects, and webcam-based computer vision.

## About

The projects in this repository primarily use a webcam as a real-time input and manipulate the video based on detected hand landmarks and user gestures.

Rather than being one large application, this repository is a collection of progressively more involved experiments. Each project explores a different computer vision concept and has its own README explaining the implementation.

## Technologies Used

- **Python** — Core programming language
- **OpenCV** — Image and video processing
- **MediaPipe** — Hand landmark detection and tracking
- **NumPy** — Numerical operations and image manipulation

## Projects

### 1. Gesture-Controlled Filter

A real-time filter system where two index fingers define a rectangular Region of Interest.

A pinch gesture using the left thumb and index finger switches between different visual effects.

**Concepts explored:**

- Hand landmark detection
- Gesture recognition
- Pinch detection
- ROI processing
- OpenCV color maps
- Pixel manipulation

### 2. Dual-Hand Overlapping ROI Effects

Uses both hands to define two separate regions.

The **index fingers** define an X-ray region while the **thumbs** define a thermal region. When the two regions overlap, a third effect is applied to the intersection.

**Concepts explored:**

- Multiple hand tracking
- ROI geometry
- Rectangle intersection
- Image masks
- Layered image effects

### 3. Multi-Region Filters

Uses corresponding fingers on both hands to create multiple polygonal regions.

Different regions receive different effects:

| Region | Effect |
|---|---|
| Thumb | X-ray |
| Index | Cool |
| Middle | Negative |
| Ring | Twilight |
| Pinky | Reserved for future effect |

**Concepts explored:**

- Hand landmarks
- Polygon construction
- OpenCV masking
- Region-based image processing
- Multiple simultaneous effects

## Repository Structure

```text
computer-vision-projects/
│
├── README.md
│
├── gesture-filter/
│   ├── main.py
│   └── README.md
│
├── dual-hand-roi-effects/
│   ├── main.py
│   └── README.md
│
└── gesture-multi-region-filters/
    ├── main.py
    └── README.md
```

Each project contains its own `README.md` with details about how it works, installation, usage, troubleshooting, and possible improvements.

## Common Requirements

The projects generally use:

```text
Python
OpenCV
MediaPipe
NumPy
```

The versions currently used include:

```text
MediaPipe: 0.10.14
OpenCV:    5.0.0.93
```

Individual projects may have slightly different dependencies depending on what they implement.

## Learning Goals

Through these projects, I'm exploring:

- Real-time computer vision
- Webcam processing
- Hand landmark detection
- Gesture recognition
- Coordinate systems
- Region of Interest (ROI) manipulation
- Image filtering
- Color maps
- Image masking
- Polygon geometry
- Pixel-level image manipulation
- Combining computer vision with interactive controls

## Future Projects

This repository will continue to grow as I experiment with more computer vision concepts, including:

- Object detection
- Face and pose tracking
- More gesture-controlled applications
- Interactive computer vision games
- Image segmentation
- Real-time augmented effects
- AI-based vision applications

## Purpose

The main purpose of this repository is to **learn by building**.

Each project starts with a specific computer vision concept and builds on techniques explored in previous projects. The code may not always represent production-ready implementations; instead, the focus is on understanding how the underlying computer vision techniques work and experimenting with them in practical applications.

---

**Built with Python + OpenCV + MediaPipe.**
