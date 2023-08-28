import streamlit as st
import cvzone
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector

st.set_page_config(page_title="Eye Tracker", layout="wide")

st.title("Eye Tracker")

idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243] # Points for eyes, taken from cvzone source doc
color = (255, 0, 255)
ratioList = []
blinkCounter = 0
counter = 0

# Argument represents which camera to capture
# Currently defaults to default webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

detector = FaceMeshDetector(maxFaces=1)

frame_placeholder = st.empty()

video_stop = st.button("Stop")

while cap.isOpened() and not video_stop:
    ret, frame = cap.read()

    if not ret:
        st.write("Webcam stream ended")
        break
    
    frame, faces = detector.findFaceMesh(frame, draw=False)

    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(frame, face[id], 5, color, cv2.FILLED)

        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lenghtVer, _ = detector.findDistance(leftUp, leftDown)
        lenghtHor, _ = detector.findDistance(leftLeft, leftRight)

        cv2.line(frame, leftUp, leftDown, (0, 200, 0), 3)
        cv2.line(frame, leftLeft, leftRight, (0, 200, 0), 3)

        ratio = int((lenghtVer / lenghtHor) * 100)
        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)

        if ratioAvg < 35 and counter == 0:
            blinkCounter += 1
            color = (0, 200, 0)
            counter = 1
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                color = (255, 0, 255)

        cvzone.putTextRect(frame, f'Blink Count: {blinkCounter}', (50, 100),
                           colorR=color)

    frame_placeholder.image(frame, channels="RGB")

    if cv2.waitKey(1) & 0xff == ord('q') or video_stop:
        break

cap.release()
cv2.destroyAllWindows()
