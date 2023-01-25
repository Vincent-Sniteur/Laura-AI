# Create vocal assistant Laura - auto activate when you say "Laura" and deactivate when you say "stop"
# The assistant will ask your question to chatGPT3 and answer you with voices

import speech_recognition as sr
import pyaudio
import openai
from gtts import gTTS
from pydub import AudioSegment
import simpleaudio as sa
from fuzzywuzzy import fuzz
import configparser

# read config file
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['openai']['api_key']

# openai api key
openai.api_key = api_keys

# Set the language of the assistant
language = 'fr'

# Set model of the assistant
model = 'text-davinci-003'

# TODO: Set the minimum ratio required for a match
# min_ratio = 80

# Initializing the recognizer
r = sr.Recognizer()

# Starting the microphone
with sr.Microphone() as source:
    print("Dite 'Laura' pour activer l'assistant vocal")
    audio = r.listen(source)

# Recognizing the speech
# TODO: add a ratio to say "Laura" and "stop"
text = r.recognize_google(audio)

# print the text
print(text)

# if you say "Laura" the assistant will start
if text.lower() == "laura":
    print("Bonjour que puis-je faire pour vous ?")
    # play a sound to say that the assistant is ready
    wave_obj = sa.WaveObject.from_wave_file("ready.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()
    # start the assistant
    while True:
        # Starting the microphone
        with sr.Microphone() as source:
            print("Je vous écoute...")
            audio = r.listen(source)

        # Recognizing the speech
        text = r.recognize_google(audio)

        # print the text
        print(text)

        # if you say "stop" the assistant will stop
        if text.lower() == "stop":
            print("Goodbye!")
            # play a sound to say that the assistant is ready
            wave_obj = sa.WaveObject.from_wave_file("bye.wav")
            play_obj = wave_obj.play()
            play_obj.wait_done()
            break

        # if you say something else the assistant will ask the question to chatGPT3 and answer you
        else:
            # ask the question to chatGPT3
            response = openai.Completion.create(
                # TODO: change the prompt
                # TODO: add a way to save the conversation
            )

# TODO: print the answer and play the answer with voices
# TODO: add a way to save the conversation
