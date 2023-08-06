import cvzone
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector


class EyeTracker:
    def __init__(self):
        self.idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
        self.color = (255, 0, 255)
        self.ratioList = []
        self.blinkCounter = 0
        self.counter = 0

        self.capture = None
        self.detector = None

    def start_capture(self, camera=0):
        self.capture = cv2.VideoCapture(camera, cv2.CAP_DSHOW)
        self.detector = FaceMeshDetector(maxFaces=1)

    def stop_capture(self):
        self.capture.release()

    def get_frame(self):
        return self.capture.read()

    def track_blinks(self):
        ret, frame = self.get_frame()
        if not ret:
            return []
        frame, faces = self.detector.findFaceMesh(frame, draw=False)

        if faces:
            face = faces[0]
            for face_id in self.idList:
                cv2.circle(frame, face[face_id], 5, self.color, cv2.FILLED)

            leftUp = face[159]
            leftDown = face[23]
            leftLeft = face[130]
            leftRight = face[243]
            lengthVer, _ = self.detector.findDistance(leftUp, leftDown)
            lengthHor, _ = self.detector.findDistance(leftLeft, leftRight)

            cv2.line(frame, leftUp, leftDown, (0, 200, 0), 3)
            cv2.line(frame, leftLeft, leftRight, (0, 200, 0), 3)

            ratio = int((lengthVer / lengthHor) * 100)
            self.ratioList.append(ratio)
            if len(self.ratioList) > 3:
                self.ratioList.pop(0)
            ratio_avg = sum(self.ratioList) / len(self.ratioList)

            if ratio_avg < 35 and self.counter == 0:
                self.blinkCounter += 1
                self.color = (0, 200, 0)
                self.counter = 1
            if self.counter != 0:
                self.counter += 1
                if self.counter > 10:
                    self.counter = 0
                    self.color = (255, 0, 255)

            cvzone.putTextRect(frame, f'Blink Count: {self.blinkCounter}', (50, 100),
                               colorR=self.color)

        return frame

    def get_blink_count(self):
        return self.blinkCounter
