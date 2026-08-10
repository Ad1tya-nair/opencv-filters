# Gesture-Controlled ROI Filter

A real-time computer vision project that uses **MediaPipe Hands** and
**OpenCV** to detect two hands, create a rectangular Region of Interest
(ROI) between the two index fingers, and apply different visual effects
to that region.

The active filter can be changed by making a **pinching gesture with the
left thumb and left index finger**.

## Features

-   Real-time hand tracking using MediaPipe
-   Supports detection of up to two hands
-   Uses the two index fingers to define a rectangular ROI
-   Left thumb + index finger pinch gesture changes the active filter
-   Each pinch advances to the next filter
-   Multiple image effects and color maps
-   1920×1080 camera capture configuration
-   OpenCV camera support using Windows DirectShow

## How It Works

1.  The webcam captures a frame.
2.  The frame is flipped horizontally to create a mirror-like view.
3.  MediaPipe detects up to two hands and their landmarks.
4.  The program identifies the left and right hands.
5.  The **index fingers** of both hands are used as the two corners of
    the ROI.
6.  The **left thumb and left index finger** are used to detect a pinch.
7.  When a pinch is detected, the program switches to the next filter.
8.  The selected filter is applied only inside the rectangle between the
    two index fingers.
9.  Press `Q` to exit.

### ROI Concept

If the two index fingers are at:

-   Left index → `(lx, ly)`
-   Right index → `(rx, ry)`

the rectangle is calculated using:

``` text
xmin = min(lx, rx)
xmax = max(lx, rx)
ymin = min(ly, ry)
ymax = max(ly, ry)
```

The resulting region is:

``` python
roi = frame[ymin:ymax, xmin:xmax]
```

The filter modifies this ROI directly, so the rest of the camera frame
remains unchanged.

## Available Filters

The filters are stored in the following order:

1.  **Inferno** -- currently implemented using OpenCV's
    `COLORMAP_SPRING`
2.  **Jet** -- applies the JET color map
3.  **Cool** -- applies the COOL color map
4.  **Pixelate** -- reduces the ROI to a small image and enlarges it
    using nearest-neighbor interpolation
5.  **Negative** -- inverts the colors
6.  **Neon** -- detects edges and displays them as a bright green effect
7.  **Parula** -- applies the PARULA color map
8.  **Glitch** -- shifts the blue, green, and red channels independently
9.  **Twilight** -- applies the TWILIGHT color map

After the ninth filter, another pinch cycles back to the first filter.

## Gesture Controls

  Gesture                         Action
  ------------------------------- -----------------------
  Left thumb + left index pinch   Switch to next filter
  Release pinch                   Reset the pinch state
  `Q`                             Quit the application

The program uses a `pinching` state so that holding the fingers together
does **not** continuously cycle through filters. A new filter is
selected only after a new pinch.

## Requirements

### Python

The project requires Python with the following packages:

``` text
mediapipe==0.10.14
opencv-python==5.0.0.93
numpy
```

The versions currently used for this project are:

``` text
MediaPipe: 0.10.14
OpenCV:    5.0.0.93
```

NumPy is used for the glitch effect.

## Installation

Clone or download the project, then install the dependencies:

``` bash
python -m pip install mediapipe==0.10.14 opencv-python==5.0.0.93 numpy
```

You can verify the installed packages with:

``` bash
python -m pip show mediapipe
python -m pip show opencv-python
python -m pip show numpy
```

## Running the Project

Save the Python program as something such as:

``` text
gesture_filter.py
```

Then run:

``` bash
python gesture_filter.py
```

The webcam window should open automatically.

Press:

``` text
Q
```

to close the application.

## Camera Configuration

The program opens camera index `0` using Windows DirectShow:

``` python
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
```

It then requests a resolution of:

``` text
1920 × 1080
```

If the camera does not support this resolution, OpenCV may use a
different supported resolution depending on the camera and driver.

If another camera is being used, change:

``` python
cv2.VideoCapture(0, cv2.CAP_DSHOW)
```

to the appropriate camera index.

## Hand Detection Settings

MediaPipe Hands is initialized with:

``` python
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5
)
```

This means:

-   At most **2 hands** are detected.
-   The minimum hand detection confidence is **0.5**.
-   The tracking confidence is not explicitly specified in the current
    code, so MediaPipe uses its default value.

## Pinch Detection

The program calculates the pixel distance between the left thumb and
left index finger:

``` python
distance = math.hypot(lx - tx, ly - ty)
```

A pinch is considered detected when:

``` python
distance < 35
```

The value `35` is a pixel-based threshold and may need adjustment
depending on:

-   Camera resolution
-   Distance from the camera
-   Hand position
-   Camera field of view

## Project Structure

A simple project structure can be:

``` text
gesture-filter/
│
├── gesture_filter.py
└── README.md
```

## Troubleshooting

### Camera does not open

Try changing the camera index:

``` python
cv2.VideoCapture(1, cv2.CAP_DSHOW)
```

or:

``` python
cv2.VideoCapture(2, cv2.CAP_DSHOW)
```

Also make sure another application is not currently using the webcam.

### Hand detection is unreliable

Try improving lighting and keeping both hands clearly visible.

You can also experiment with:

``` python
min_detection_confidence=0.5
```

A higher value can make detection stricter, while a lower value can make
it more tolerant.

### Pinch does not switch filters

The pinch threshold is currently:

``` python
distance < 35
```

Try adjusting this value if the gesture is difficult to trigger.

For example:

``` python
if distance < 45:
```

The best threshold depends on the camera resolution and how close the
hands are to the camera.

### ROI does not appear

The ROI is created only when:

``` python
xmax > xmin and ymax > ymin
```

Make sure both index fingers are visible and positioned so that they
form a valid rectangle.

## Technologies Used

-   **Python**
-   **OpenCV**
-   **MediaPipe**
-   **NumPy**
-   **Computer Vision**
-   **Hand Landmark Detection**
-   **Real-time Image Processing**

## Future Improvements

Possible improvements include:

-   Displaying the current filter name on screen
-   Drawing the ROI boundary
-   Adding more filters
-   Using a more robust pinch-distance calculation
-   Adding smoothing to hand landmark positions
-   Adding keyboard controls for filter selection
-   Supporting one-hand ROI selection
-   Adding a graphical user interface
-   Saving filtered frames or recording the processed video
-   Adding configurable camera resolution and gesture thresholds

## License

This project is intended for educational and experimental use. Add an
appropriate license if you plan to distribute or publish the project.
