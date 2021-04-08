import cv2
import numpy as np

def empty(pas):
    pass


def track():
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", (640, 480))
    cv2.createTrackbar("Hue min", "Trackbars", 0, 179, empty)
    cv2.createTrackbar("Hue max", "Trackbars", 179, 179, empty)
    cv2.createTrackbar("Sat min", "Trackbars", 0, 255, empty)
    cv2.createTrackbar("Sat max", "Trackbars", 255, 255, empty)
    cv2.createTrackbar("Val min", "Trackbars", 110, 255, empty)
    cv2.createTrackbar("Val max", "Trackbars", 255, 255, empty)


def run():

    track()
    while True:
        h_min = cv2.getTrackbarPos("Hue min", "Trackbars")
        h_max = cv2.getTrackbarPos("Hue max", "Trackbars")
        s_min = cv2.getTrackbarPos("Sat min", "Trackbars")
        s_max = cv2.getTrackbarPos("Sat max", "Trackbars")
        v_min = cv2.getTrackbarPos("Val min", "Trackbars")
        v_max = cv2.getTrackbarPos("Val max", "Trackbars") 
        print(v_min,h_min, h_max, v_max, s_max, s_min)



        lower = np.array([h_min, s_min, v_min])
        higher = np.array([h_max, s_max, v_max])

        img = cv2.imread("D:/teja file/Python/Image manipulator/photo2.jpeg")
        img = cv2.resize(img, (440, 280))
        imgHSV = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(imgHSV, lower, higher, 0)
        imgresult = cv2.bitwise_and(img, img, mask=mask)

        cv2.imshow("Original", img)
        cv2.imshow("HSVimage", imgHSV)
        cv2.imshow("Mask", mask)
        cv2.imshow("Result", imgresult)

        cv2.waitKey(1)

        #v_min = 94
        #h_min = 0
        #h_maz = 179
        #v_max = 255
        #s_max = 255
        #s_min = 0


if __name__ ==  "__main__":
    run()