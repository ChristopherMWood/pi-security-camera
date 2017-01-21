# HomeSecurityCamera
Home spun security program for Raspberry PI Zero w/Camera v2 setup

Haarcascades and lbpcascades provided by (https://github.com/spmallick/mallick_cascades)

# Home Security Camera
This project is intended to be used with a Raspberry PI and Camera V2 to monitor the outside of a house using motion motion detecting and facial recognition. Despite there being a lot of projects out there that do the same thing (and probably much better), I have been inspired by my house being recently robbed (the bastard(s)).

Instead of paying a bundle of cash for a pre made solution, I thought it would be fun to track visits to my house using open source software and a bit of Raspberry PI hardware. Everything I used, both hardware and software, is listed below so I can recreate this in a matter of hours given the right setup.

### Hardware
- Raspberry PI Zero v1.3
- Raspberry PI Camera v2
- 802.11n Wireless Dongle
- USB 2.0 4-Port Hub (non-passive)*

#### OpenCV
All facial recognition is done using OpenCV which can be downloaded for both C++ and Python using the following repository linked below. https://github.com/jayrambhia/Install-OpenCV. Somebody was nice enough to put together a script to get the most recent version and install them which has been known to be kinda difficuts with OpenCV so thank them for that.

#### C++ vs Python
I intend to finish this project in both C++ and Python. I started with python since it was easier to make a proof of concept using it. I then went for C++ since it runs magnitudes faster on Raspberry PI hardware which is really important on such a low powered devices doing image processing. If you are using a PI Zero I suggest C++. If you are working on a more powerful system and don't have experience with C/C++, feel free to run the Python version and just do some testing to make sure the video streaming can keep up with the processing requirement and that frames are not dropped or lost. (Hopefully I will explainn more about this when I actually get this running)

#### Save new Person to face directory (create_new_face_database_record.py)
- [ ] Program param1: directory of saved faces ; param2: name of new face
- [ ] Show Video Stream and take picture on press of spacebar
- [ ] Save grayscale image of each face direction profile

#### Convert Face Directory into Face Database CSV (faces_to_csv.py)
- [ ] Read in directory and build id/profile data

#### Detect Faces from Face database in realtime (saved_faces_recognizer.py)
- [ ] Load Existing saved faces from CSV
- [ ] Do more stuff
