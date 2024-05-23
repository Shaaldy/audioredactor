from .EditPanel import EditPanel
from PyQt6.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout,
                             QHBoxLayout, QListWidget, QScrollBar, QDialog)
from PyQt6.QtCore import Qt
from .SoundHandler import SoundHandler
from .ControlPanel import ControlPanel
from .TimeLine import TimeLine


# Сделать френдли
class AudioEditor(QWidget):
    
    def __init__(self):
        super().__init__()
        self.timeline = TimeLine(self)
        self.sound_handler = SoundHandler(self.timeline, self)
        self.setWindowTitle('Audio Editor')
        self.setGeometry(400, 100, 600, 650)
        self.setStyleSheet('background-color: #2E2E2E; color: #FFFFFF; font-size: 16px;')

        self.initUI()

    def initUI(self):
        self.control_panel = ControlPanel(self.sound_handler)
        self.edit_panel = EditPanel(self.sound_handler)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.edit_panel)
        self.main_layout.addWidget(self.control_panel)

        list_layout = QHBoxLayout()
        self.listbox = QListWidget()
        list_layout.addWidget(self.listbox)


        self.main_layout.addWidget(self.timeline)

        self.scrollbar = QScrollBar()
        self.scrollbar.setOrientation(Qt.Orientation.Vertical)
        list_layout.addWidget(self.scrollbar)
        self.main_layout.addLayout(list_layout)


        self.setLayout(self.main_layout)

    def update_list(self):
        self.listbox.clear()
        self.listbox.addItems(self.sound_handler.song.history_stack)

    def enable_controls(self):
        self.control_panel.play_btn.setEnabled(True)
        self.control_panel.pause_btn.setEnabled(True)
        self.control_panel.stop_btn.setEnabled(True)
        self.edit_panel.undo_btn.setEnabled(True)
        self.edit_panel.redo_btn.setEnabled(True)
        self.edit_panel.speed_btn.setEnabled(True)
        self.edit_panel.speed_entry.setEnabled(True)
        self.edit_panel.reverse_btn.setEnabled(True)
        self.edit_panel.overlay_btn.setEnabled(True)
        self.edit_panel.merge_btn.setEnabled(True)
        self.edit_panel.volume_btn.setEnabled(True)
        self.edit_panel.volume_entry.setEnabled(True)
        self.edit_panel.slice_btn.setEnabled(True)
        self.edit_panel.first_slice_entry.setEnabled(True)
        self.edit_panel.second_slice_entry.setEnabled(True)
        self.edit_panel.fade_in_btn.setEnabled(True)
        self.edit_panel.fade_in_entry.setEnabled(True)
        self.edit_panel.fade_out_btn.setEnabled(True)
        self.edit_panel.fade_out_entry.setEnabled(True)
        self.edit_panel.repeat_btn.setEnabled(True)
        self.edit_panel.repeat_entry.setEnabled(True)
        self.edit_panel.save_btn.setEnabled(True)

    def make_warning_msg(self, message, title):
        win = QDialog(self)
        win.setWindowTitle(title)
        win.setGeometry(100, 100, 250, 60)

        layout = QVBoxLayout()
        label = QLabel(message)
        label.setStyleSheet("color: red;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        btn = QPushButton('OK')
        btn.clicked.connect(win.accept)
        layout.addWidget(btn)

        win.setLayout(layout)
        win.exec()
