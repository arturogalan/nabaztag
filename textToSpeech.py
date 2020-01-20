# Google approach, too much time in process the request

# from gtts import gTTS
# import pygame
# from io import BytesIO

# def say(text):
#     tts = gTTS(text=text, lang='es', slow=False)
#     fp = BytesIO()
#     tts.write_to_fp(fp)
#     fp.seek(0)
#     pygame.mixer.init()
#     pygame.mixer.music.load(fp)
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)
# myText = "que pasa tronco como lo llevas"
# say(myText)

# pyttsx3
# import pyttsx3
# engine = pyttsx3.init() # object creation

# """ RATE"""
# rate = engine.getProperty('rate')   # getting details of current speaking rate
# print (rate)                        #printing current voice rate
# engine.setProperty('rate', 150)     # setting up new voice rate


# """VOLUME"""
# volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
# print (volume)                          #printing current volume level
# engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

# """VOICE"""
# voices = engine.getProperty('voices')       #getting details of current voice
# #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
# engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
# # engine.setProperty('voice', 'spanish')

# engine.say("Hola tronco!")
# engine.say('Mi velocidad es ' + str(engine.getProperty('rate')))
# engine.runAndWait()
# engine.stop()

# espeak
import os

text = "eh niño... que haces, quieres jugar?. No te voy a hacer daño"
os.system("amixer set 'Master' 100%")
os.system("espeak -ves+whisper -g4 \"{}\"".format(text))