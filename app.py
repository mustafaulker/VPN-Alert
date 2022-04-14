import copy
import time
import urllib.request

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget, QTextEdit

external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()

        self.activate_button = QPushButton("Activate")
        self.textArea = QTextEdit()
        self.effect = QSoundEffect()

        self.textArea.setReadOnly(True)

        self.effect.setSource(QUrl.fromLocalFile("beep.wav"))
        self.effect.setLoopCount(-2)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("VPN Alert")
        self.resize(450, 300)
        self.ui_components()
        self.show()

    def ui_components(self):
        layout = QVBoxLayout()

        self.activate_button.clicked.connect(self.start)
        self.activate_button.setCheckable(True)

        layout.addWidget(self.textArea)
        layout.addWidget(self.activate_button)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

    def start(self):
        if self.activate_button.isChecked():
            self.activate_button.setText("Deactivate")

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
            self.activate_button.setText("Activate")
            print("Alert has deactivated at: " + time.strftime("%H:%M:%S"))


app = QApplication([])
window = Main()
app.exec()
