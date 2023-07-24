import streamlit as st
import numpy as np
import cv2

st.set_page_config(page_title="Eye Tracker", layout="wide")

st.title("Eye Tracker")

# Argument represents which camera to capture
# Currently defaults to default webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

frame_placeholder = st.empty()

video_stop = st.button("Stop")

while cap.isOpened() and not video_stop:
    ret, frame = cap.read()

    if not ret:
        st.write("Webcam stream ended")
        break
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame_placeholder.image(frame, channels="RGB")

    if cv2.waitKey(1) & 0xff == ord('q') or video_stop:
        break

cap.release()
cv2.destroyAllWindows()
