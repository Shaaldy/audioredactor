from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QTimer
from pydub import AudioSegment
from pygame import mixer
from model.Sound import Sound
from model.Metadata import Metadata


class SoundHandler:
    def __init__(self, timeline, parent=None):
        self.timeline = timeline
        self.song = Sound(self.timeline)
        mixer.init()
        self.parent = parent
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timeline)
        self.log_msg = None

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

    def play(self, play_btn):
        self.song.track.export("song.mp3", format="mp3", bitrate="320k", codec="libmp3lame", parameters=["-v", "0"])
        mixer.music.load("song.mp3")
        mixer.music.play(loops=0)
        play_btn.setEnabled(False)
        self.timer.start(1000)

    def pause(self):
        mixer.music.pause()

    def unpause(self):
        mixer.music.unpause()
        self.timer.start()

    def stop(self):
        self.pause()
        self.timer.stop()

    def update_timeline(self):
        if mixer.music.get_busy():
            current_time = mixer.music.get_pos() // 1000
            self.parent.timeline.set_value(current_time)
        else:
            self.timer.stop()
