from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QTimer, pyqtSignal
from pydub import AudioSegment
from pydub.playback import play
import threading
from model.Sound import Sound
from model.Metadata import Metadata
import time

class SoundHandler:
    def __init__(self, timeline, parent=None):
        super().__init__()
        self.timeline = timeline
        self.song = Sound(self.timeline)
        self.parent = parent
        self.log_msg = None
        self.is_playing = False
        self.play_thread = None

        self.timer_thread = QTimer()
        self.timer_thread.timeout.connect(self.update_timeline)

    def open_sound(self):
        try:
            path, _ = QFileDialog.getOpenFileName(self.parent, "What file do you want to import?", "/home/",
                                                  "MP3 Files (*.mp3);;All Files (*)")
            if not path:
                raise ValueError("No file selected")
            self.song.filePath = path
            self.song.track = AudioSegment.from_mp3(path)
            try:
                metadata = Metadata(path)
                title, artist = metadata.get_title(), metadata.get_artist()
                self.log_msg = f"Opened {title} by {artist}"
            except Exception as e:
                self.log_msg = "Opened changed sound"
            self.song.queue.append(self.song.track)
            self.song.history_stack.append(self.log_msg)
            self.parent.update_list()
            self.timeline.set_maximum(self.song.track.duration_seconds)

            self.parent.enable_controls()
        except Exception as e:
            self.parent.make_warning_msg(f"Failed to open sound file: {e}", "WARNING")
            print(e)

    def save(self):
        self.song.save()

    def play(self, play_btn=None):
        def playback():
            self.is_playing = True
            play(self.song.track)
            self.is_playing = False

        self.play_thread = threading.Thread(target=playback)
        self.play_thread.start()
        play_btn.setEnabled(False)

        self.timer_thread = threading.Thread(target=self.start_timer)
        self.timer_thread.start()

    def start_timer(self):
        while self.is_playing:
            time.sleep(1)
            self.update_timeline()

    def pause(self):
        if self.is_playing:
            self.is_playing = False
            self.play()

    def unpause(self):
        if not self.is_playing:
            self.is_playing = True
            self.play()

    def stop(self):
        self.pause()
        self.timer.stop()

    def update_timeline(self):
        current_time = self.timeline.get_value() + 1
        self.timeline.set_value(current_time)