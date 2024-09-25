#!/usr/bin/env python
# Python 2 compatibility for print
from __future__ import print_function
import rospy
from std_msgs.msg import String
from gtts import gTTS
from pydub import AudioSegment
import os
import socket
import subprocess

class TTSNode:

    def __init__(self):
        rospy.init_node('tts_node', anonymous=True)
        rospy.loginfo('Start tts_node')
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

    def adjust_pitch(self, file_path, octaves=1.0):
        sound = AudioSegment.from_file(file_path)
        new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
        pitch_changed_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        pitch_changed_sound = pitch_changed_sound.set_frame_rate(44100)
        return pitch_changed_sound

    def adjust_speed(self, sound, speed=0.5):
        new_sound = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * 0.65)
        })
        
        return new_sound.set_frame_rate(44100)

    def adjust_pitch_and_speed(self, file_path, octaves=1.0, speed=0.8):
        sound = AudioSegment.from_file(file_path)

        # Aumenta il pitch
        pitch_changed_sound = self.adjust_pitch(file_path, octaves=1.0)
        slowed_sound = self.adjust_speed(pitch_changed_sound, speed=0.5)

        # Esporta l'audio modificato
        slowed_sound.export('output_with_pitch_and_speed.mp3', format='mp3')

    def tts_callback(self, msg):
        text = msg.data
        rospy.loginfo('Received text: "%s"' % text)
        rospy.loginfo('Using language: "%s"' % self.language)  # Log current language
        self.finished_speaking = False
        self.loop_count_down = 0

        # Check internet connectivity
        if self.is_connected():
            # Convert text to speech
            tts = gTTS(text, lang=self.language)
            tts.save('output.mp3')
            
             
            self.adjust_pitch_and_speed('output.mp3', octaves=0.5, speed=0.8)
            
            # Play the file using mpg321 (or any other preferred method)
            os.system('mpg321 output_with_pitch_and_speed.mp3')
            
            # Publish the fact that the TTS is done
            self.publisher_.publish(String(data='TTS done'))
        else:
            # Fallback to pico2wave if there's no internet connection
            filename = "/tmp/robot_speach.wav"
            voice = 'it-IT'
            cmd = ['pico2wave', '--wave=' + filename, '--lang=' + voice, text]
            subprocess.call(cmd)
            cmd = ['play', filename, '--norm', '-q']
            subprocess.call(cmd)
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
