import sys
from PIL import Image
from picamera import PiCamera
import os
import cv2
import select
import time


_CV_COLOR_ = cv2.COLOR_RGB2GRAY

program_display_name = "New Face Registration"
user_quit = False
capture_video_data = True
face_profiles_list = [ "frontal_face" ]
haarcascade_list = [ 
	"../haarcascades/haarcascade_frontalface_default.xml"
]

def main(first_name, last_name):

	new_profile_name = first_name.lower() + "_" + last_name.lower()
	user_directory = "./saved_faces/" + new_profile_name + "/"
	make_directory(user_directory)

	cascade_path = "../haarcascades/haarcascade_frontalface_default.xml"
	face_cascade = cv2.CascadeClassifier(cascade_path)
	
	#video_stream = cv2.VideoCapture(0)
	camera = PiCamera()
	camera.resolution = (1024, 768)
	camera.start_preview()

	capture_profiles = [ "frontal_face" ]

	captured_faces = 0

	current_milli_time = lambda: int(round(time.time() * 1000))
	start_time = current_milli_time
	pictures_taken = 0

	while(capture_video_data):
		key_press = cv2.waitKey(1)
		#ret, video_frame = video_stream.read()
		temp_path = './temp.jpg'
		camera.capture(temp_path)
		pictures_taken += 1
		video_frame = cv2.imread(temp_path, _CV_COLOR_)

		faces = find_faces(video_frame, face_cascade)
		video_frame = bound_found_faces(video_frame, faces)

		image_captured_with_single_face = (key_press == 32 and len(faces) == 1)

		if image_captured_with_single_face:
			save_path = get_file_path(user_directory, new_profile_name, capture_profiles[0], captured_faces)
			image = video_frame
			image = crop_image(image, faces)
			image = greyscale_image(image)
			save_image(image, save_path)
			captured_faces += 1
		
		if key_press == 27 or captured_faces >= 10:
			user_quit = True
			break;

		execution_time = current_milli_time - start_time
		if execution_time >= 1000
			print(pictures_taken)
			pictures_taken = 0
			start_time = current_milli_time

		#show_image_to_screen(video_frame, face_profiles_list[0], captured_faces)

	#video_stream.release()
	camera.stop_preview()
	print("Stream Exited")

def show_image_to_screen(frame, current_profile, image_number):
	height, width, channels = frame.shape
	frame_info_text = "Picture Required: " + current_profile + "(" + str(image_number) + ")"
	cv2.putText(frame, frame_info_text, (5, 25), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
	cv2.putText(frame, "[Press Spacebar to Take Picture...]", (width/4, height - 10), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
	cv2.imshow(program_display_name, frame)

def crop_image(image, faces):
	for (x, y, w, h) in faces:
		temp_file_location = "./temp/temp_file.png"
		save_image(image, temp_file_location)
		temp_image = Image.open(temp_file_location)
		cropped_image = temp_image.crop((x, y, x + w, y + h))
		cropped_image.save(temp_file_location, "PNG")
		loaded_cropped_image = cv2.imread(temp_file_location, _CV_COLOR_)
		return cv2.resize(loaded_cropped_image, (200, 200))

def greyscale_image(image):
	return cv2.cvtColor(image, _CV_COLOR_)

def find_faces(image, face_cascade):
	return face_cascade.detectMultiScale(
		cv2.cvtColor(image, _CV_COLOR_),
		scaleFactor = 1.1,
		minNeighbors = 5,
		minSize = (30, 30),
		flags = cv2.CASCADE_SCALE_IMAGE
	)

def bound_found_faces(image, faces):
	for (x, y, w, h) in faces:
		cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
	return image

def save_image(image, path):
	cv2.imwrite(path, image)
	print("Saved image to " + path)

def get_file_path(path, username, profile, image_number, extension=".pgm"):
	return path + profile + "_" + str(image_number) + extension

def make_directory(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

if __name__ == '__main__':
	make_directory("saved_faces")
	make_directory("temp")
	if len(sys.argv) == 3:
		print("Starting Camera...")
		new_profile_first_name = sys.argv[1]
		new_profile_last_name = sys.argv[2]
		main(new_profile_first_name, new_profile_last_name)
	else:
		print("PROGRAM TERMINATED: Required parameters not provided")
		print("\tParam1: First name of new user")
		print("\tParam2: Last name of new user")
		print("Example: python " + sys.argv[0] + " John Doe")