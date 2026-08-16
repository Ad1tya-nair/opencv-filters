# Dual-Hand Region Filters

A real-time computer vision project using **Python, OpenCV, and MediaPipe Hands** to apply different image filters to rectangular regions defined by corresponding fingers on two hands.

Unlike the polygon-based version, this implementation uses the position of corresponding fingers on the left and right hands as the two opposite corners of each rectangular Region of Interest (ROI).

## Features

- Real-time webcam processing
- Tracks up to two hands using MediaPipe
- Identifies left and right hands
- Uses corresponding fingers to define five rectangular regions
- Applies a different visual effect to each region
- Keeps each filter in a separate function
- Includes X-ray, thermal, Twilight, negative, and Cool effects
- Uses a reusable rectangle-coordinate helper
- Supports 1920×1080 camera capture
- Press `Q` to exit

## Region and Filter Mapping

| Finger Pair | Filter |
|---|---|
| Left + Right Thumb | X-ray |
| Left + Right Index | Thermal / Inferno |
| Left + Right Middle | Twilight |
| Left + Right Ring | Negative |
| Left + Right Pinky | Cool |

## How It Works

The program detects both hands and extracts the landmarks for the thumb, index, middle, ring, and pinky.

For each finger, the corresponding landmark on the left and right hands becomes the two opposite corners of a rectangle.

```text
Left Finger                    Right Finger
     ●────────────────────────────●
              FILTER ROI
```

The rectangle is generated using:

```python
def rectanglepoints(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    xmin = min(x1, x2)
    xmax = max(x1, x2)

    ymin = min(y1, y2)
    ymax = max(y1, y2)

    return xmin, ymin, xmax, ymax
```

This produces:

```text
(xmin, ymin, xmax, ymax)
```

Using `min()` and `max()` makes the function independent of which point has the smaller coordinates.

## Filter Implementation

Each filter receives the full frame and its rectangle:

```python
apply_xray(frame, thumb)
apply_thermal(frame, index)
apply_twilight(frame, middle)
apply_negative(frame, ring)
apply_cool(frame, pinky)
```

Inside each function, the relevant ROI is extracted:

```python
roi = frame[ymin:ymax, xmin:xmax]
```

The filter then modifies that ROI directly.

### X-ray

```python
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
roi[:] = cv2.cvtColor(
    255 - gray,
    cv2.COLOR_GRAY2BGR
)
```

### Thermal

Uses the Inferno color map:

```python
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
roi[:] = cv2.applyColorMap(
    gray,
    cv2.COLORMAP_INFERNO
)
```

### Twilight

```python
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
roi[:] = cv2.applyColorMap(
    gray,
    cv2.COLORMAP_TWILIGHT
)
```

### Negative

```python
roi[:] = ~roi
```

### Cool

```python
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
roi[:] = cv2.applyColorMap(
    gray,
    cv2.COLORMAP_COOL
)
```

## Why `roi[:]` Is Used

The ROI is obtained as a NumPy slice of the original frame:

```python
roi = frame[ymin:ymax, xmin:xmax]
```

Because this is a view into the original image, assigning to:

```python
roi[:]
```

modifies the corresponding part of `frame` directly.

This allows each filter to update only its selected region.

## ROI Validation

Every filter checks:

```python
if xmax > xmin and ymax > ymin:
```

before processing.

This makes sure the rectangle has a positive width and height and prevents invalid image slices.

## Processing Pipeline

```text
Webcam
   ↓
Capture Frame
   ↓
Mirror Frame
   ↓
Convert BGR → RGB
   ↓
MediaPipe Hand Detection
   ↓
Identify Left + Right Hands
   ↓
Extract Finger Landmarks
   ↓
Convert Normalized Coordinates → Pixel Coordinates
   ↓
Create Five Rectangles
   ↓
Apply Different Filter to Each Rectangle
   ↓
Display Processed Frame
```

## Requirements

```text
Python
OpenCV
MediaPipe
```

Versions used in the project collection:

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

Save the script as:

```text
main.py
```

Run:

```bash
python main.py
```

Press **Q** to exit.

## Camera Configuration

The project uses camera index `0` with Windows DirectShow:

```python
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
```

The requested resolution is:

```text
1920 × 1080
```

For another camera, change the index:

```python
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
```

## MediaPipe Configuration

```python
hands = mp_hands.Hands(
    max_num_hands=2
)
```

The program can therefore detect up to two hands.

Detection and tracking confidence values are not explicitly specified, so MediaPipe uses its default values.

## Project Structure

```text
dual-hand-finger-filters/
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

Both a left and right hand are required before the filters are applied. Ensure both hands are visible and lighting is sufficient.

### Rectangles are unstable

MediaPipe landmarks can move slightly between frames. Better lighting and steadier hand positions can improve stability. Landmark smoothing could also be added.

### Filters appear in unexpected regions

Each rectangle is controlled directly by the positions of its corresponding fingers. Moving those fingers changes the size and location of the ROI.

## Technologies Used

- **Python**
- **OpenCV**
- **MediaPipe**
- **Computer Vision**
- **Hand Landmark Detection**
- **Coordinate Transformation**
- **Region of Interest Processing**
- **Image Filtering**
- **OpenCV Color Maps**
- **Real-Time Video Processing**

## Possible Improvements

- Add landmark smoothing
- Draw rectangle boundaries around each region
- Display filter names
- Add more effects
- Allow filters to be reassigned to different fingers
- Add gesture-based filter switching
- Add transparency and blending
- Add screenshots
- Add video recording
- Add configurable camera resolution
- Add a GUI for filter configuration

## License

This project is intended for educational and experimental use. Add an appropriate open-source license if you plan to distribute the project publicly.
