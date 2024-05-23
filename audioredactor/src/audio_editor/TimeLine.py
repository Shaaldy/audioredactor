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
        self.update_slider_stylesheet()

    def update_slider_stylesheet(self):
        # Update the stylesheet to fill the passed distance
        style = """
           QSlider::groove:horizontal {
               background: #444444;  /* Background color of the groove */
               height: 10px;
               border-radius: 5px;
           }

           QSlider::sub-page:horizontal {
               background: #1E90FF;  /* Color of the filled area */
               height: 10px;
               border-radius: 5px;
           }

           QSlider::add-page:horizontal {
               background: #aaaaaa;  /* Color of the unfilled area */
               height: 10px;
               border-radius: 5px;
           }

           QSlider::handle:horizontal {
               background: #ffffff;  /* Color of the handle */
               border: 1px solid #5c5c5c;
               width: 14px;
               height: 14px;
               margin: -2px 0;
               border-radius: 7px;
           }
           """
        self.timeline_slider.setStyleSheet(style)

    def set_maximum(self, max_value):
        self.timeline_slider.setMaximum(int(max_value))
        minutes = int(max_value // 60)
        seconds = int(max_value % 60)
        self.total_time_label.setText(f"{minutes}:{seconds:02}")

    def set_value(self, value):
        self.timeline_slider.setValue(value)
        self.current_time_label.setText(f"{value // 60}:{value % 60:02}")
