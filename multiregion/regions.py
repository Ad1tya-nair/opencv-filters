import cv2
import mediapipe as mp
import numpy as np

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

    # Mirror image
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
            
            #left hand landmarks
            lthumb  = left_hand.landmark[4]
            lindex  = left_hand.landmark[8]
            lmiddle = left_hand.landmark[12]
            lring   = left_hand.landmark[16]
            lpinky  = left_hand.landmark[20]

            # Right hand landmarks
            rthumb  = right_hand.landmark[4]
            rindex  = right_hand.landmark[8]
            rmiddle = right_hand.landmark[12]
            rring   = right_hand.landmark[16]
            rpinky  = right_hand.landmark[20]

            #left hand coordinates
            ltx = int(lthumb.x * w)
            lty = int(lthumb.y * h)
            lix = int(lindex.x * w)
            liy = int(lindex.y * h)
            lmx = int(lmiddle.x * w)
            lmy = int(lmiddle.y * h)
            lrx = int(lring.x * w)
            lry = int(lring.y * h)
            lpx = int(lpinky.x * w)
            lpy = int(lpinky.y * h)

            # Right hand coordinates
            rtx = int(rthumb.x * w)
            rty = int(rthumb.y * h)
            rix = int(rindex.x * w)
            riy = int(rindex.y * h)
            rmx = int(rmiddle.x * w)
            rmy = int(rmiddle.y * h)
            rrx = int(rring.x * w)
            rry = int(rring.y * h)
            rpx = int(rpinky.x * w)
            rpy = int(rpinky.y * h)

            #polygons
            #thumbs
            thumb_points = np.array([
                [ltx, lty],
                [rtx, rty],
                [rix, riy],
                [lix, liy]
            ])

            #index
            index_points = np.array([
                [lix, liy],
                [rix, riy],
                [rmx, rmy],
                [lmx, lmy]
            ])

            #middle
            middle_points = np.array([
                [lmx, lmy],
                [rmx, rmy],
                [rrx, rry],
                [lrx, lry]
            ])

            #ring
            ring_points = np.array([
                [lrx, lry],
                [rrx, rry],
                [rpx, rpy],
                [lpx, lpy]
            ])  

            #pinky
            pinky_points = np.array([
                [lpx, lpy],
                [rpx, rpy],
                [rtx, rty],
                [ltx, lty]
            ])


            #filtering functions
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

            #xray filter
            xray=cv2.cvtColor(255-gray,cv2.COLOR_GRAY2BGR)

            #thermal
            thermal=cv2.applyColorMap(gray,cv2.COLORMAP_INFERNO)

            #twilight
            twilight=cv2.applyColorMap(gray,cv2.COLORMAP_TWILIGHT)

            # Glitch
            b, g, r = cv2.split(frame)
            b = np.roll(b, 25, axis=1)
            g = np.roll(g, -20, axis=0)
            r = np.roll(r, -25, axis=1)
            glitch = cv2.merge((b, g, r))

            #negative
            negative=~frame

            #cool
            cool=cv2.applyColorMap(gray,cv2.COLORMAP_COOL)


            #masking
            #thumb
            thumb_mask=np.zeros((h,w),dtype=np.uint8)
            cv2.fillPoly(thumb_mask,[thumb_points],255)
            frame[thumb_mask==255]=xray[thumb_mask==255]

            #index
            index_mask = np.zeros((h, w), dtype=np.uint8)
            cv2.fillPoly(index_mask,[index_points],255)
            frame[index_mask == 255] = cool[index_mask == 255] 

            #middle
            middle_mask = np.zeros((h, w), dtype=np.uint8)
            cv2.fillPoly(middle_mask,[middle_points],255)
            frame[middle_mask == 255] = negative[middle_mask == 255]  

            #ring
            ring_mask = np.zeros((h, w), dtype=np.uint8)
            cv2.fillPoly(ring_mask,[ring_points],255)
            frame[ring_mask == 255] = twilight[ring_mask == 255]            


       
    cv2.imshow("Gesture Filters", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
hands.close()
cv2.destroyAllWindows()