import os

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

public_ip = os.popen("nslookup myip.opendns.com resolver1.opendns.com").read().split()[-1]


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()

        global effect
        effect = QSoundEffect()
        effect.setSource(QUrl.fromLocalFile("beep.wav"))
        effect.setLoopCount(-2)

        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start)

        start_button.setCheckable(True)

        self.setCentralWidget(start_button)

    def start(self):
        global public_ip
        current_public_ip = ""
        print("Activated")

        while current_public_ip in public_ip:
            current_public_ip = os.popen("nslookup myip.opendns.com resolver1.opendns.com").read().split()[-1]
        print(public_ip, current_public_ip)
        effect.play()


app = QApplication([])

window = Main()
window.show()

app.exec()
