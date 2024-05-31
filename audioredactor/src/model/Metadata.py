from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC


class Metadata:
    image = "pictures/icon.png"

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
        self.audio = MP3(file_path, ID3=ID3)

    def get_title(self):
        if self.audio:
            return self.audio.tags['TIT2'].text[0]
        return None

    def get_artist(self):
        if self.audio:
            return self.audio.tags['TPE1'].text[0]
        return None

    def load_art(self):
        for tag in self.audio.tags.values():
            if isinstance(tag, APIC):
                with open(image, 'wb') as img:
                    img.write(tag.data)
                return
        return None

    def get_tags(self):
        if self.audio:
            return self.audio.tags
        return None
