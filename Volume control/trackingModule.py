import cv2
import mediapipe as mp
import time

# Frame & FrameRate....
framewidth, frameheight = 640, 480

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackingCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon

        # Hand tracking.....
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackingCon)
        self.mpDraw = mp.solutions.drawing_utils


    def handTracking(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for mhand in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, mhand, self.mpHands.HAND_CONNECTIONS)
        return img

    def positionTracking(self, img, handNo =0, draw=True):
        lmList = list()

        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(w*lm.x), int(h*lm.y)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 255), -1)   
     
        return lmList


def run():
    # Camera setting....
    cap = cv2.VideoCapture(1)
    cap.set(3, framewidth)
    cap.set(4, frameheight)
    cap.set(10, 150)

    cTime, pTime = 0, 0
    Detector = handDetector()

    while True:
        ret, img = cap.read()

        img = Detector.handTracking(img)
        lmList = Detector.positionTracking(img, draw=False)

        # This value can be changed to get the values of a certain landmark that we want.
        # https://google.github.io/mediapipe/solutions/hands
        # To get the Id's of the landmarks of each fingers check out the website.
        if len(lmList) !=0:
            print(lmList)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 5)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    pass
    # run()