import sys
import cv2
import time
import math
import os
import random
import numpy
import pprint
from PIL import Image

_CV_COLOR_ = cv2.COLOR_RGB2GRAY
saved_users = {}

def main():
	frames_per_second = 20
	frame_length = 1000.0/frames_per_second
	current_milliseconds = lambda: int(round(time.time() * 1000.0))

	cascPath = "../haarcascades/haarcascade_frontalface_default.xml"
	faceCascade = cv2.CascadeClassifier(cascPath)
	videoStream = cv2.VideoCapture(0)
	
	training_data, testing_data = prepare_training_testing_data(read_csv())
	data_dict = create_label_matrix_dict(training_data)
	model = create_and_train_model_from_dict(data_dict)

	while(True):
		execution_start = current_milliseconds()

		ret, videoFrame = videoStream.read()
		gray = cv2.cvtColor(videoFrame, _CV_COLOR_)

		faces = faceCascade.detectMultiScale(
			gray,
			scaleFactor = 1.1,
			minNeighbors = 5,
			minSize = (30, 30),
			flags = cv2.CASCADE_SCALE_IMAGE
		)

		prediction_image = get_prediction_formatted_image(videoFrame, faces)

		for (x, y, w, h) in faces:
			predicted_user, confidence = model.predict(prediction_image)
			print(str(predicted_user) + " - Confidence: " + str(confidence))

			predicted_user_output = "Unknown"
			if predicted_user >= 0:
				predicted_user_output = saved_users[predicted_user]

			cv2.putText(videoFrame, predicted_user_output, (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
			cv2.rectangle(videoFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)

		cv2.imshow('Live Feed', videoFrame)

		execution_time = current_milliseconds() - execution_start
		#print(execution_time) PRINT AVERAGE TIME PER SECOND INSTEAD OF ALL TIME

		if execution_time < frame_length:
			remaining_frame_time = frame_length - execution_time
			time.sleep(remaining_frame_time/1000)

		if cv2.waitKey(1) & 0xFF == ord('q'):
		   break

	cap.release()
	cv2.waitKey(0)

def make_directory(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

def get_prediction_formatted_image(image, faces):
	for (x, y, w, h) in faces:
		temp_file_location = "./temp/temp_file.png"
		save_image(image, temp_file_location)
		temp_image = Image.open(temp_file_location)
		cropped_image = temp_image.crop((x, y, x + w, y + h))
		cropped_image.save(temp_file_location, "PNG")
		loaded_cropped_image = cv2.imread(temp_file_location, _CV_COLOR_)
		temp_image = cv2.resize(loaded_cropped_image, (200, 200))
		return cv2.cvtColor(temp_image, cv2.COLOR_BGR2GRAY)

def save_image(image, path):
	cv2.imwrite(path, image)

def create_and_train_model_from_dict(label_matrix):
	""" Create eigenface model from dict of labels and images """
	model = cv2.face.createEigenFaceRecognizer()
	model.train(label_matrix.values(), numpy.array(label_matrix.keys()))
	return model

def read_csv(filename='faces.csv'):
	""" Read a csv file """
	csv = open(filename, 'r')
	return csv

def prepare_training_testing_data(file):
	""" prepare testing and training data from file"""
	lines = file.readlines()
	training_data, testing_data = split_test_training_data(lines)
	return training_data, testing_data

def create_label_matrix_dict(input_file):
	""" Create dict of label -> matricies from file """
	### for every line, if key exists, insert into dict, else append
	label_dict = {}

	for line in input_file:
		filename, username, label = line.strip().split(';')
		
		print(filename + " " + username + " " + str(label))

		if not saved_users.has_key(int(label)):
			saved_users[int(label)] = username

		##update the current key if it exists, else append to it
		if label_dict.has_key(int(label)):
			current_files = label_dict.get(label)
			numpy.append(current_files,read_matrix_from_file(filename))
		else:
			label_dict[int(label)] = read_matrix_from_file(filename)

	return label_dict 

def split_test_training_data(data, ratio=0.2):
	""" Split a list of image files by ratio of training:test data """
	test_size = int(math.floor(ratio*len(data)))
	random.shuffle(data)
	return data[test_size:], data[:test_size]

def read_matrix_from_file(filename):
	""" read in grayscale version of image from file """
	return cv2.imread(filename, _CV_COLOR_)

if __name__ == '__main__':
	make_directory("temp")
	main()