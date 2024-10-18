# -*- coding: utf-8 -*-

import os
import socket
from gtts import gTTS
from pydub import AudioSegment
from subprocess import Popen, PIPE

def remove_special_characters(input_string):
    # Usando una regex per mantenere solo lettere e numeri
    cleaned_string = input_string  # re.sub(r'[^A-Za-z0-9,. ?!]+', '', input_string)
    return cleaned_string

# Percorsi dei file temporanei
tmpfile = "/tmp/cacheita.mp3"
wavfile = "/tmp/cacheita.wav"

class TTSNodeTest:

    def __init__(self):
        print('Starting TTS test...')
        
        # Lingua predefinita
        self.language = 'it'  # Italiano per default

    def set_language(self, lang):
        # Aggiorna la lingua
        self.language = lang
        print('Language updated to: "{}"'.format(self.language))

    def tts_callback(self, text):
        # Pulisce il testo e lo converte in Unicode
        text = remove_special_characters(text).decode('utf-8')  # Conversione in Unicode
       # print('Received text: "{}"'.format(text))
        print('Using language: "{}"'.format(self.language))

        # Controlla la connettività Internet
        
        # Usa Google TTS
        tts = gTTS(text, lang=self.language)
        tts.save(tmpfile)
        sound = AudioSegment.from_mp3(tmpfile)
        sound.export(wavfile, format="wav")
        p = Popen("play " + wavfile + " -q pitch 300 rate 48000", stdout=PIPE, shell=True)
        p.wait()

        print('TTS done with Google TTS.')
     
     


# Esempio di utilizzo
if __name__ == '__main__':
    # Inizializza il sistema TTS di test
    tts_test = TTSNodeTest()

    # Imposta la lingua (opzionale)
    tts_test.set_language('it')

    # Inserisci il testo che vuoi convertire in voce
    text_to_speak = "Ciao, questa è la mia voce in italiano"

    # Esegui il TTS
    tts_test.tts_callback(text_to_speak)
