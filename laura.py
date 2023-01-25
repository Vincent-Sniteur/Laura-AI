# Create vocal assistant Laura - auto activate when you say "Laura" and deactivate when you say "stop"
# The assistant will ask your question to chatGPT3 and answer you with voices

import speech_recognition as sr
import pyaudio
import openai
from gtts import gTTS
from pydub import AudioSegment
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

# Set the minimum ratio required for a match
min_ratio = 70

# Initializing the recognizer
r = sr.Recognizer()


# Starting the microphone
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("Dite 'Laura' pour activer l'assistant vocal")
    audio = r.listen(source)

# Function to convert the text to an audio file and play it


def play_audio(text):
    # Use the gTTS library to convert the text to an audio file
    tts = gTTS(text)
    tts.save("response.mp3")
    # Convert mp3 to wav
    sound = AudioSegment.from_mp3("response.mp3")
    sound.export("response.wav", format="wav")
    # Play the converted file using pyaudio
    chunk = 1024
    f = wave.open(r"response.wav", "rb")
    p = pyaudio.PyAudio()
    stream = p.open(
        format=p.get_format_from_width(f.getsampwidth()),
        channels=f.getnchannels(),
        rate=f.getframerate(),
        output=True,
    )
    data = f.readframes(chunk)
    while data:
        stream.write(data)
        data = f.readframes(chunk)
    stream.stop_stream()
    stream.close()
    p.terminate()


# Recognize the user's voice
try:
    transcribed_text = r.recognize_google(audio)
    ratio = fuzz.token_set_ratio(transcribed_text.lower(), "laura")
    if ratio >= min_ratio:
        print("Je vous écoute...")
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            prompt = r.recognize_google(audio)
            print("Votre avez dit: " + prompt)
            # Generate a response
            completion = openai.Completion.create(
                engine=model,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )
            response = completion.choices[0].text
            print("Laura: " + response)
            # Call the function to convert the text to an audio file and play it
            play_audio(response)
        except sr.UnknownValueError:
            print("Je n'ai pas compris votre question")
            # Call the function to convert the text to an audio file and play it
            play_audio("Je n'ai pas compris votre question")
    else:
        print("Vous m'avez appelée ?")
        # Call the function to convert the text to an audio file and play it
        play_audio("Vous m'avez appelée ?")

except sr.UnknownValueError:
    print("Je n'ai pas compris votre question")
    # Call the function to convert the text to an audio file and play it
    play_audio("Je n'ai pas compris votre question")
