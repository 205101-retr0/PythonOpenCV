import cv2

def run():
    # Download the haarcascade from the github of the haarcascades.

    facecascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    img = cv2.imread("test2.jpg")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = facecascade.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0))

    cv2.imshow("Image", img)
    cv2.waitKey(0)

if __name__ == "__main__":
    run()