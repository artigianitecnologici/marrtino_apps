#!/usr/bin/env python
# Python 2 compatibility for print
from __future__ import print_function
import rospy
from std_msgs.msg import String
from gtts import gTTS
import os
import socket
import subprocess

class TTSNode:

    def __init__(self):
        rospy.init_node('tts_node', anonymous=True)
        rospy.loginfo('Start ny tts_node')
        self.publisher_ = rospy.Publisher('/social/speech/status', String, queue_size=10)
        self.subscription = rospy.Subscriber('/social/speech/to_speak', String, self.tts_callback)
        # Subscriber for language settings
        self.lang_subscription = rospy.Subscriber('/social/speech/language', String, self.language_callback)
        
        # Default language
        self.language = 'it'  # Italian by default
        # For managing speaking state
        self.finished_speaking = False
        self.loop_count_down = 0
        self.rate = rospy.Rate(10)  # Set loop frequency to 10Hz

    def language_callback(self, msg):
        self.language = msg.data
        rospy.loginfo('Language updated to: "%s"' % self.language)

    def tts_callback(self, msg):
        text = msg.data
        rospy.loginfo('Received text: "%s"' % text)
        rospy.loginfo('Using language: "%s"' % self.language)  # Log current language
        self.finished_speaking = False
        self.loop_count_down = 0

        # Check internet connectivity
        if self.is_connected():
            # Convert text to speech
            tts = gTTS(text,lang=self.language)
            tts.save('output.mp3')
            os.system('mpg321 output.mp3')
            # Publish the fact that the TTS is done
             
            self.publisher_.publish(String(data='TTS done'))
        else:
            # Fallback to pico2wave if there's no internet connection
            filename = "/tmp/robot_speach.wav"
            # Adjust this to set the correct voice or use default language
            voice = 'it-IT'
            cmd = ['pico2wave', '--wave=' + filename, '--lang=' + voice, text]
            subprocess.call(cmd)
            # Play created wav file using sox play
            cmd = ['play', filename, '--norm', '-q']
            subprocess.call(cmd)
            # Set up to send talking finished
            self.finished_speaking = True
            self.loop_count_down = int(10 * 2)  # 2 seconds delay at 10Hz rate

    def speaking_finished(self):
        if self.finished_speaking:
            self.loop_count_down -= 1
            if self.loop_count_down <= 0:
                rospy.loginfo('Speaking finished')
                self.finished_speaking = False
                self.publisher_.publish(String(data='TTS done'))

    def is_connected(self):
        try:
            # Try to connect to a well-known website
            socket.create_connection(("www.google.com", 80))
            return True
        except OSError:
            return False

    def spin(self):
        while not rospy.is_shutdown():
            self.speaking_finished()
            self.rate.sleep()


if __name__ == '__main__':
    node = TTSNode()
    node.spin()

