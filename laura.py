import speech_recognition as sr
import openai
from gtts import gTTS
from pydub import AudioSegment
import configparser

# read config file
config = configparser.ConfigParser()
config.read('config.ini')
api_keys = config['openai']['api_key']

# openai api key
openai.api_key = api_keys

# Set the language of the assistant
language = 'fr'
voice = 'fr-FR-Wavenet-A'

# Set model of the assistant
model = 'davinci'

# Initializing the recognizer
r = sr.Recognizer()

while True:
    # Starting the microphone and waiting for the user to say "Laura"
    with sr.Microphone() as source:
        print("Dites 'Laura' pour m'activer...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    # Recognize the user's voice
    try:
        transcribed_text = r.recognize_google(audio, language='fr-FR')
        if "laura" in transcribed_text.lower():
            print("Je vous écoute...")
            while True:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                    try:
                        question = r.recognize_google(audio, language='fr-FR')
                        print("Vous avez demandé: ", question)
                        response = openai.Completion.create(
                            engine=model,
                            prompt=question,
                            max_tokens=1,
                            n=1,
                            stop=None,
                            temperature=0.5
                        )
                        answer = response.choices[0].text
                        print("Réponse: ", answer)
                        tts = gTTS(answer, lang=language)
                        tts.save("answer.mp3")
                        sound = AudioSegment.from_mp3("answer.mp3")
                        play(sound)
                        if "stop" in question.lower():
                            print("Au revoir!")
                            break
                    except sr.UnknownValueError:
                        print("Désolé, je n'ai pas compris votre question.")
                    except sr.RequestError as e:
                        print("Erreur de reconnaissance vocale; {0}".format(e))
    except sr.UnknownValueError:
        print("Désolé, je n'ai pas reconnu votre commande.")
    except sr.RequestError as e:
        print("Erreur de reconnaissance vocale; {0}".format(e))
