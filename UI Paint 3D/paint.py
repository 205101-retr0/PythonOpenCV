import cv2
import numpy as np
import trackingModule as tm
import os

################
framewidth, frameheight = 1280, 640
brushThickness = 15
earserThinckness = 25
###############

overlay = []
folder = 'Header2'
images = os.listdir(folder)
for impath in images:
    img = cv2.imread(f'{folder}/{impath}')
    overlay.append(img)
# print(images)


def run():
    # Camera setting....
    cap = cv2.VideoCapture(2)
    cap.set(3, framewidth)
    cap.set(4, frameheight)
    header = overlay[0]
    drawColor = (255, 255, 0)
    xp, yp = 0, 0
    imgCanvas = np.zeros((frameheight, framewidth, 3), np.uint8)

    Detector = tm.handDetector(detectionCon=0.85)

    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)


        img = Detector.handTracking(img)
        lmList = Detector.positionTracking(img, draw=False)

        if len(lmList) !=0:

            fingers = Detector.fingersUp()
            # print(fingers)

            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

            if fingers[1] and fingers[2]:
                xp, yp = 0, 0
                cv2.rectangle(img, (x1, y1-15), (x2, y2+15), (255, 23, 54), -1)
                print("Selection Mode")
                if y1 < 139:
                    if 0 < x1 < 220:
                        header = overlay[0]
                        drawColor = (255, 255, 0) ##BGR
                    elif 230 < x1 < 450:
                        header = overlay[1]
                        drawColor = (51, 255, 51)
                    elif 450 < x1 < 740:
                        header = overlay[2]
                        drawColor = (0, 0, 255)
                    elif 750 < x1 < 900:
                        header = overlay[3]
                        drawColor = (0, 0, 0)
                    elif 910<x1<1280:
                        header = overlay[4]
                        drawColor = (255, 255, 255)
            
            if fingers[1] and fingers[2]==0:
                cv2.circle(img, (x1, y1), 10, (255, 23, 54), -1)

                if xp ==0 and yp == 0:
                    xp, yp = x1, y1

                if drawColor == (255, 255, 255):
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, earserThinckness, -1)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, earserThinckness, -1)
                
                else:
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness, -1)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness, -1)
                print("Drawing mode")

                xp, yp = x1, y1
            

        img[0:139, 0:1280] = header
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, inv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
        img = cv2.resize(img, (1280, 640))
        img = cv2.bitwise_and(img, inv)
        img = cv2.bitwise_or(img, imgCanvas)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    run()