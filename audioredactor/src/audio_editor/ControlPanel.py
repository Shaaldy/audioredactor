from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton


class ControlPanel(QWidget):
    def __init__(self, sound_handler):
        super().__init__()
        self.sound_handler = sound_handler
        self.initUI()
        self.paused = False

    def initUI(self):
        self.play_btn = self.create_button(icon='pictures/1.png', slot=self.play, enabled=False)
        self.pause_btn = self.create_button(icon='pictures/2.png', slot=self.pause, enabled=False)
        self.stop_btn = self.create_button(icon='pictures/3.png', slot=self.stop, enabled=False)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.play_btn)
        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.stop_btn)
        self.setLayout(control_layout)

    def create_button(self, text=None, slot=None, enabled=True, icon=None):
        button = QPushButton()
        if text:
            button.setText(text)
        if slot:
            button.clicked.connect(slot)
        if not enabled:
            button.setEnabled(False)
        if icon:
            button.setIcon(QIcon(icon))
        return button

    def play(self):
        self.sound_handler.play(self.play_btn)

    def pause(self):
        if self.paused:
            self.sound_handler.unpause()
            self.paused = False
        else:
            self.sound_handler.pause()
            self.paused = True

    def stop(self):
        self.sound_handler.stop()
        self.paused = True
