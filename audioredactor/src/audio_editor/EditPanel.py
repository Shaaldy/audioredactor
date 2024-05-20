from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit


class EditPanel(QWidget):
    def __init__(self, sound_handler):
        super().__init__()
        self.sound_handler = sound_handler
        self.initUI()

    def initUI(self):
        self.open_btn = self.create_button('Open', self.sound_handler.open_sound)
        self.undo_btn = self.create_button('Undo', self.get_undo, False)
        self.redo_btn = self.create_button('Redo', self.get_redo, False)
        self.speed_btn = self.create_button('Change Speed', self.get_speed, False)
        self.speed_entry = self.create_line_edit(False, "Укажите число", '1.0')
        self.reverse_btn = self.create_button('Reverse', self.get_reverse, False)
        self.overlay_btn = self.create_button('Overlay', self.get_overlay, False)
        self.merge_btn = self.create_button('Merge', self.get_merge, False)
        self.volume_btn = self.create_button('Change Volume', self.get_volume, False)
        self.volume_entry = self.create_line_edit(False, "Укажите на сколько увеличить или уменьшить громкость в дБ", '0')
        self.slice_btn = self.create_button('Slice', self.get_slice, False)
        self.first_slice_entry = self.create_line_edit(False, "Укажите в секундах первую границу")
        self.second_slice_entry = self.create_line_edit(False, "Укажите в секундах вторую границу")
        self.fade_in_btn = self.create_button('Fade In', self.get_fade_in, False)
        self.fade_in_entry = self.create_line_edit(False, "Укажите в секундах длительность эффекта")
        self.fade_out_btn = self.create_button('Fade Out', self.get_fade_out, False)
        self.fade_out_entry = self.create_line_edit(False, "Укажите в секундах длительность эффекта")
        self.repeat_btn = self.create_button('Repeat', self.get_repeat, False)
        self.repeat_entry = self.create_line_edit(False, "Укажите количество повторов", '0')
        self.save_btn = self.create_button('Save', self.sound_handler.save, False)

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
        self.setLayout(self.main_layout)

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

    def create_line_edit(self, enabled=True, tooltip=None, text=None):
        line_edit = QLineEdit()
        line_edit.setEnabled(enabled)
        if tooltip:
            line_edit.setToolTip(tooltip)
        if text:
            line_edit.setText(text)
        return line_edit

    # Add methods for undo, redo, speed, reverse, overlay, merge, volume, slice, fade in/out, repeat, save
    def get_undo(self):
        self.sound_handler.song.undo()
        self.parent().update_list()

    def get_redo(self):
        self.sound_handler.song.redo()
        self.parent().update_list()

    def get_speed(self):
        speed_arg = self.speed_entry.text()
        try:
            speed_arg = float(speed_arg)
        except ValueError:
            speed_arg = None
        if speed_arg is not None and speed_arg > 0:
            self.sound_handler.song.speed_change(speed_arg)
            self.parent().update_list()
        else:
            self.parent().make_warning_msg('Please write a right value!', "WARNING")

    def get_reverse(self):
        self.sound_handler.song.reverse_sound()
        self.parent().update_list()

    def get_overlay(self):
        try:
            self.sound_handler.song.overlay()
            self.parent().update_list()
        except FileNotFoundError:
            self.parent().make_warning_msg('Please choose a file!', "WARNING")

    def get_merge(self):
        try:
            self.sound_handler.song.merge()
            self.parent().update_list()
        except FileNotFoundError:
            self.parent().make_warning_msg('Please choose a file!', "WARNING")

    def get_volume(self):
        vol_arg = self.volume_entry.text()
        try:
            vol_arg = float(vol_arg)
        except ValueError:
            vol_arg = None
        if vol_arg is not None:
            self.sound_handler.song.volume_change(vol_arg)
            self.parent().update_list()
        else:
            self.parent().make_warning_msg('Please write a right value!', "WARNING")

    def get_slice(self):
        try:
            begin = self.first_slice_entry.text().strip()
            end = self.second_slice_entry.text().strip()

            begin = float(begin) if begin else None
            end = float(end) if end else None

            if begin is None and end is None:
                raise ValueError("At least one of 'begin' or 'end' must be specified.")

            if begin is not None and end is not None and begin >= end:
                raise ValueError("Begin value must be less than end value.")

            self.sound_handler.song.slice(begin, end)
            self.parent().update_list()
        except ValueError as e:
            self.parent().make_warning_msg(f'Invalid input: {e}', "WARNING")

    def get_fade_in(self):
        value = self.fade_in_entry.text()
        try:
            value = float(value)
        except ValueError:
            value = None
        if value is not None and value > 0:
            self.sound_handler.song.fade_in(value)
            self.parent().update_list()
        else:
            self.parent().make_warning_msg('Please write a right value!', "WARNING")

    def get_fade_out(self):
        value = self.fade_out_entry.text()
        try:
            value = float(value)
        except ValueError:
            value = None
        if value is not None and value > 0:
            self.sound_handler.song.fade_out(value)
            self.parent().update_list()
        else:
            self.parent().make_warning_msg('Please write a right value!', "WARNING")

    def get_repeat(self):
        times = self.repeat_entry.text()
        try:
            times = int(times)
        except ValueError:
            times = None
        if times is not None and times >= 0:
            self.sound_handler.song.repeat_sound(times)
            self.parent().update_list()
        else:
            self.parent().make_warning_msg('Please write a right value!', "WARNING")