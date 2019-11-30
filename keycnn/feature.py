# encoding: utf-8

"""
Feature loading from audio files.

Specifically, key-cnn uses CQT spectra with 8 octaves starting at C1.
"""

import librosa as librosa
import numpy as np


def read_features(file, frames=60, hop_length=30, zero_pad=False):
    """
    Resample file to 22050 Hz, then transform using CQT with length 8192
    and hop size 4096, ranging from E1 + 7 octaves with two semitones
    per bin.

    Since we require at least 60 frames, shorter audio excerpts are always
    zero padded.

    Specifically for keygram, 30 frames each can be added at the front and
    at the back in order to make the calculation of key values for the first
    and the last window possible.

    :param file: file
    :param frames: 60
    :param hop_length: 30 or shorter
    :param zero_pad: adds 30 zero frames both at the front and back
    :return: feature tensor for the whole file
    """
    y, sr = librosa.load(file, sr=22050)
    octaves = 7
    bins_per_semitone = 2
    bins_per_octave = 12 * bins_per_semitone
    window_length = 8192
    data = np.abs(librosa.cqt(y, sr=sr, hop_length=window_length // 2,
                              fmin=librosa.note_to_hz('E1'),
                              n_bins=bins_per_octave * octaves,
                              bins_per_octave=bins_per_octave))

    data = np.reshape(data, (1, data.shape[0], data.shape[1], 1))

    # add frames/2 zero frames before and after the data
    if zero_pad:
        data = _add_zeros(data, frames)

    # zero-pad, if we have less than 256 frames to make sure we get some
    # result at all
    if data.shape[2] < frames:
        data = _ensure_length(data, frames)

    # convert data to overlapping windows,
    # each window is one sample (first dim)
    return _to_sliding_window(data, frames, hop_length)


def _ensure_length(data, length):
    padded_data = np.zeros((1, data.shape[1], length, 1), dtype=data.dtype)
    padded_data[0, :, 0:data.shape[2], 0] = data[0, :, :, 0]
    return padded_data


def _add_zeros(data, zeros):
    padded_data = np.zeros((1, data.shape[1], data.shape[2] + zeros, 1), dtype=data.dtype)
    padded_data[0, :, zeros // 2:data.shape[2] + (zeros // 2), 0] = data[0, :, :, 0]
    return padded_data


def _to_sliding_window(data, window_length, hop_length):
    total_frames = data.shape[2]
    windowed_data = []
    for offset in range(0, ((total_frames - window_length) // hop_length + 1) * hop_length, hop_length):
        windowed_data.append(np.copy(data[:, :, offset:window_length + offset, :]))
    return np.concatenate(windowed_data, axis=0)
