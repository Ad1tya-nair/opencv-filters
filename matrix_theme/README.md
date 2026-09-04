# Binary Vision Mask

A real-time OpenCV project that uses a webcam to detect bright regions in a video frame and represent those regions using randomly generated binary characters.

The project converts each webcam frame from **BGR to HSV**, creates a brightness-based mask, and overlays randomly generated `0` and `1` characters on the detected regions.

## Features

* Real-time webcam input
* BGR → HSV color-space conversion
* Brightness-based image masking
* Binary `0` / `1` character generation
* Real-time text rendering using OpenCV
* Mirrored camera output
* Configurable camera resolution
* Press `Q` to exit

## How It Works

The processing pipeline is:

```text
Webcam
   ↓
Capture Frame
   ↓
BGR → HSV
   ↓
Brightness Mask
   ↓
Check Mask Pixels
   ↓
Generate Random 0 / 1
   ↓
Draw Characters
   ↓
Flip Horizontally
   ↓
Display
```

### 1. Capture Webcam Frames

OpenCV connects to the default webcam:

```python
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
```

The requested camera resolution is set to 1920 × 1080.

### 2. Convert to HSV

Each frame is converted from BGR to HSV:

```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
```

HSV makes it possible to work with the **Value (V)** channel, which represents brightness.

### 3. Create the Brightness Mask

The project uses:

```python
low = np.array([0, 0, 200])
high = np.array([179, 255, 255])

mask = cv2.inRange(hsv, low, high)
```

This selects pixels with a **Value between 200 and 255**, effectively identifying relatively bright regions.

The resulting mask contains:

```text
255 → selected pixel
0   → ignored pixel
```

### 4. Generate the Binary Representation

A black canvas is created:

```python
black = np.zeros_like(frame)
```

The program then scans the image using a grid:

```python
for y in range(0, h, 10):
    for x in range(0, w, 10):
```

At each grid position, it checks whether that position belongs to the bright region:

```python
if mask[y, x] == 255:
```

If it does, a random binary character is generated:

```python
number = str(np.random.choice(["1", "0"]))
```

The character is then drawn onto the black canvas using `cv2.putText()`.

## Requirements

* Python 3.x
* OpenCV
* NumPy
* A webcam

Install the dependencies with:

```bash
pip install opencv-python numpy
```

## Running the Project

Clone or download the project and run:

```bash
python main.py
```

Make sure your webcam is available.

Press:

```text
Q
```

to quit the application.

## Configuration

### Brightness Threshold

The brightness threshold can be changed here:

```python
low = np.array([0, 0, 200])
high = np.array([179, 255, 255])
```

For example, increasing:

```python
200 → 230
```

will make the mask select only brighter regions.

### Character Density

The spacing of the binary characters can be changed here:

```python
range(0, h, 10)
range(0, w, 10)
```

Smaller values produce a denser character field.

For example:

```python
range(0, h, 5)
range(0, w, 5)
```

creates a much denser representation.

### Character Color

The text color is controlled by the BGR tuple passed to `cv2.putText()`:

```python
(0, 255, 0)
```

For example:

```text
(0, 255, 0)   → Green
(255, 0, 0)   → Blue
(0, 0, 255)   → Red
```

## Controls

| Key | Action |
| --- | ------ |
| `Q` | Quit   |

## Project Structure

```text
binary-vision-mask/
│
├── main.py
└── README.md
```

## Future Improvements

Possible extensions include:

* Multiple layers of characters
* Different characters such as `*`, `#`, `x`, `y`
* Animated colors
* Adjustable brightness threshold
* Adjustable character density
* Smooth color cycling
* Morphological operations to clean the mask
* Contour detection for more accurate subject boundaries
* GUI controls for real-time parameter adjustment

## License

This project is intended for learning and experimentation with OpenCV, image masking, HSV color spaces, and real-time computer vision.
