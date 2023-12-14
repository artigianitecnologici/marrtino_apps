#!/usr/bin/python
# -*- coding:utf-8 -*-
import rospy 
from std_msgs.msg import String

import sys
import cv2

def capture_photo(device_index=2, photo_filename='captured_photo.jpg'):
    # Open the video capture device
    cap = cv2.VideoCapture(device_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4600)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2592)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture a single frame
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        print("Error: Could not capture frame.")
        cap.release()
        return

    # Save the captured frame as an image file
    cv2.imwrite(photo_filename, frame)

    # Release the capture device
    cap.release()
    print("Photo captured and saved ")

def callback(data):
    rospy.loginfo('I shot %s', data.data)
    try:
        # Specify the device index and photo filename (modify as needed)
        device_index = 2  # Check which device index your camera is using (e.g., /dev/video2)
        # Capture the photo
        capture_photo(device_index, data.data)

    except Exception as e:
        print("receive msg,but parse exception:", e)

   
    
if __name__ == '__main__':
    rospy.init_node('shot_node', anonymous=True)
    rospy.Subscriber('shot', String, callback, queue_size=1)
    rospy.spin()




