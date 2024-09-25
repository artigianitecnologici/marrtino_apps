# -*- coding: utf-8 -*-
from pydub import AudioSegment
from gtts import gTTS
import os
import time

def adjust_pitch(sound, octaves=0.0):
    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
    pitch_changed_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    return pitch_changed_sound.set_frame_rate(44100)

def adjust_speed(sound, speed=1.0):
    new_sound = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })
    return new_sound.set_frame_rate(44100)

def adjust_pitch_and_speed(file_path, octaves=0.0, speed=1.0):
    sound = AudioSegment.from_file(file_path)
    pitch_changed_sound = adjust_pitch(sound, octaves)
    final_sound = adjust_speed(pitch_changed_sound, speed)
    
    # Nome del file di output con .format() per Python 2 o versioni precedenti
    output_file = 'output_pitch_{:.1f}_speed_{:.1f}.mp3'.format(octaves, speed)
    final_sound.export(output_file, format='mp3')
    return output_file

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save('original.mp3')

def main():
    text = raw_input("Enter text to convert to speech: ")  # raw_input per Python 2
    lang = raw_input("Enter language (e.g., 'it' for Italian, 'en' for English): ")

    # Genera il file audio originale dal testo
    text_to_speech(text, lang)

    # Velocità fissa per questo esempio (puoi modificarla se necessario)
    speed = 0.8

    # Ciclo per variare il pitch da -1.0 a 1.0 con passi di 0.2
    for octaves in range(-2, 11, 2):  # Questo genera valori come -1.0, -0.8, ..., 1.0
        octaves_value = octaves / 10.0
        print("Testing pitch: {:.1f}".format(octaves_value))
        output_file = adjust_pitch_and_speed('original.mp3', octaves=octaves_value, speed=speed)
        
        # Riproduci il file
        os.system('mpg321 {}'.format(output_file))
        
        # Attesa tra la riproduzione di ogni variazione di pitch
        time.sleep(1)

if __name__ == "__main__":
    main()
