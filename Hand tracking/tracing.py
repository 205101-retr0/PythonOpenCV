import cv2
import mediapipe as mp
import time

# Frame & FrameRate....
framewidth = 640
frameheight = 480


# Camera setting....
cap = cv2.VideoCapture(1)
cap.set(3, framewidth)
cap.set(4, frameheight)
cap.set(10, 150)

# Hand tracking.....
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

def handTracking(img, results):
    if results.multi_hand_landmarks:
            for mhand in results.multi_hand_landmarks:
                for id, lm in enumerate(mhand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(h*lm.x), int(w*lm.y)
                    print(id, cx, cy)
                mpDraw.draw_landmarks(img, mhand, mpHands.HAND_CONNECTIONS)


def run():
    cTime = 0
    pTime = 0
    while True:
        ret, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        handTracking(img, results)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 5)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    run()