"""
Author: Vincent - Sniteur
Date:   2023-01-25
"""

import speech_recognition as sr
import openai
import configparser
import pyttsx3

# # read config file
config = configparser.ConfigParser()
config.read('config.ini')
api_keys = config['openai']['api_key']

# # openai api key
openai.api_key = api_keys

# Set the language of the assistant
language = 'fr-FR,fr'
voice = 'fr-FR-Wavenet-A'

# Set model of the assistant
model = 'text-davinci-003'

# Initializing the recognizer
r = sr.Recognizer()


# play audio function
def play(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('voice', voice)
    engine.say(text)
    engine.runAndWait()


# Infinite loop to keep the assistant running until the user says "stop" or "laura"
while True:
    # Starting the microphone and waiting for the user to say "Laura"
    with sr.Microphone() as source:
        print("Dites 'Ok Laura' pour m'activer...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    # Recognize the user's voices
    try:
        transcribed_text = r.recognize_google(audio, language='fr-FR')
        #  If user says "stop" the assistant stops
        if "stop" in transcribed_text.lower():
            print("Au revoir!")
            play("Au revoir!") # play audio
            break
        # If user says "ok laura" the assistant starts listening to the user's question
        if "ok laura" in transcribed_text.lower():
            print("Je vous écoute...")
            play("Je vous écoute...") # play audio
            while True:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                # Recognize the user's question
                    try:
                        question = r.recognize_google(audio, language='fr-FR')
                        print("Vous avez demandé: ", question)
                        response = openai.Completion.create(
                            engine=model,
                            prompt=question,
                            temperature=0,
                            max_tokens=100,
                            top_p=1,
                            frequency_penalty=0.0,
                            presence_penalty=0.0,
                            stop=["\n"]
                        )
                        answer = response.choices[0].text
                        print("Réponse: ", answer)
                        play(answer)
                        if "stop" in question.lower():
                            print("Au revoir!")
                            play("Au revoir!")  # play audio
                            break
                    except sr.UnknownValueError:
                        print("Désolé, je n'ai pas compris votre question.")
                        play("Désolé, je n'ai pas compris votre question.") # play audio
                    except sr.RequestError as e:
                        print("Erreur de reconnaissance vocale; {0}".format(e))
    except sr.UnknownValueError:
        print("Désolé, je n'ai pas reconnu votre commande.")
    except sr.RequestError as e:
        print("Erreur de reconnaissance vocale; {0}".format(e))
