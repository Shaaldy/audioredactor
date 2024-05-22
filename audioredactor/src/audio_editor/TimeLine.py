from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QSlider, QHBoxLayout, QWidget


class TimeLine(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.current_time_label = QLabel('0:00')
        self.timeline_slider = QSlider(Qt.Orientation.Horizontal)
        self.timeline_slider.setMinimum(0)
        self.timeline_slider.setMaximum(1000)
        self.total_time_label = QLabel('0:00')

        layout.addWidget(self.current_time_label)
        layout.addWidget(self.timeline_slider)
        layout.addWidget(self.total_time_label)

        self.setLayout(layout)

    def set_maximum(self, max_value):
        self.timeline_slider.setMaximum(max_value)
        minutes = int(max_value // 60)
        seconds = int(max_value % 60)
        self.total_time_label.setText(f"{minutes}:{seconds:02}")

    def set_value(self, value):
        self.timeline_slider.setValue(value)
        self.current_time_label.setText(f"{value // 60}:{value % 60:02}")
