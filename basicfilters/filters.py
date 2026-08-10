import cv2
import mediapipe as mp
import math
import numpy as np
# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5
)

#available effects and filters stored in an array
filters = [
    "inferno",
    "jet",
    "cool",
    "pixelate",
    "negative",
    "neon",
    "parula",
    "glitch",
    "twilight"
]

current_filter = 0
pinching = False

#camera output window
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)   # Property ID 3
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # Property ID 4

while cap.isOpened():

    success, frame = cap.read()

    if not success:
        continue

    frame = cv2.flip(frame, 1)

    h, w, _ = frame.shape

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(image_rgb)

    left_hand = None
    right_hand = None

    if results.multi_hand_landmarks and results.multi_handedness:

        # Identify left and right hands
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):

            label = results.multi_handedness[i].classification[0].label

            if label == "Left":
                left_hand = hand_landmarks

            else:
                right_hand = hand_landmarks

        if left_hand and right_hand:

            # Left hand
            lindex = left_hand.landmark[8]
            lthumb = left_hand.landmark[4]

            # Right hand
            rindex = right_hand.landmark[8]

            # Left index coordinates
            lx = int(lindex.x * w)
            ly = int(lindex.y * h)

            # Right index coordinates
            rx = int(rindex.x * w)
            ry = int(rindex.y * h)

            # Left thumb coordinates
            tx = int(lthumb.x * w)
            ty = int(lthumb.y * h)


            # Distance between LEFT thumb and LEFT index
            distance = math.hypot(lx - tx, ly - ty)
            #text = f"{distance:.2f} px"
            #cv2.putText(frame, text, (lx,ly), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

            # Toggle once per pinch
            if distance < 35:
              if not pinching:
                current_filter = (current_filter + 1) % len(filters)
                pinching = True
            else:
              pinching = False

            # Rectangle between the two index fingers
            xmin = min(lx, rx)
            xmax = max(lx, rx)
            ymin = min(ly, ry)
            ymax = max(ly, ry)

            # Make sure ROI is not empty
            if xmax > xmin and ymax > ymin:
              roi = frame[ymin:ymax, xmin:xmax]

              filter_name = filters[current_filter]

              if filter_name == "jet":
                  gray = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
                  roi[:] = cv2.applyColorMap(gray,cv2.COLORMAP_JET)

              elif filter_name == "cool":
                  gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                  roi[:] = cv2.applyColorMap(gray, cv2.COLORMAP_COOL)

              elif filter_name == "pixelate":
                  small = cv2.resize(roi,(20,20))
                  roi[:] = cv2.resize(small,(roi.shape[1],roi.shape[0]),
                    interpolation=cv2.INTER_NEAREST)
                  
              elif filter_name == "negative":
                  roi[:] = ~roi

              elif filter_name == "neon":
                  gray = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
                  edges = cv2.Canny(gray,100,200)
                  roi[:] = 0
                  roi[:,:,1] = edges

              elif filter_name == "parula":
                  gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                  roi[:] = cv2.applyColorMap(gray, cv2.COLORMAP_PARULA)

              elif filter_name=="inferno":
                  gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                  roi[:] = cv2.applyColorMap(gray, cv2.COLORMAP_SPRING)

              elif filter_name=="twilight":
                  gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                  roi[:] = cv2.applyColorMap(gray, cv2.COLORMAP_TWILIGHT)

              elif filter_name == "glitch":
                  b, g, r = cv2.split(roi)
                  b = np.roll(b, 30, axis=0)
                  g = np.roll(g, -15, axis=1)
                  r = np.roll(r, -30, axis=0)
                  roi[:] = cv2.merge((b, g, r))
    #cv2.putText(frame, filters[current_filter], (15,15), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
    cv2.imshow("Gesture Toggle", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
hands.close()
cv2.destroyAllWindows()