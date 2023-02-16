import os
import sys
import pyglet
import requests
from datetime import datetime
from io import open
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import uic

globalUser = {}

class Sesion(QDialog):
    def __init__(self):
        super(Sesion, self).__init__()
        uic.loadUi(os.getcwd() + "\sesion.ui", self)
        self.login.clicked.connect(self.auth)

    def auth(self):
        if not os.path.exists("proxy logs"):
            os.mkdir("proxy logs")
        try:
            globalUser['http'] = 'http://' + self.userLine.text() + ':'+ self.passwordLine.text() + '@' + self.proxyLine.text() + ':' + self.portLine.text() + '/'
            print("En auth: " + str(globalUser))
            requests.get('http://www.dpsca.cmw.sld.cu/', proxies = globalUser)
            main = Mainwindow()
            main.exec()
        except Exception as err:
            try:
                open("proxy logs/errorLog.txt")
                main = Mainwindow()
                main.exec()
            except:
                open("proxy logs/errorLog.txt", 'w')
                print("No abrio")
                main = Mainwindow()
                main.exec()
            finally:
                file = open("proxy logs/errorLog.txt", "a")
                file.write(str(datetime.now) + "  " + str(err))
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
        genFileRemoteURL = 'http://lepolle33.pythonanywhere.com/gtts/es/' + self.textEdit.toPlainText() + '/' + self.lineEdit.text()
        downloadFileRemoteURL = 'http://lepolle33.pythonanywhere.com/gtts/descargar/' + self.lineEdit.text() + '.mp3/'
        print("URL crear archivo: " + genFileRemoteURL)
        print("URL descargar archivo: " + downloadFileRemoteURL)
        print("Dict with proxy: " + str(globalUser))
        if not os.path.exists("files"):
            os.mkdir("files")
        if not os.path.exists("files logs"):
            os.mkdir("files logs")
        
        try:
            requests.get(genFileRemoteURL, proxies=globalUser)
            data = requests.get(downloadFileRemoteURL, proxies=globalUser)
            localFile = 'files/' + self.lineEdit.text() + '.mp3'
            with open(localFile, 'wb') as file:
                file.write(data.content)
        except Exception as err:
            try:
                open("files logs/errorLog.txt")
            except:
                open("files logs/errorLog.txt", 'w')
                print("No abrio")
            finally:
                file = open("files logs/errorLog.txt", "a")
                file.app(str(err))
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
