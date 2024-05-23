from PyQt6.QtWidgets import QFileDialog
from pydub import AudioSegment


class Sound:
    def __init__(self, timeline):
        self.filePath = None
        self.track = None
        self.queue = []
        self.stack = []
        self.history_stack = []
        self.history_queue = []
        self.overlayTrack = None
        self.timeline = timeline

    def update_timeline_max(self):
        duration = len(self.track) / 1000
        self.timeline.set_maximum(duration)

    def update_timeline_value(self, value):
        self.timeline.set_value(value)

    def speed_change(self, speed=1.0):
        sound_with_altered_frame_rate = self.track._spawn(self.track.raw_data, overrides={
            "frame_rate": int(self.track.frame_rate * speed)
        })
        self.stack.append(self.track)
        self.history_stack.append(f'Speed changed to {speed}x')
        self.track = sound_with_altered_frame_rate.set_frame_rate(self.track.frame_rate)
        self.update_timeline_max()

    def save(self):
        save_path, _ = QFileDialog.getSaveFileName(
            None,
            "Where do you want to save the modified file?",
            "/home/",
            "MP3 files (*.mp3);;All files (*.*)"
        )
        if save_path:
            self.track.export(save_path, bitrate="320k", format="mp3")

    def volume_change(self, vol):
        self.stack.append(self.track)
        self.history_stack.append(f'Volume changed by {vol} dB')
        self.track = self.track.apply_gain(vol)

    def slice(self, begin, end):
        ms1 = begin * 1000
        ms2 = end * 1000
        self.stack.append(self.track)
        self.history_stack.append(f'Sliced from {begin} to {end}')
        self.track = self.track[ms1:ms2]
        self.update_timeline_max()
        #self.timeline.set_slice_range(begin, end) "in future"

    def reverse_sound(self):
        self.stack.append(self.track)
        self.history_stack.append('Reversed')
        self.track = self.track.reverse()

    def repeat_sound(self, count):
        self.stack.append(self.track)
        self.history_stack.append(f'Repeat {count} times')
        self.track = self.track * count
        self.update_timeline_max()

    def merge(self):
        path, _ = QFileDialog.getOpenFileName(
            None,
            "What file do you want to import?",
            "/home/",
            "MP3 files (*.mp3);;All files (*.*)"
        )
        if path:
            track = AudioSegment.from_mp3(path)
            s = str(path.split('/')[-1])
            self.stack.append(self.track)
            self.history_stack.append(f'Merge with {s}')
            self.track = self.track + track
            self.update_timeline_max()

    def fade_in(self, seconds):
        ms = int(seconds * 1000)
        self.stack.append(self.track)
        self.history_stack.append(f'Fade in {seconds}s')
        self.track = self.track.fade_in(ms)

    def fade_out(self, seconds):
        ms = int(seconds * 1000)
        self.stack.append(self.track)
        self.history_stack.append(f'Fade out {seconds}s')
        self.track = self.track.fade_out(ms)

    def overlay(self):
        self.stack.append(self.track)
        filePath, _ = QFileDialog.getOpenFileName(
            None,
            "What file do you want to import?",
            "/home/",
            "MP3 files (*.mp3);;All files (*.*)"
        )
        if filePath:
            self.overlayTrack = AudioSegment.from_mp3(filePath)
            name = filePath.split('/')[-1]
            self.history_stack.append(f'Overlay by {name}')
            self.track = self.track.overlay(self.overlayTrack)
            self.update_timeline_max()

    def undo(self):
        self.queue.insert(0, self.track)
        self.track = self.stack.pop()
        self.history_queue.insert(0, self.history_stack.pop())
        self.update_timeline_max()

    def redo(self):
        self.stack.append(self.track)
        self.track = self.queue[0]
        self.queue.pop(0)
        self.history_stack.append(self.history_queue[0])
        self.history_queue.pop(0)
        self.update_timeline_max()
