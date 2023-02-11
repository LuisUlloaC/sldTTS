from gtts import gTTS
from io import BytesIO

textInput = "Hola a todos . Oracion de prueba"
nombreAudio = "Defaul"

tts = gTTS(text=textInput, lang='es')
tts.save(nombreAudio + ".mp3")


import pyglet

music = pyglet.resource.media(nombreAudio + ".mp3")
music.play()
pyglet.app.run()