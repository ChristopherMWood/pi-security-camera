import cv2
import time
import math
import os
import random
import numpy
from PIL import Image

_CV_COLOR_ = cv2.COLOR_RGB2GRAY
face_cascade_path = "../haarcascades/haarcascade_frontalface_default.xml"
saved_users = {}


def main():
	face_cascade = cv2.CascadeClassifier(face_cascade_path)
	video_stream = cv2.VideoCapture(0)

	eigenface_model = get_training_model()

	while True:
		ret, video_frame = video_stream.read()

		gray = cv2.cvtColor(video_frame, _CV_COLOR_)
		faces = face_cascade.detectMultiScale(
			gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE
		)

		for (x, y, width, height) in faces:
			prediction_image = get_prediction_formatted_image(video_frame, x, y, width, height)
			predicted_user = eigenface_model.predict(prediction_image)
			print(predicted_user)

			predicted_user_output = "Unknown"
			# if predicted_user >= 0:
			# 	predicted_user_output = saved_users[predicted_user]

			cv2.putText(video_frame, predicted_user_output, (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
			cv2.rectangle(video_frame, (x, y), (x + width, y + height), (0, 255, 0), 2)

		cv2.imshow('Live Feed', video_frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	video_stream.release()
	cv2.waitKey(0)


def get_training_model():
	training_data, testing_data = prepare_training_testing_data()
	dictionary = create_label_matrix_dict(training_data)
	model = cv2.face.createEigenFaceRecognizer()
	model.train(dictionary.values(), numpy.array(dictionary.keys()))
	return model


def prepare_training_testing_data():
	csv_file = read_csv()
	lines = csv_file.readlines()
	training_data, testing_data = split_test_training_data(lines)
	return training_data, testing_data


def create_label_matrix_dict(input_file):
	label_dict = {}

	for line in input_file:
		filename, username, label = line.strip().split(';')

		if not saved_users.has_key(int(label)):
			saved_users[int(label)] = username

		if label_dict.has_key(int(label)):
			current_files = label_dict.get(label)
			numpy.append(current_files, read_matrix_from_file(filename))
		else:
			label_dict[int(label)] = read_matrix_from_file(filename)

	print(saved_users)
	return label_dict


def make_directory(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)


def get_prediction_formatted_image(image, x, y, width, height):
	temp_file_location = "./temp/temp_file.png"
	save_image(image, temp_file_location)
	temp_image = Image.open(temp_file_location)
	cropped_image = temp_image.crop((x, y, x + width, y + height))
	cropped_image.save(temp_file_location, "PNG")
	loaded_cropped_image = cv2.imread(temp_file_location, _CV_COLOR_)
	temp_image = cv2.resize(loaded_cropped_image, (200, 200))
	return cv2.cvtColor(temp_image, _CV_COLOR_)


def save_image(image, path):
	cv2.imwrite(path, image)


def read_csv(filename='faces.csv'):
	csv = open(filename, 'r')
	return csv


def split_test_training_data(data, ratio=0.2):
	test_size = int(math.floor(ratio*len(data)))
	random.shuffle(data)
	return data[test_size:], data[:test_size]


def read_matrix_from_file(filename):
	return cv2.imread(filename, _CV_COLOR_)


if __name__ == '__main__':
	make_directory("temp")
	main()