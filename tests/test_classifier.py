import unittest

import numpy as np

from keycnn.classifier import KeyClassifier
from keycnn.feature import read_features


class TestKeyClassifier(unittest.TestCase):

    def test_init(self):
        key_classifier = KeyClassifier('deepspec')
        self.assertIsNotNone(key_classifier.model)

    def test_winterreise_init(self):
        key_classifier = KeyClassifier('winterreise')
        self.assertIsNotNone(key_classifier.model)

    def test_bad_model_name(self):
        try:
            KeyClassifier('bad_model_name')
            self.fail('Expected FileNotFoundError')
        except FileNotFoundError:
            pass

    def test_predict(self):
        key_classifier = KeyClassifier('deepspec')
        predictions = key_classifier.estimate(self.get_test_data())
        self.assertEqual(predictions.shape, (2, 24))
        np.testing.assert_array_almost_equal(np.ones(2), np.sum(predictions, axis=1))
        tempi = np.argmax(predictions, axis=1)
        self.assertEqual(tempi[0], 5)
        self.assertEqual(tempi[1], 2)

    def test_predict_key(self):
        key_classifier = KeyClassifier('deepspec')
        key = key_classifier.estimate_key(self.get_test_data())
        self.assertEqual('D', key[0])
        self.assertEqual('major', key[1])

    def test_key_with_real_data(self):
        features = read_features('data/drumtrack.mp3')
        key_classifier = KeyClassifier('deepspec')
        key = key_classifier.estimate_key(features)
        self.assertEqual('C', key[0])
        self.assertEqual('major', key[1])

    def get_test_data(self):
        artificial_data = np.zeros((2, 168, 60, 1))
        for i in np.arange(0, 60, 4):
            artificial_data[0, :, i, 0] = 1
        for i in np.arange(0, 60, 30):
            artificial_data[1, :, i, 0] = 1
        return artificial_data
