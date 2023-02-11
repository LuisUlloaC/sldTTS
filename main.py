import os
import sys
import pyglet
import requests
import datetime
from io import open
from gtts import gTTS
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import uic


class Sesion(QDialog):
    def __init__(self):
        super(Sesion, self).__init__()
        uic.loadUi(os.getcwd() + "\sesion.ui", self)
        self.login.clicked.connect(self.auth)





    def auth(self):

        def generarArchivo():
            if not os.path.exists("files"):
                os.mkdir("files")
            if not os.path.exists("files logs"):
                os.mkdir("files logs")

            try:
                tts = gTTS(text=self.userLine.text(), lang='es')
                print("Estos es el tts   " + str(tts.GOOGLE_TTS_HEADERS) + " otro        " + str(tts.lang) )
                tts.save("files/" + self.proxyLine.text() + ".mp3")
            except Exception as err:
                file = open("files logs/errorLog.txt", "w")
                file.write(str(err))
                file.close()
                raise err





        proxy = {
            'http': 'http://' + self.userLine.text() + ':'+ self.passwordLine.text() + '@' + self.proxyLine.text() + ':' + self.portLine.text() + '/'
        }
        if not os.path.exists("proxy logs"):
            os.mkdir("proxy logs")

        try:
            r = requests.get('http://www.dpsca.cmw.sld.cu/', proxies = proxy)
            user = requests.Session()
            user.proxies.update(proxy)
            user.post(generarArchivo())
            




            file = open("proxy logs/SuccessLog.txt", "w")
            file.write(str(f'Status Code: {r.status_code}' + '  ' + str(datetime.datetime.today()) + "User: " + self.userLine.text() ) )
            file.write("\n")
            file.write("\n")
            file.close()
            main = Mainwindow()
            main.exec()
        except Exception as err:
            file = open("proxy logs/errorLog.txt", "w")
            file.write(str(err))
            file.write("\n")
            file.write("\n")
            file.close()
            main = Mainwindow()
            main.exec()
            raise err


class Mainwindow(QDialog):
    def __init__(self):
        super(Mainwindow, self).__init__()
        uic.loadUi(os.getcwd() + "\window.ui", self)
        self.createFile.clicked.connect(self.generarArchivo)
        self.playFile.clicked.connect(self.play)

    def generarArchivo(self):
        if not os.path.exists("files"):
            os.mkdir("files")
        if not os.path.exists("files logs"):
            os.mkdir("files logs")
        
        try:
            tts = gTTS(text=self.textEdit.toPlainText(), lang='es')
            print("Estos es el tts   " + str(tts.GOOGLE_TTS_HEADERS) + " otro        " + str(tts.lang) )
            tts.save("files/" + self.lineEdit.text() + ".mp3")
        except Exception as err:
            file = open("files logs/errorLog.txt", "w")
            file.write(str(err))
            file.close()
            raise err

    def play(self):
        music = pyglet.resource.media("files/" + self.lineEdit.text() + ".mp3")
        music.play()
        pyglet.app.run()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    _win = Sesion()
    _win.show()
    app.exec()
