import cv2
import numpy as np
import sys
if sys.platform == "win32":
    import winsound
else:
    import simpleaudio as sa
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

cap = cv2.VideoCapture(0)
closed_eyes_frames = 0
CONSEC_FRAMES = 6
play_obj = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    eyes_detected = False

    for (x, y, w, h) in faces:
        face_roi_gray = gray[y:y+h//2, x:x+w]
        eyes = eye_cascade.detectMultiScale(face_roi_gray, scaleFactor=1.1, minNeighbors=7, minSize=(30,30))

        if len(eyes) > 0:
            eyes_detected = True
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (0, 255, 0), 2)

    if not eyes_detected:
        closed_eyes_frames += 1
    else:
        closed_eyes_frames = 0
        if play_obj is not None:
            if sys.platform == "win32":
                winsound.PlaySound(None, winsound.SND_PURGE)
            else:
                play_obj.stop()
            play_obj = None

    status = "Eyes Open"
    if closed_eyes_frames >= CONSEC_FRAMES:
        status = "Eyes Closed - Drowsy!"
        if play_obj is None:
            if sys.platform == "win32":
                winsound.Beep(1000, 500)
            else:
                wave_obj = sa.WaveObject.from_wave_file("/Users/rishavsingh/Documents/CODE/Hackathon 1.0/beep.wav")
                play_obj = wave_obj.play()

    cv2.putText(frame, status, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 0, 255) if "Closed" in status else (0, 255, 0), 2)

    cv2.imshow("Driver Monitoring", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()