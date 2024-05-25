import unittest
from unittest.mock import patch, MagicMock
from pydub.generators import Sine
from pydub import AudioSegment
from model.Sound import Sound


class MockTimeline:
    def set_maximum(self, duration):
        self.maximum = duration

    def set_value(self, value):
        self.value = value


class TestSound(unittest.TestCase):
    def setUp(self):
        self.timeline = MockTimeline()
        self.sound = Sound(self.timeline)
        self.audio = Sine(440).to_audio_segment(duration=1000)  # 1 секунда синусоидального тона
        self.sound.track = self.audio

    def test_update_timeline_max(self):
        self.sound.update_timeline_max()
        self.assertEqual(self.timeline.maximum, 1.0)

    def test_update_timeline_value(self):
        self.sound.update_timeline_value(5)
        self.assertEqual(self.timeline.value, 5)

    def test_speed_change(self):
        self.sound.speed_change(2.0)
        self.assertEqual(len(self.sound.track), len(self.audio) // 2)
        self.assertEqual(self.sound.history_stack[-1], 'Speed changed to 2.0x')

    @patch('model.Sound.QFileDialog.getSaveFileName', return_value=('saved.mp3', 'mp3'))
    @patch('model.Sound.AudioSegment.export')
    def test_save(self, mock_export, mock_get_save_file_name):
        self.sound.save()
        mock_export.assert_called_once()

    def test_volume_change(self):
        self.sound.volume_change(10)
        self.assertEqual(self.sound.history_stack[-1], 'Volume changed by 10 dB')

    def test_slice(self):
        self.sound.slice(0.2, 0.8)
        self.assertEqual(len(self.sound.track), 600)
        self.assertEqual(self.sound.history_stack[-1], 'Sliced from 0.2 to 0.8')

    def test_reverse_sound(self):
        self.sound.reverse_sound()
        self.assertEqual(self.sound.history_stack[-1], 'Reversed')

    def test_repeat_sound(self):
        self.sound.repeat_sound(3)
        self.assertEqual(len(self.sound.track), len(self.audio) * 3)
        self.assertEqual(self.sound.history_stack[-1], 'Repeat 3 times')

    @patch('model.Sound.QFileDialog.getOpenFileName', return_value=('merged.mp3', 'mp3'))
    @patch('model.Sound.AudioSegment.from_mp3', return_value=Sine(220).to_audio_segment(duration=1000))
    def test_merge(self, mock_from_mp3, mock_get_open_file_name):
        self.sound.merge()
        self.assertEqual(len(self.sound.track), len(self.audio) + 1000)
        self.assertIn('Merge with merged.mp3', self.sound.history_stack)

    def test_fade_in(self):
        self.sound.fade_in(1)
        self.assertEqual(self.sound.history_stack[-1], 'Fade in 1s')

    def test_fade_out(self):
        self.sound.fade_out(1)
        self.assertEqual(self.sound.history_stack[-1], 'Fade out 1s')

    @patch('model.Sound.QFileDialog.getOpenFileName', return_value=('overlayed.mp3', 'mp3'))
    @patch('model.Sound.AudioSegment.from_mp3', return_value=Sine(220).to_audio_segment(duration=1000))
    def test_overlay(self, mock_from_mp3, mock_get_open_file_name):
        self.sound.overlay()
        self.assertEqual(self.sound.history_stack[-1], 'Overlay by overlayed.mp3')

    def test_undo(self):
        self.sound.stack.append(self.audio)
        self.sound.history_stack.append('Dummy history')
        self.sound.undo()
        self.assertEqual(len(self.sound.track), 1000)

    def test_redo(self):
        self.sound.queue.insert(0, self.audio)
        self.sound.history_queue.insert(0, 'Dummy history')
        self.sound.redo()
        self.assertEqual(len(self.sound.track), 1000)


if __name__ == '__main__':
    unittest.main()
