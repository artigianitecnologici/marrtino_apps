#!/usr/bin/env python
# Python 2 compatibility for print
from __future__ import print_function
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

def remove_special_characters(input_string):
    # Usando una regex per mantenere solo lettere e numeri
    cleaned_string = re.sub(r'[^A-Za-z0-9,. ?!]+', '', input_string)
    return cleaned_string

tmpfile = "/tmp/cacheita.mp3"
wavfile = "/tmp/cacheita.wav"

class TTSNode:

    def __init__(self):
        rospy.init_node('tts_node', anonymous=True)
        rospy.loginfo('Start my tts_node')
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
        # Convert the language setting to Unicode
        self.language = msg.data.decode('utf-8')
        rospy.loginfo(u'Language updated to: "%s"' % self.language)

    def tts_callback(self, msg):
        # Convert the incoming text to Unicode
        text = remove_special_characters(msg.data)
        rospy.loginfo(u'Received text: "%s"' % text)  # Log the received text in Unicode
        rospy.loginfo(u'Using language: "%s"' % self.language)  # Log current language
        self.finished_speaking = False
        self.loop_count_down = 0
       
        # Check internet connectivity
        if self.is_connected():
            try:
                # Convert text to speech
                tts = gTTS(text, lang=self.language)
                tts.save(tmpfile)
                sound = AudioSegment.from_mp3(tmpfile)
                sound.export(wavfile, format="wav")
                p = Popen("play " + wavfile + " -q pitch 300 rate 48000", stdout=PIPE, shell=True)
                p.wait()
                
                #os.remove(tmpfile)
                # Publish the fact that the TTS is done
                self.publisher_.publish(String(data='TTS done'))
            except Exception as e:
                rospy.logerr("Error in TTS conversion: %s" % str(e))
        else:
            # Fallback to pico2wave if there's no internet connection
            
            voice = 'it-IT'  # Adjust the voice as per language
           # cmd = 'pico2wave -l "%s" -w %s " , %s"' %(lang,tmpfile, data)
            rospy.loginfo("pico2wave -l " + voice + " -w " + wavfile + " '" + text.encode('utf-8') + "'" )
            p = Popen("pico2wave -l " + voice + " -w " + wavfile + " '" + text.encode('utf-8') + "' "  , stdout=PIPE, shell=True)
            p.wait()
            #subprocess.call(cmd)
            p = Popen("play " + wavfile + " -q --norm", stdout=PIPE, shell=True)
            p.wait()
            #os.remove(wavfile)
            #cmd = ['play', filename, '--norm', '-q']
            #subprocess.call(cmd)
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
            # Crea un socket e imposta un timeout molto breve (es. 0.1 secondi)
            sock = socket.create_connection(("www.google.it", 80), timeout=0.1)
            sock.close()  # Chiude il socket dopo la connessione
            return True
        except socket.error as e:
            rospy.loginfo("No internet connection: %s" % str(e))
            return False

    def spin(self):
        while not rospy.is_shutdown():
            self.speaking_finished()
            self.rate.sleep()

if __name__ == '__main__':
    node = TTSNode()
    node.spin()
