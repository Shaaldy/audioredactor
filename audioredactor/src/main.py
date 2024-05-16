from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QFileDialog, QVBoxLayout,
                             QHBoxLayout, QListWidget, QScrollBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from sound import *
from pygame import mixer

global paused
paused = False


class AudioEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.song = Sound()
        self.paused = False

        mixer.init()

        self.setWindowTitle('Audio Editor')
        self.setGeometry(100, 100, 700, 700)
        self.setStyleSheet('background-color: grey;')
        self.initUI()

    def initUI(self):
        self.create_buttons()
        self.create_layouts()
        self.setLayout(self.main_layout)

    def create_buttons(self):
        self.open_btn = self.create_button('Open', self.open_sound)
        self.undo_btn = self.create_button('Undo', self.get_undo, False)
        self.redo_btn = self.create_button('Redo', self.get_redo, False)
        self.speed_btn = self.create_button('Change Speed', self.get_speed, False)
        self.speed_entry = self.create_line_edit(False)
        self.reverse_btn = self.create_button('Reverse', self.get_reverse, False)
        self.overlay_btn = self.create_button('Overlay', self.get_overlay, False)
        self.merge_btn = self.create_button('Merge', self.get_merge, False)
        self.volume_btn = self.create_button('Change Volume', self.get_volume, False)
        self.volume_entry = self.create_line_edit(False)
        self.slice_btn = self.create_button('Slice', self.get_slice, False)
        self.first_slice_entry = self.create_line_edit(False)
        self.second_slice_entry = self.create_line_edit(False)
        self.fade_in_btn = self.create_button('Fade In', self.get_fade_in, False)
        self.fade_in_entry = self.create_line_edit(False)
        self.fade_out_btn = self.create_button('Fade Out', self.get_fade_out, False)
        self.fade_out_entry = self.create_line_edit(False)
        self.repeat_btn = self.create_button('Repeat', self.get_repeat, False)
        self.repeat_entry = self.create_line_edit(False)
        self.save_btn = self.create_button('Save', self.song.save, False)

        self.play_btn = self.create_button(icon='1.png', slot=self.play, enabled=False)
        self.pause_btn = self.create_button(icon='2.png', slot=self.pause, enabled=False)
        self.stop_btn = self.create_button(icon='3.png', slot=self.stop, enabled=False)

    def create_layouts(self):
        self.main_layout = QVBoxLayout()

        self.main_layout.addWidget(self.open_btn)
        self.main_layout.addWidget(self.undo_btn)
        self.main_layout.addWidget(self.redo_btn)

        speed_layout = QHBoxLayout()
        speed_layout.addWidget(self.speed_btn)
        speed_layout.addWidget(self.speed_entry)
        self.main_layout.addLayout(speed_layout)

        self.main_layout.addWidget(self.reverse_btn)
        self.main_layout.addWidget(self.overlay_btn)
        self.main_layout.addWidget(self.merge_btn)

        volume_layout = QHBoxLayout()
        volume_layout.addWidget(self.volume_btn)
        volume_layout.addWidget(self.volume_entry)
        self.main_layout.addLayout(volume_layout)

        slice_layout = QHBoxLayout()
        slice_layout.addWidget(self.slice_btn)
        slice_layout.addWidget(self.first_slice_entry)
        slice_layout.addWidget(self.second_slice_entry)
        self.main_layout.addLayout(slice_layout)

        fade_in_layout = QHBoxLayout()
        fade_in_layout.addWidget(self.fade_in_btn)
        fade_in_layout.addWidget(self.fade_in_entry)
        self.main_layout.addLayout(fade_in_layout)

        fade_out_layout = QHBoxLayout()
        fade_out_layout.addWidget(self.fade_out_btn)
        fade_out_layout.addWidget(self.fade_out_entry)
        self.main_layout.addLayout(fade_out_layout)

        repeat_layout = QHBoxLayout()
        repeat_layout.addWidget(self.repeat_btn)
        repeat_layout.addWidget(self.repeat_entry)
        self.main_layout.addLayout(repeat_layout)

        self.main_layout.addWidget(self.save_btn)

        list_layout = QHBoxLayout()
        self.listbox = QListWidget()
        list_layout.addWidget(self.listbox)

        self.scrollbar = QScrollBar()
        self.scrollbar.setOrientation(Qt.Orientation.Vertical)
        list_layout.addWidget(self.scrollbar)
        self.main_layout.addLayout(list_layout)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.play_btn)
        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.stop_btn)
        self.main_layout.addLayout(control_layout)

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

    def create_line_edit(self, enabled=True):
        line_edit = QLineEdit()
        line_edit.setEnabled(enabled)
        return line_edit

    def check_undo_redo_buttons(self):
        self.undo_btn.setEnabled(self.song.can_undo())
        self.redo_btn.setEnabled(self.song.can_redo())

    def update_list(self):
        self.listbox.clear()
        self.listbox.addItems(self.song.history_stack)

    def get_reverse(self):
        self.song.reverse_sound()
        self.update_list()

    def get_undo(self):
        self.song.undo()
        self.update_list()

    def get_redo(self):
        self.song.redo()
        self.update_list()

    def get_overlay(self):
        self.song.overlay()
        self.update_list()

    def get_merge(self):
        self.song.merge()
        self.update_list()

    def get_repeat(self):
        times = int(self.repeat_entry.text())
        self.song.repeat_sound(times)
        self.update_list()

    def get_fade_out(self):
        value = float(self.fade_out_entry.text())
        self.song.fade_out(value)
        self.update_list()

    def get_fade_in(self):
        value = float(self.fade_in_entry.text())
        self.song.fade_in(value)
        self.update_list()

    def get_slice(self):
        begin = float(self.first_slice_entry.text())
        end = float(self.second_slice_entry.text())
        self.song.slice(begin, end)
        self.update_list()

    def get_volume(self):
        vol_arg = float(self.volume_entry.text())
        self.song.volume_change(vol_arg)
        self.update_list()

    def get_speed(self):
        try:
            speed_arg = float(self.speed_entry.text())
            if speed_arg > 0:
                self.song.speed_change(speed_arg)
                self.update_list()
            else:
                raise ValueError("Speed must be a positive number")
        except ValueError as e:
            print(f"Invalid input for speed: {e}")

    from PyQt6.QtWidgets import QMessageBox

    def open_sound(self):
        path, _ = QFileDialog.getOpenFileName(self, "What file do you want to import?", "/home/",
                                              "MP3 Files (*.mp3);;All Files (*)")
        if path:
            self.song.filePath = path
            self.song.track = AudioSegment.from_mp3(path)
            self.enable_controls()

    def enable_controls(self):
        self.play_btn.setEnabled(True)
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        self.undo_btn.setEnabled(True)
        self.redo_btn.setEnabled(True)
        self.speed_btn.setEnabled(True)
        self.speed_entry.setEnabled(True)
        self.reverse_btn.setEnabled(True)
        self.overlay_btn.setEnabled(True)
        self.merge_btn.setEnabled(True)
        self.volume_btn.setEnabled(True)
        self.volume_entry.setEnabled(True)
        self.slice_btn.setEnabled(True)
        self.first_slice_entry.setEnabled(True)
        self.second_slice_entry.setEnabled(True)
        self.fade_in_btn.setEnabled(True)
        self.fade_in_entry.setEnabled(True)
        self.fade_out_btn.setEnabled(True)
        self.fade_out_entry.setEnabled(True)
        self.repeat_btn.setEnabled(True)
        self.repeat_entry.setEnabled(True)
        self.save_btn.setEnabled(True)

    def play(self):
        self.song.track.export("song.mp3", format="mp3")
        mixer.music.load("song.mp3")
        mixer.music.play(loops=0)

    def stop(self):
        mixer.music.stop()

    def pause(self):
        global paused
        if self.paused:
            mixer.music.unpause()
            self.paused = False
        else:
            mixer.music.pause()
            self.paused = True


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ex = AudioEditor()
    ex.show()
    sys.exit(app.exec())


