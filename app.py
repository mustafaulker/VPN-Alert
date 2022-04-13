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

        global effect
        effect = QSoundEffect()
        effect.setSource(QUrl.fromLocalFile("beep.wav"))
        effect.setLoopCount(-2)

        global start_button
        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start)

        start_button.setCheckable(True)

        self.setCentralWidget(start_button)

    def start(self):
        if start_button.isChecked():
            start_button.setText("Stop")

            global external_ip
            current_external_ip = copy.copy(external_ip)
            
            print("Alert has activated at: " + time.strftime("%H:%M:%S"))

            while current_external_ip == external_ip:
                current_external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
                time.sleep(2)

            print("Discconected from VPN at: " + time.strftime("%H:%M:%S"))
            effect.play()
        else:
            effect.stop()
            start_button.setText("Start")
            print("Alert has deactivated at: " + time.strftime("%H:%M:%S"))


app = QApplication([])

window = Main()
window.show()

app.exec()
