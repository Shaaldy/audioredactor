import unittest
from unittest.mock import MagicMock, patch
from model.Metadata import Metadata


class TestMetadata(unittest.TestCase):
    @patch('model.Metadata.MP3')
    def test_load_audio(self, mock_mp3):
        mock_audio = MagicMock()
        mock_mp3.return_value = mock_audio

        metadata = Metadata('test_song.mp3')

        mock_mp3.assert_called_once_with('test_song.mp3')
        self.assertEqual(metadata.audio, mock_audio)
        self.assertEqual(metadata.file_path, 'test_song.mp3')

    @patch('model.Metadata.MP3')
    def test_get_title(self, mock_mp3):
        mock_audio = MagicMock()
        mock_audio.tags = {'TIT2': MagicMock(text=['Дорадура'])}
        mock_mp3.return_value = mock_audio

        metadata = Metadata('test_song.mp3')
        title = metadata.get_title()

        self.assertEqual(title, 'Дорадура')

    @patch('model.Metadata.MP3')
    def test_get_artist(self, mock_mp3):
        mock_audio = MagicMock()
        mock_audio.tags = {'TPE1': MagicMock(text=['дора'])}
        mock_mp3.return_value = mock_audio

        metadata = Metadata('test_song.mp3')
        artist = metadata.get_artist()

        self.assertEqual(artist, 'дора')

    @patch('model.Metadata.MP3')
    def test_get_tags(self, mock_mp3):
        mock_audio = MagicMock()
        mock_tags = {'TIT2': MagicMock(text=['Дорадура']), 'TPE1': MagicMock(text=['дора'])}
        mock_audio.tags = mock_tags
        mock_mp3.return_value = mock_audio

        metadata = Metadata('test_song.mp3')
        tags = metadata.get_tags()

        self.assertEqual(tags, mock_tags)


if __name__ == '__main__':
    unittest.main()
