import copy
import time
import urllib.request

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()

        self.effect = QSoundEffect()
        self.effect.setSource(QUrl.fromLocalFile("beep.wav"))
        self.effect.setLoopCount(-2)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start)

        self.start_button.setCheckable(True)

        self.setCentralWidget(self.start_button)

    def start(self):
        if self.start_button.isChecked():
            self.start_button.setText("Stop")

            global external_ip
            current_external_ip = copy.copy(external_ip)

            print("Alert has activated at: " + time.strftime("%H:%M:%S"))

            while current_external_ip == external_ip:
                current_external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
                time.sleep(2)

            print("Disconnected from the VPN at: " + time.strftime("%H:%M:%S"))
            self.effect.play()
        else:
            self.effect.stop()
            self.start_button.setText("Start")
            print("Alert has deactivated at: " + time.strftime("%H:%M:%S"))


app = QApplication([])

window = Main()
window.show()

app.exec()
