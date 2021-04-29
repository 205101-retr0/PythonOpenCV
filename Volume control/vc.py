import cv2
import mediapipe as mp
import time
import trackingModule
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

framewidth, frameheight = 1028, 720

def run():
    cap = cv2.VideoCapture(1)
    cap.set(3, framewidth)
    cap.set(4, frameheight)
    cTime, pTime = 0, 0

    Detector = trackingModule.handDetector(detectionCon=0.8)

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # volume.GetMute()
    # volume.GetMasterVolumeLevel()
    volrange = volume.GetVolumeRange()
    minvol = volrange[0]
    maxvol = volrange[1]
    
    while True:
        ret, img = cap.read()

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        img = Detector.handTracking(img)
        lmlist = Detector.positionTracking(img, handNo=0,draw=False)

        if len(lmlist) !=0:
            # Co-ordinates for the volume control
            x1, y1 = lmlist[4][1], lmlist[4][2]
            x2, y2 = lmlist[8][1], lmlist[8][2]
            
            cx, cy = (x1+x2)//2, (y1+y2)//2

            cv2.circle(img, (x1, y1), 6, (255, 0, 0), -1)
            cv2.circle(img, (x2, y2), 6, (255, 0, 0), -1)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.circle(img, (cx, cy), 6, (255, 0, 0), -1)

            length = math.hypot(x2-x1, y2-y1)
            print(length)

            ## Max len = 190 and Min len = 30
            ## volume range Max = 0 and Min = -65.25
            
            vol = np.interp(length, [30, 250], [minvol, maxvol])
            volume.SetMasterVolumeLevel(vol, None)

            if length < 30:
                cv2.circle(img, (cx, cy), 6, (255, 255, 0), -1)

        cv2.putText(img, f'FPS: {str(int(fps))}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1)
        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    run()