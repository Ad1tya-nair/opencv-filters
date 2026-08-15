# Gesture-Controlled Multi-Region Filters

A real-time computer vision project using **OpenCV**, **MediaPipe Hands**, and **NumPy** to create multiple polygonal regions between two hands and apply a different visual effect to each region.

## Features

- Real-time hand tracking using MediaPipe
- Supports up to two hands
- Uses corresponding finger landmarks to create polygonal regions
- Applies different filters to different regions
- Uses OpenCV masks for region-specific processing
- Supports 1920×1080 webcam capture
- Includes X-ray, Cool, Negative, and Twilight effects
- Real-time webcam processing

## How It Works

The program detects the left and right hands and extracts the landmarks for the thumb, index, middle, ring, and pinky fingers.

Adjacent fingers on the two hands are connected to form polygonal regions:

```text
Thumb  → Index
Index  → Middle
Middle → Ring
Ring   → Pinky
Pinky  → Thumb
```

Each polygon is converted into a mask, and a filter is applied only to the pixels inside that mask.

## Region and Filter Mapping

| Region | Filter |
|---|---|
| Thumb region | X-ray |
| Index region | Cool |
| Middle region | Negative |
| Ring region | Twilight |
| Pinky region | Not currently filtered |

### X-ray

The frame is converted to grayscale and inverted:

```python
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
xray = cv2.cvtColor(255 - gray, cv2.COLOR_GRAY2BGR)
```

### Cool

```python
cool = cv2.applyColorMap(
    gray,
    cv2.COLORMAP_COOL
)
```

### Negative

```python
negative = ~frame
```

### Twilight

```python
twilight = cv2.applyColorMap(
    gray,
    cv2.COLORMAP_TWILIGHT
)
```

## Polygon Construction

For example, the thumb region is formed using:

```python
thumb_points = np.array([
    [ltx, lty],
    [rtx, rty],
    [rix, riy],
    [lix, liy]
])
```

This connects the left thumb, right thumb, right index, and left index to create a quadrilateral.

The same idea is used for the remaining finger pairs.

## Masking

Each polygon is converted into a binary mask:

```python
thumb_mask = np.zeros((h, w), dtype=np.uint8)

cv2.fillPoly(
    thumb_mask,
    [thumb_points],
    255
)
```

The filtered image is then copied into the masked region:

```python
frame[thumb_mask == 255] = xray[thumb_mask == 255]
```

This means the filter affects only the selected polygon rather than the entire camera frame.

## Processing Pipeline

```text
Webcam
   ↓
Capture Frame
   ↓
Flip Horizontally
   ↓
MediaPipe Hand Detection
   ↓
Identify Left + Right Hands
   ↓
Extract Finger Landmarks
   ↓
Convert Landmarks to Pixel Coordinates
   ↓
Create Polygon Regions
   ↓
Generate Filtered Images
   ↓
Create Masks
   ↓
Apply Filters
   ↓
Display Result
```

## Requirements

```text
Python
OpenCV
MediaPipe
NumPy
```

Versions used:

```text
MediaPipe: 0.10.14
OpenCV:    5.0.0.93
```

## Installation

```bash
python -m pip install mediapipe==0.10.14 opencv-python==5.0.0.93 numpy
```

Verify the packages:

```bash
python -m pip show mediapipe
python -m pip show opencv-python
python -m pip show numpy
```

## Running the Project

Save the program as:

```text
main.py
```

Run:

```bash
python main.py
```

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

If another camera is required, change the index:

```python
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
```

## MediaPipe Configuration

```python
hands = mp_hands.Hands(
    max_num_hands=2
)
```

The program can therefore track up to two hands.

Detection and tracking confidence values are not explicitly specified, so MediaPipe uses its defaults.

## Project Structure

```text
gesture-multi-region-filters/
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

Both hands need to be visible for the regions to be created. Improve lighting and keep both hands inside the camera frame.

### Regions are unstable

Hand landmarks naturally move slightly between frames. Better lighting and keeping the hands steady can help. Landmark smoothing could also be added later.

### A filter does not appear

The corresponding left and right hand landmarks must be detected before the polygon is created.

## Technologies Used

- **Python**
- **OpenCV**
- **MediaPipe**
- **NumPy**
- **Computer Vision**
- **Hand Landmark Detection**
- **Polygon Masking**
- **Region-Based Image Processing**
- **Real-Time Image Processing**

## Possible Improvements

- Add a filter to the pinky region
- Draw outlines around the polygons
- Display filter names
- Add more effects
- Add gesture-controlled filter selection
- Smooth hand landmark coordinates
- Allow customizable filter assignments
- Add transparency/blending
- Add screenshot and video recording
- Add a GUI for filter configuration

## License

This project is intended for educational and experimental use. Add an appropriate open-source license if you plan to distribute the project publicly.
