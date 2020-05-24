import speech_recognition as sr
import time
from time import ctime
import playsound
import os
import random
from gtts import gTTS
import datetime
from facerec import FaceAssistant



faceAssistant = FaceAssistant
now = datetime.datetime.now()
time_now = f"{now.hour}:{now.minute}"
day_now = f"{now.day}"
WAKE_WORD = "mirror"
r = sr.Recognizer()
m = sr.Microphone(device_index=0)
#m.RATE = 8000
#m.CHUNK = 512
wrong_count = 0


def record_audio():
    with m as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
            print(voice_data)
        except Exception as e:
            mirror_speech("Did not understand")
        return voice_data

def mirror_speech(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)

def respond(voice_data):
    if 'what is your name' in voice_data:
        mirror_speech("My name is Mirror.")
    if 'what time is it' in voice_data:
        mirror_speech(time_now)
    if 'what day is it' in voice_data:
        mirror_speech(day_now)
    if 'how are you' in voice_data:
        mirror_speech('Not great because of corona virus.')
    if 'bye' in voice_data:
        mirror_speech('have a good day and see you')
        exit()

def speech_main():
    while True:
        print("Listening:")
        voice_data = record_audio()
        if  WAKE_WORD in voice_data.lower():
            faceAssistant.face_rec()
            if faceAssistant.userName == None:
                mirror_speech("Can't recognize face.")
                wrong_count += 1
                print(wrong_count)
                if wrong_count == 3:
                    mirror_speech("You've reached the false login count. Terminating the program")
                    exit()
            else:
                wrong_count = 0
                mirror_speech(f"Hello, {faceAssistant.userName}. How can I help you?")
                uName = faceAssistant.userName
                print("Command:")
                voice_data = record_audio()
                respond(voice_data)
                return uName

speech_main()

