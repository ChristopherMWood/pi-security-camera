import sys
import cv2
import time

frames_per_second = 20
frame_length = frames_per_second/1000
current_milliseconds = lambda: int(round(time.time() * 1000))

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
		cv2.rectangle(videoFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)

	cv2.imshow('Live Feed', videoFrame)

	execution_time = current_milliseconds() - execution_start

	if execution_time < frame_length:
		remaining_frame_time = frame_length - execution_time
		sleep(remaining_frame_time/1000)

#imagePath = sys.argv[1]
#cascPath = "../haarcascades/haarcascade_frontalface_default.xml"

#faceCascade = cv2.CascadeClassifier(cascPath)

#image = cv2.imread(imagePath)
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#faces = faceCascade.detectMultiScale(
#    gray,
#    scaleFactor=1.1,
#    minNeighbors=5,
#    minSize=(30, 30),
#    flags = cv2.CASCADE_SCALE_IMAGE
#)

#print "Found {0} faces!".format(len(faces))

# Draw a rectangle around the faces
#for (x, y, w, h) in faces:
#    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

#cv2.imshow("Faces found" ,image)
cap.release()
cv2.waitKey(0)