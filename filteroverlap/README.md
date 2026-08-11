# Dual-Hand Overlapping ROI Effects

A real-time computer vision project using **OpenCV** and **MediaPipe Hands** to create two different visual effects controlled by the user's hands.

The **index fingers** define one Region of Interest (ROI), while the **thumbs** define another. An X-ray-style effect is applied to the index-finger ROI, a thermal effect is applied to the thumb ROI, and when the two regions overlap, the overlapping area receives a combined X-ray/thermal effect.

## Features

- Real-time hand tracking using MediaPipe
- Detects up to two hands
- Uses both index fingers to define the X-ray region
- Uses both thumbs to define the thermal region
- Automatically calculates the intersection between the two ROIs
- Applies a third effect to the overlapping region
- Works directly on the webcam feed
- Supports 1920×1080 camera capture
- Uses OpenCV DirectShow on Windows

## How It Works

The project uses four hand landmarks:

- Left index finger → first corner of the X-ray ROI
- Right index finger → second corner of the X-ray ROI
- Left thumb → first corner of the thermal ROI
- Right thumb → second corner of the thermal ROI

### 1. X-ray ROI

The two index fingers define the first rectangle:

```python
xmin = min(x1, x2)
xmax = max(x1, x2)
ymin = min(y1, y2)
ymax = max(y1, y2)
```

This region receives the X-ray effect.

The X-ray effect is created by converting the original frame to grayscale and inverting it:

```python
gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
xray = cv2.cvtColor(255 - gray, cv2.COLOR_GRAY2BGR)
```

### 2. Thermal ROI

The two thumbs define the second rectangle:

```python
wmin = min(w1, w2)
wmax = max(w1, w2)
zmin = min(z1, z2)
zmax = max(z1, z2)
```

A thermal-style color map is then applied:

```python
thermal = cv2.applyColorMap(gray, cv2.COLORMAP_COOL)
```

### 3. Finding the Overlap

The intersection between the two rectangles is calculated using:

```python
oxmin = max(xmin, wmin)
oxmax = min(xmax, wmax)
oymin = max(ymin, zmin)
oymax = min(ymax, zmax)
```

The overlap exists only when:

```python
oxmax > oxmin and oymax > oymin
```

### 4. Overlap Effect

The X-ray image is converted to grayscale and then mapped using the Inferno color map:

```python
xray_gray = cv2.cvtColor(xray, cv2.COLOR_BGR2GRAY)
xray_thermal = cv2.applyColorMap(
    xray_gray,
    cv2.COLORMAP_INFERNO
)
```

This effect is applied only to the intersection of the two ROIs.

## Visual Logic

```text
             INDEX FINGERS
          ┌──────────────────┐
          │                  │
          │      FILTER 1    │
          │        ┌─────────┼───────┐
          │        │ OVERLAP │       │
          └────────┼─────────┘       │
                   │    FILTER 2     │
                   └─────────────────┘
                       THUMBS
```

In simple terms:

```text
Index ROI       → X-ray
Thumb ROI       → Thermal
Index ∩ Thumb   → X-ray + Inferno effect
```

## Requirements

The project uses:

```text
MediaPipe: 0.10.14
OpenCV:    5.0.0.93
```

## Installation

```bash
python -m pip install mediapipe==0.10.14 opencv-python==5.0.0.93
```

Verify the installations:

```bash
python -m pip show mediapipe
python -m pip show opencv-python
```

## Running the Project

Save the Python file as:

```text
main.py
```

Then run:

```bash
python main.py
```

The webcam window will open.

Press **Q** to exit.

## Camera Configuration

The program uses camera index `0` with Windows DirectShow:

```python
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
```

It requests a resolution of:

```text
1920 × 1080
```

If you have multiple cameras, change the camera index as needed.

## MediaPipe Configuration

MediaPipe Hands is initialized with:

```python
hands = mp_hands.Hands(
    max_num_hands=2
)
```

The program therefore attempts to track up to two hands.

`min_detection_confidence` and `min_tracking_confidence` are not explicitly specified, so MediaPipe uses its default values.

## ROI Safety Checks

Before applying effects, the program verifies that both rectangles have a valid width and height:

```python
if xmax > xmin and ymax > ymin and    wmax > wmin and zmax > zmin:
```

The overlap is separately checked:

```python
if oxmax > oxmin and oymax > oymin:
```

This prevents invalid or empty image slices from being processed.

## Project Structure

```text
dual-hand-roi-effects/
│
├── main.py
└── README.md
```

## Troubleshooting

### Camera does not open

Try another camera index:

```python
cv2.VideoCapture(1, cv2.CAP_DSHOW)
```

Also make sure another application is not using the webcam.

### Only one hand is detected

Make sure both hands are visible and there is sufficient lighting. The program requires both a left and right hand before creating the ROIs.

### Effects do not appear

Both index fingers and both thumbs need to be detected. The corresponding points must also form valid rectangles.

### The overlap effect does not appear

The two rectangles must actually intersect. The intersection is valid only when:

```python
oxmax > oxmin
```

and:

```python
oymax > oymin
```

## Technologies Used

- **Python**
- **OpenCV**
- **MediaPipe**
- **Computer Vision**
- **Hand Landmark Detection**
- **Region of Interest (ROI) Processing**
- **Image Color Mapping**
- **Real-time Image Processing**

## Possible Improvements

- Draw visible boundaries around both ROIs
- Display `X-RAY`, `THERMAL`, and `OVERLAP` labels
- Add more visual effects
- Smooth hand landmark coordinates to reduce ROI jitter
- Add gesture controls
- Add video recording
- Allow screenshots
- Add configurable camera resolution
- Add a GUI for effect selection
- Support a one-hand mode

## License

This project is intended for educational and experimental use. Add an appropriate open-source license if you plan to distribute the project publicly.
