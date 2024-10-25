#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import String
from gtts import gTTS
import os
import socket
from pydub import AudioSegment
from subprocess import Popen, PIPE
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
import re


tmpfile = "/tmp/cacheita.mp3"
wavfile = "/tmp/cacheita.wav"

class TTSNode:

    def __init__(self):
        rospy.init_node('tts_node', anonymous=True)
        rospy.loginfo('Start   tts_node v.1.00' )
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
        self.connected = True
        self.msgoffline = False

    def language_callback(self, msg):
        # Convert the language setting to Unicode
        self.language = msg.data.decode('utf-8')
        # if self.language == 'it':
        #     self.language = 'it-IT'
        # if self.language == 'en':
        #     # self.language = 'en-GB'

        rospy.loginfo(u'Language updated to: "{}"'.format(self.language))

    def tts_callback(self, msg):
        # Convert the incoming text to Unicode
        text = msg.data.decode('utf-8')  # Ensures proper decoding of special characters
        print(u'Received text: "{}"'.format(text))
        rospy.loginfo(u'Using language: "{}"'.format(self.language))
        self.finished_speaking = False
        self.loop_count_down = 0
       
        # Check internet connectivity
        if self.is_connected():
            try:
                # Convert text to speech using Google TTS
                
                tts = gTTS(text, lang=self.language)
                tts.save(tmpfile)
                sound = AudioSegment.from_mp3(tmpfile)
                sound.export(wavfile, format="wav")
                if self.language in ['it-IT', 'it']:
                    p = Popen("play " + wavfile + " -q pitch 300 rate 48000", stdout=PIPE, shell=True)
                else:
                    p = Popen("play " + wavfile + " -q ", stdout=PIPE, shell=True)
                p.wait()
                
                # Publish the fact that the TTS is done
                self.publisher_.publish(String(data='TTS done'))
            except Exception as e:
                rospy.logerr("Error in TTS conversion: {}".format(str(e)))
        else:
            voice = self.language
            # Fallback to pico2wave if there's no internet connection
            if self.language == 'it':
                self.language = 'it-IT'
            if self.language == 'en':
                self.language = 'en-GB'
            if (text == 'online'):
                self.connected = True
                if self.is_connected():
                    
                    p = Popen("pico2wave -l " + voice + " -w " + wavfile + " ' Sono  online' ", stdout=PIPE, shell=True)
                    p.wait()
                    p = Popen("play " + wavfile + " -q --norm", stdout=PIPE, shell=True)
                    p.wait()
                    self.msgoffline = False


            if (self.msgoffline == True):
                p = Popen("pico2wave -l " + voice + " -w " + wavfile + " ' Sono off line per riattivare  use la parola online' ", stdout=PIPE, shell=True)
                p.wait()
                p = Popen("play " + wavfile + " -q --norm", stdout=PIPE, shell=True)
                p.wait()
                self.msgoffline = False

            
            rospy.loginfo("pico2wave -l " + voice + " -w " + wavfile + " '" + text.encode('utf-8') + "'")
            p = Popen("pico2wave -l " + voice + " -w " + wavfile + " '" + text.encode('utf-8') + "' ", stdout=PIPE, shell=True)
            p.wait()
            p = Popen("play " + wavfile + " -q --norm", stdout=PIPE, shell=True)
            p.wait()
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
        if (self.connected == True):
            try:
                # Crea un socket e imposta un timeout molto breve (es. 0.1 secondi)
                sock = socket.create_connection(("www.google.it", 80), timeout=0.1)
                sock.close()  # Chiude il socket dopo la connessione
                return True
            except socket.error as e:
                rospy.loginfo("No internet connection: {}".format(str(e)))
                self.connected = False
                self.msgoffline = True
                return False
        else:
            return False                

    def spin(self):
        while not rospy.is_shutdown():
            self.speaking_finished()
            self.rate.sleep()

if __name__ == '__main__':
    node = TTSNode()
    node.spin()
