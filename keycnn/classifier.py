# encoding: utf-8

import os
import pkgutil
import sys
import tempfile

import librosa
import numpy as np
from tensorflow.python.keras.models import load_model


def std_normalizer(data):
    """
    Normalizes data to zero mean and unit variance.

    :param data: data
    :return: standardized data
    """
    # normalize as 64 bit, to avoid numpy warnings
    data = data.astype(np.float64)
    mean = np.mean(data)
    std = np.std(data)
    if std != 0.:
        data = (data-mean) / std
    return data.astype(np.float16)


class KeyClassifier:
    """
    Classifier that can estimate musical key in different formats.
    """

    def __init__(self, model_name='deepspec'):
        """
        Initializes this classifier with a Keras model.

        :param model_name: model name from sub-package models. E.g. 'deepspec', 'shallowspec', or 'deepsquare'
        """

        def to_major_minor_key(index):

            if not np.isscalar(index):
                return [to_major_minor_key(x) for x in index]

            minor = index >= 12
            midi = index + 12
            if minor:
                midi = index - 12
            tonic = librosa.midi_to_note(midi=midi, octave=False)
            mode = 'minor' if minor else 'major'
            return tonic, mode

        self.to_key = to_major_minor_key

        # match aliases for specific deep/shallow models
        if model_name == 'deepspec':
            model_name = 'deepspec_k16'
        elif model_name == 'shallowspec':
            model_name = 'shallowspec_k4'
        elif model_name == 'deepsquare':
            model_name = 'deepsquare_k8'
        self.model_name = model_name

        self.normalize = std_normalizer

        resource = _to_model_resource(model_name)
        try:
            file = _extract_from_package(resource)
        except Exception as e:
            print('Failed to find a model named \'{}\'. Please check the model name.'.format(model_name),
                  file=sys.stderr)
            raise e
        try:
            self.model = load_model(file)
        finally:
            os.remove(file)

    def estimate(self, data):
        """
        Estimate a key distribution.
        Probabilities are indexed, starting with 30 BPM and ending with 286 BPM.

        :param data: features
        :return: key probability distribution
        """
        assert len(data.shape) == 4, 'Input data must be four dimensional. Actual shape was ' + str(data.shape)
        assert data.shape[1] == 168, 'Second dim of data must be 168. Actual shape was ' + str(data.shape)
        assert data.shape[2] == 60, 'Third dim of data must be 60. Actual shape was ' + str(data.shape)
        assert data.shape[3] == 1, 'Fourth dim of data must be 1. Actual shape was ' + str(data.shape)
        norm_data = self.normalize(data)
        return self.model.predict(norm_data, norm_data.shape[0])

    def estimate_key(self, data):
        """
        Estimates the pre-dominant global key.

        :param data: features
        :return: a single key
        """
        prediction = self.estimate(data)
        averaged_prediction = np.average(prediction, axis=0)
        index = np.argmax(averaged_prediction)
        return self.to_key(index)


def _to_model_resource(model_name):
    file = model_name
    if not model_name.endswith('.h5'):
        file = file + '.h5'
    if not file.startswith('models/'):
        file = 'models/' + file
    return file


def _extract_from_package(resource):
    data = pkgutil.get_data('keycnn', resource)
    with tempfile.NamedTemporaryFile(prefix='model', suffix='.h5', delete=False) as f:
        f.write(data)
        name = f.name
    return name
