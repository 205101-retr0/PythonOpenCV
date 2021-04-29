import cv2
import numpy as np

framewidth = 640
frameheight = 480

cap = cv2.VideoCapture(2)
cap.set(3, framewidth)
cap.set(4, frameheight)
cap.set(10, 150)

def getCountors(img):
    # RETR_***** is a mode to find the outer corners there are others but this is ok for now.
    # CHAIN_APPROX_**** is a apporximation method to to minimize the number of corners found in the shapes.
    countors, heirarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0

    for cnt in countors:
        area = cv2.contourArea(cnt)
        if area> 900 and area < 2500:
            peri = cv2.arcLength(cnt, True)
            print(area)

            # True because all figures are closed, approx gives points where the boundaries are.
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)

            x, y, w, h = cv2.boundingRect(approx)
    
    return x+w//2, y


myColors = [[0, 100, 160, 29, 255, 254], [14, 73, 203, 97, 255, 255], [30, 141, 7, 74, 255, 201], [109, 114, 160, 179, 247, 243]]
myColorValues = [[255, 0, 0], [51, 255, 255], [0, 255, 0], [51, 153, 255]]              #In BGR
myPoints = []                                                                           ## (x, y, ColorId)


def findColors(img, result):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        higher = np.array(color[3:6])
        
        mask = cv2.inRange(imgHSV, lower, higher)
        x, y = getCountors(mask)
        
        cv2.circle(result, (x, y), 5, myColorValues[count], -1)
        if x !=0 and y !=0:
            newPoints.append([x, y, count])
        count +=1
        # cv2.imshow(str(color[0]), result)
    return newPoints

def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(result, (point[0], point[1]), 10, myColorValues[point[2]], -1)

while True:
    ret, img = cap.read()
    result = img.copy()
    newPoints = findColors(img, result)

    if len(newPoints): 
        for newp in newPoints:
            myPoints.append(newp)

    if len(myPoints):
        drawOnCanvas(myPoints, myColorValues)
    cv2.imshow("Cam", result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

## SKETCH PENS
# BLUE : hmin: 0, hmax: 23 ,smin: 100, smax: 255, vmin: 160, vmax: 255
# YELLOW : hmin: 14, hmax: 97 ,smin: 73, smax: 255, vmin: 203, vmax: 255 
# GREEN : hmin: 30, hmax: 74 ,smin: 141, smax: 255, vmin: 7, vmax: 201
# ORANGE : hmin: 109, hmax: 179 ,smin: 114, smax: 247, vmin: 160, vmax: 243


## PENS
# BLUE : hmin: 0, hmax: 30 ,smin: 173, smax: 255, vmin: 90, vmax: 255