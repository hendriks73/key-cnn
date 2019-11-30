import unittest

import librosa

from keycnn.feature import read_features


class TestTempoClassifier(unittest.TestCase):

    def test_init(self):
        file = 'data/drumtrack.mp3'
        y, sr = librosa.load(file, sr=22050)
        # possible features frames
        num_feature_frames = y.shape[0] / 4096
        # possible feature windows with half overlap
        num_feature_windows = (num_feature_frames // 30) // 2

        features = read_features(file)
        self.assertEqual(len(features.shape), 4)
        self.assertEqual(features.shape[0], num_feature_windows)
        self.assertEqual(features.shape[1], 168)
        self.assertEqual(features.shape[2], 60)
        self.assertEqual(features.shape[3], 1)

