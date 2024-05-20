from PyQt6.QtWidgets import QFileDialog
from pydub import AudioSegment
from pygame import mixer
from model.sound import Sound


class SoundHandler:
    def __init__(self, parent=None):
        self.song = Sound()
        mixer.init()
        self.parent = parent

    def open_sound(self):
        try:
            path, _ = QFileDialog.getOpenFileName(self.parent, "What file do you want to import?", "/home/",
                                                  "MP3 Files (*.mp3);;All Files (*)")
            if not path:
                raise ValueError("No file selected")
            self.song.filePath = path
            self.song.track = AudioSegment.from_mp3(path)
            self.parent.enable_controls()
        except Exception as e:
            self.parent.make_warning_msg(f"Failed to open sound file: {e}", "WARNING")

    def save(self):
        self.song.save()

    def play(self, play_btn):
        self.song.track.export("song.mp3", format="mp3")
        mixer.music.load("song.mp3")
        mixer.music.play(loops=0)
        play_btn.setEnabled(False)

    def pause(self):
        mixer.music.pause()

    def unpause(self):
        mixer.music.unpause()

    def stop(self):
        self.pause()
