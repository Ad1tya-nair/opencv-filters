import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=2
)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)

    original = frame.copy()

    h, w, _ = frame.shape

    image_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    results = hands.process(image_rgb)

    left_hand = None
    right_hand = None

    if results.multi_hand_landmarks and results.multi_handedness:

        for i, hand_landmarks in enumerate(
            results.multi_hand_landmarks):
            label = results.multi_handedness[i].classification[0].label

            if label == "Left":
                left_hand = hand_landmarks

            elif label == "Right":
                right_hand = hand_landmarks

        if left_hand and right_hand:

            lindex = left_hand.landmark[8]
            rindex = right_hand.landmark[8]

            lthumb = left_hand.landmark[4]
            rthumb = right_hand.landmark[4]

            x1 = int(lindex.x * w)
            y1 = int(lindex.y * h)

            x2 = int(rindex.x * w)
            y2 = int(rindex.y * h)

            xmin = min(x1, x2)
            xmax = max(x1, x2)

            ymin = min(y1, y2)
            ymax = max(y1, y2)

            w1 = int(lthumb.x * w)
            z1 = int(lthumb.y * h)

            w2 = int(rthumb.x * w)
            z2 = int(rthumb.y * h)

            wmin = min(w1, w2)
            wmax = max(w1, w2)

            zmin = min(z1, z2)
            zmax = max(z1, z2)

            if xmax > xmin and ymax > ymin and wmax > wmin and zmax > zmin:

                gray = cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
                xray = cv2.cvtColor(255 - gray,cv2.COLOR_GRAY2BGR)
                thermal = cv2.applyColorMap(gray,cv2.COLORMAP_COOL)
                xray_gray = cv2.cvtColor(xray,cv2.COLOR_BGR2GRAY)
                xray_thermal = cv2.applyColorMap(xray_gray,cv2.COLORMAP_INFERNO)

                oxmin = max(xmin, wmin)
                oxmax = min(xmax, wmax)
                oymin = max(ymin, zmin)
                oymax = min(ymax, zmax)

                frame[ymin:ymax, xmin:xmax] = \
                    xray[ymin:ymax, xmin:xmax]

                frame[zmin:zmax, wmin:wmax] = \
                    thermal[zmin:zmax, wmin:wmax]

                if oxmax > oxmin and oymax > oymin:

                    frame[oymin:oymax, oxmin:oxmax] = \
                        xray_thermal[oymin:oymax, oxmin:oxmax]

    cv2.imshow("Overlapped",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
hands.close()
cv2.destroyAllWindows()