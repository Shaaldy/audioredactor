from audio_editor.AudioEditor import AudioEditor
from PyQt6.QtWidgets import QApplication
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = AudioEditor()
    ex.show()
    sys.exit(app.exec())
