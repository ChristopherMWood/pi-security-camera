import sys
import cv2
import time

frames_per_second = 20
frame_length = 1000.0/frames_per_second
current_milliseconds = lambda: int(round(time.time() * 1000.0))

#-------------GETTING TRAINING CODE READY-------------------------------------------
training_data, testing_data = prepare_training_testing_data(read_csv())

""" Create dict of label -> matricies from file """
### for every line, if key exists, insert into dict, else append
label_dict = {}

for line in training_data:
    ## split on the ';' in the csv separating filename;label
    filename, label = line.strip().split(';')

    ##update the current key if it exists, else append to it
    if label_dict.has_key(int(label)):
        current_files = label_dict.get(label)
        numpy.append(current_files,read_matrix_from_file(filename))
    else:
        label_dict[int(label)] = read_matrix_from_file(filename) 

recognizer = cv2.createEigenFaceRecognizer()
label_dict.train(data_dict.values(), numpy.array(data_dict.keys()))
#-------------ENDING TRAINING CODE -------------------------------------------------

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