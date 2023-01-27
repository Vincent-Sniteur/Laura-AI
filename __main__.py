# Imports
from laura import ChatGPT
import os
import speech_recognition as sr
import pyttsx3

# Constants
# Set the language of the assistant
voice = 'french+f4'
# Initializing the recognizer
r = sr.Recognizer()

# play audio function
def play(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('voice', voice)
    engine.say(text)
    engine.runAndWait()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

#  Starting the assistant and asking for the session token and the conversation id
# If the conversation id is not provided, a new conversation will be created
if __name__ == '__main__':
    while True:
        session_token = input('\nLaura: Bonjour Humain, merci de mettre votre session token ! ')
        conversation_id = input('\nLaura: Entrer un ID de conversation ? Sinon laisser vide... ')
        chat = ChatGPT(session_token, conversation_id)
        break
    while True:
        # Starting the microphone and waiting for the user to say "Laura" wait for the user to say "Laura" to start the conversation
        with sr.Microphone() as source:
            print("Dites 'Ok Laura' pour m'activer...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        # Recognize the user's voices
        try:
            prompt = r.recognize_google(audio, language='fr-FR')
            # if user says "reset" the assistant resets the conversation
            if 'reset' in prompt.lower():
                chat.reset_conversation()
                clear_screen()
                print(
                    'Bonjour je suis Laura votre Assistant. Mes commandes sont "Ok Laura" pour commencer. "Stop" pour arrêter. "Reset" pour supprimer la discussion.\n'
                )
                continue
            #  If user says "stop" the assistant stops
            if 'stop' in prompt.lower():
                response = "Au revoir!"
                play(response) # play audio
                print('\nLaura: ', response)
                break
            # If user says "ok laura" the assistant starts listening to the user's question
            if 'ok laura' in prompt.lower():
                print('\nLaura: ', "Je vous écoute...")
                while True:
                    with sr.Microphone() as source:
                        r.adjust_for_ambient_noise(source)
                        audio = r.listen(source)
                    # Recognize the user's question
                    try:
                        # Recognize the user's question
                        prompt = r.recognize_google(audio, language='fr-FR')
                        # If user says "stop" the assistant stops
                        if 'stop' in prompt.lower():
                            response = "Au revoir!"
                            print('\nLaura: ', response)
                            play(response)
                            break
                        # Laura say to wait
                        print('\nLaura: ', "Je réfléchis...")
                        # Laura answers the user's question
                        response = chat.send_message(prompt)
                        print('\nLaura: ', response['message'], end='')
                        play(response['message']) # play audio
                        break
                    except sr.UnknownValueError:
                        print('\nLaura: ', 'Désolé, je n ai pas compris votre question.')
                    except sr.RequestError as e:
                        print("Erreur de reconnaissance vocale; {0}".format(e))
        except sr.UnknownValueError:
            print('\nLaura: ', 'Désolé, je n ai pas compris votre question.')
        except sr.RequestError as e:
            print("Erreur de reconnaissance vocale; {0}".format(e))