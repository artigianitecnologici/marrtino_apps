# program to capture single image from webcam in python 

# importing OpenCV library 
from cv2 import *

# initialize the camera 
# If you have multiple camera connected with 
# current device, assign a value in cam_port 
# variable according to that 
cam_port = 2
cam = VideoCapture(cam_port) 
# Check if the camera is opened successfully
if not cam.isOpened():
    print("Error: Could not open camera.")
    exit()
# Set the desired resolution (width, height)
desired_width = 640
desired_height = 480
cam.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)
# reading the input using the camera 
result, image = cam.read() 
# If image will detected without any error, 
# show result 
if result: 

	# showing result, it take frame name and image 
	# output 
	imshow("GeeksForGeeks", image) 

	# saving image in local storage 
	imwrite("GeeksForGeeks.png", image) 

	# If keyboard interrupt occurs, destroy image 
	# window 
	waitKey(0) 
	destroyWindow("GeeksForGeeks") 

# If captured image is corrupted, moving to else part 
else: 
	print("No image detected. Please! try again") 

