import cv2
import numpy as np
import random

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

green=0,255,0
blue=255,0,0
red=0,0,255

color=[green,blue,red]
randomcolour=random.choice(color)


while True:
    ret, frame = cap.read()

    if not ret:
        break

    h, w, _ = frame.shape
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    low = np.array([0, 0, 200])
    high = np.array([179, 255, 255])
    mask = cv2.inRange(hsv, low, high)

    black = np.zeros_like(frame)


    for y in range(0,h,10):
        for x in range(0,w,10):
            if mask[y, x] == 255:
                number = str(np.random.choice(["1","0"]))
                cv2.putText(black,number,(x, y),cv2.FONT_HERSHEY_SIMPLEX,0.3,(green),1)
 


    black = cv2.flip(black, 1)
    cv2.imshow(" ", black)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()