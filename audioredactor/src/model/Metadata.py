from mutagen.mp3 import MP3
from mutagen import id3 as mu

class Metadata:
    def __init__(self, file_path=None):
        self.file_path = file_path
        if file_path is None:
            self.audio = None
            self.title = None
            self.artist = None
        else:
            self.__load_audio__(file_path)

    def __load_audio__(self, file_path):
        self.file_path = file_path
        self.audio = MP3(file_path)

    def get_title(self):
        if self.audio:
            return self.audio.tags['TIT2'].text[0]
        return None

    def get_artist(self):
        if self.audio:
            return self.audio.tags['TPE1'].text[0]
        return None

    def get_tags(self):
        if self.audio:
            return self.audio.tags
        return None