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

        # aliases for specific deep/shallow models
        aliases = {
            'deepspec': 'deepspec_k16',
            'shallowspec': 'shallowspec_k4',
            'deepsquare': 'deepsquare_k8',
            'winterreise': 'ds_winterreise_v_fold0_HU33_OL06_QU98_SC06_TR99',
            'winterreise_v': 'ds_winterreise_v_fold0_HU33_OL06_QU98_SC06_TR99',
            'winterreise_v_fold0': 'ds_winterreise_v_fold0_HU33_OL06_QU98_SC06_TR99',
            'winterreise_v_fold1': 'ds_winterreise_v_fold1_SC06_TR99_AL98_FI55_FI66',
            'winterreise_v_fold2': 'ds_winterreise_v_fold2_FI55_FI66_FI80_HU33_OL06',
            'winterreise_s': 'ds_winterreise_s_fold0_12_13_14_15_16_17_18_19_20_21_22_23_24',
            'winterreise_s_fold0': 'ds_winterreise_s_fold0_12_13_14_15_16_17_18_19_20_21_22_23_24',
            'winterreise_s_fold1': 'ds_winterreise_s_fold1_20_21_22_23_24_01_02_03_04_05_06_07_08',
            'winterreise_s_fold2': 'ds_winterreise_s_fold2_04_05_06_07_08_09_10_11_12_13_14_15_16',
            'winterreise_n': 'ds_winterreise_n_fold_NOT_AL98_FI55_FI66_01_02_03_FI80_HU33_04_05',
            'winterreise_n_fold00': 'ds_winterreise_n_fold_NOT_AL98_FI55_FI66_01_02_03_FI80_HU33_04_05',
            'winterreise_n_fold01': 'ds_winterreise_n_fold_NOT_AL98_FI55_FI66_04_05_06_FI80_HU33_07_08',
            'winterreise_n_fold02': 'ds_winterreise_n_fold_NOT_AL98_FI55_FI66_07_08_09_FI80_HU33_10_11',
            'winterreise_n_fold03': 'ds_winterreise_n_fold_NOT_AL98_FI55_FI66_10_11_12_FI80_HU33_13_14',
            'winterreise_n_fold04': 'ds_winterreise_n_fold_NOT_AL98_FI55_FI66_13_14_15_FI80_HU33_16_17',
            'winterreise_n_fold05': 'ds_winterreise_n_fold_NOT_AL98_FI55_FI66_16_17_18_FI80_HU33_19_20',
            'winterreise_n_fold06': 'ds_winterreise_n_fold_NOT_AL98_FI55_FI66_19_20_21_FI80_HU33_22_23',
            'winterreise_n_fold07': 'ds_winterreise_n_fold_NOT_AL98_FI55_FI66_22_23_24_FI80_HU33_01_02',
            'winterreise_n_fold08': 'ds_winterreise_n_fold_NOT_FI80_HU33_OL06_01_02_03_QU98_SC06_04_05',
            'winterreise_n_fold09': 'ds_winterreise_n_fold_NOT_FI80_HU33_OL06_04_05_06_QU98_SC06_07_08',
            'winterreise_n_fold10': 'ds_winterreise_n_fold_NOT_FI80_HU33_OL06_07_08_09_QU98_SC06_10_11',
            'winterreise_n_fold11': 'ds_winterreise_n_fold_NOT_FI80_HU33_OL06_10_11_12_QU98_SC06_13_14',
            'winterreise_n_fold12': 'ds_winterreise_n_fold_NOT_FI80_HU33_OL06_13_14_15_QU98_SC06_16_17',
            'winterreise_n_fold13': 'ds_winterreise_n_fold_NOT_FI80_HU33_OL06_16_17_18_QU98_SC06_19_20',
            'winterreise_n_fold14': 'ds_winterreise_n_fold_NOT_FI80_HU33_OL06_19_20_21_QU98_SC06_22_23',
            'winterreise_n_fold15': 'ds_winterreise_n_fold_NOT_FI80_HU33_OL06_22_23_24_QU98_SC06_01_02',
            'winterreise_n_fold16': 'ds_winterreise_n_fold_NOT_QU98_SC06_TR99_01_02_03_AL98_FI55_04_05',
            'winterreise_n_fold17': 'ds_winterreise_n_fold_NOT_QU98_SC06_TR99_04_05_06_AL98_FI55_07_08',
            'winterreise_n_fold18': 'ds_winterreise_n_fold_NOT_QU98_SC06_TR99_07_08_09_AL98_FI55_10_11',
            'winterreise_n_fold19': 'ds_winterreise_n_fold_NOT_QU98_SC06_TR99_10_11_12_AL98_FI55_13_14',
            'winterreise_n_fold20': 'ds_winterreise_n_fold_NOT_QU98_SC06_TR99_13_14_15_AL98_FI55_16_17',
            'winterreise_n_fold21': 'ds_winterreise_n_fold_NOT_QU98_SC06_TR99_16_17_18_AL98_FI55_19_20',
            'winterreise_n_fold22': 'ds_winterreise_n_fold_NOT_QU98_SC06_TR99_19_20_21_AL98_FI55_22_23',
            'winterreise_n_fold23': 'ds_winterreise_n_fold_NOT_QU98_SC06_TR99_22_23_24_AL98_FI55_01_02',
        }
        if model_name in aliases:
            model_name = aliases[model_name]
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
