"""
aplikasi ini akan mengambil video dari kamera webcam yang tepasang di komputer

"""

import cv2

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter("video/video.avi", fourcc, 6.0, (640, 480))

while cap.isOpened():
    _, img = cap.read()

    frame = cv2.flip(img, 1)
    out.write(frame)
    cv2.imshow('kamera', frame)
    if cv2.waitKey(5) == ord('q'):
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        break