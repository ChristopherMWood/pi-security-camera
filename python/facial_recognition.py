import sys
import cv2
import time

frames_per_second = 20
frame_length = 1000.0/frames_per_second
current_milliseconds = lambda: int(round(time.time() * 1000.0))

cascPath = "../haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
videoStream = cv2.VideoCapture(0)

while(True):
	execution_start = current_milliseconds()

	ret, videoFrame = videoStream.read()
	gray = cv2.cvtColor(videoFrame, cv2.COLOR_BGR2GRAY)

	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor = 1.1,
		minNeighbors = 5,
		minSize = (30, 30),
		flags = cv2.CASCADE_SCALE_IMAGE
	)

	for (x, y, w, h) in faces:
		cv2.putText(videoFrame, "Unknown", (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
		cv2.rectangle(videoFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)

	cv2.imshow('Live Feed', videoFrame)

	execution_time = current_milliseconds() - execution_start
	print(execution_time)

	if execution_time < frame_length:
		remaining_frame_time = frame_length - execution_time
		time.sleep(remaining_frame_time/1000)

	if cv2.waitKey(1) & 0xFF == ord('q'):
	   break

cap.release()
cv2.waitKey(0)