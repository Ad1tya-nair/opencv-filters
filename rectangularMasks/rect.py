import cv2
import mediapipe as mp
import numpy as np


def rectanglepoints(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    xmin = min(x1, x2)
    xmax = max(x1, x2)
    ymin = min(y1, y2)
    ymax = max(y1, y2)
    return xmin, ymin, xmax, ymax


def apply_xray(frame, rect):
    xmin, ymin, xmax, ymax = rect
    if xmax > xmin and ymax > ymin:
        roi = frame[ymin:ymax, xmin:xmax]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        roi[:] = cv2.cvtColor(255 - gray, cv2.COLOR_GRAY2BGR)


def apply_thermal(frame, rect):
    xmin, ymin, xmax, ymax = rect
    if xmax > xmin and ymax > ymin:
        roi = frame[ymin:ymax, xmin:xmax]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        roi[:] = cv2.applyColorMap(gray, cv2.COLORMAP_INFERNO)


def apply_twilight(frame, rect):
    xmin, ymin, xmax, ymax = rect
    if xmax > xmin and ymax > ymin:
        roi = frame[ymin:ymax, xmin:xmax]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        roi[:] = cv2.applyColorMap(gray, cv2.COLORMAP_TWILIGHT)


def apply_negative(frame, rect):
    xmin, ymin, xmax, ymax = rect
    if xmax > xmin and ymax > ymin:
        roi = frame[ymin:ymax, xmin:xmax]
        roi[:] = ~roi


def apply_cool(frame, rect):
    xmin, ymin, xmax, ymax = rect
    if xmax > xmin and ymax > ymin:
        roi = frame[ymin:ymax, xmin:xmax]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        roi[:] = cv2.applyColorMap(gray, cv2.COLORMAP_COOL)


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


while cap.isOpened():

    success, frame = cap.read()

    if not success:
        continue

    frame = cv2.flip(frame, 1)

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    left_hand = None
    right_hand = None

    if results.multi_hand_landmarks and results.multi_handedness:

        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            label = results.multi_handedness[i].classification[0].label

            if label == "Left":
                left_hand = hand_landmarks
            elif label == "Right":
                right_hand = hand_landmarks

        if left_hand and right_hand:

            lthumb = left_hand.landmark[4]
            lindex = left_hand.landmark[8]
            lmiddle = left_hand.landmark[12]
            lring = left_hand.landmark[16]
            lpinky = left_hand.landmark[20]

            rthumb = right_hand.landmark[4]
            rindex = right_hand.landmark[8]
            rmiddle = right_hand.landmark[12]
            rring = right_hand.landmark[16]
            rpinky = right_hand.landmark[20]

            ltx, lty = int(lthumb.x * w), int(lthumb.y * h)
            lix, liy = int(lindex.x * w), int(lindex.y * h)
            lmx, lmy = int(lmiddle.x * w), int(lmiddle.y * h)
            lrx, lry = int(lring.x * w), int(lring.y * h)
            lpx, lpy = int(lpinky.x * w), int(lpinky.y * h)

            rtx, rty = int(rthumb.x * w), int(rthumb.y * h)
            rix, riy = int(rindex.x * w), int(rindex.y * h)
            rmx, rmy = int(rmiddle.x * w), int(rmiddle.y * h)
            rrx, rry = int(rring.x * w), int(rring.y * h)
            rpx, rpy = int(rpinky.x * w), int(rpinky.y * h)

            thumb = rectanglepoints((ltx, lty), (rtx, rty))
            index = rectanglepoints((lix, liy), (rix, riy))
            middle = rectanglepoints((lmx, lmy), (rmx, rmy))
            ring = rectanglepoints((lrx, lry), (rrx, rry))
            pinky = rectanglepoints((lpx, lpy), (rpx, rpy))

            apply_xray(frame, thumb)
            apply_thermal(frame, index)
            apply_twilight(frame, middle)
            apply_negative(frame, ring)
            apply_cool(frame, pinky)

    cv2.imshow("Gesture Filters", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
hands.close()
cv2.destroyAllWindows()