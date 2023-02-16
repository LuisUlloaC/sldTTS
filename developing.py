from gtts import gTTS
from io import BytesIO

file = open("leer.txt", "r")
print(file.read)

tts = gTTS(text=file.read(), lang='es')
tts.save("test" + ".mp3")


"""import pyglet

music = pyglet.resource.media("test" + ".mp3")
music.play()
pyglet.app.run()"""