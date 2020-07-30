.. image:: https://img.shields.io/badge/License-AGPL%20v3-blue.svg
   :target: https://www.gnu.org/licenses/agpl-3.0

=======
Key-CNN
=======

Key-CNN is a simple CNN-based framework for estimating harmonic properties
of music tracks.

First and foremost, Key-CNN is a key estimator. To determine the global key of
an audio file, simply run the script

.. code-block:: console

    key -i my_audio.wav

You may specify other models and output formats (`mirex <https://www.music-ir.org/mirex/wiki/2019:Audio_Key_Detection>`_,
`JAMS <https://github.com/marl/jams>`_) via command line parameters.

E.g. to create JAMS as output format and a deepsquare model used in the SMC
paper [1], please run

.. code-block:: console

    key -m deepsquare --jams -i my_audio.wav


To use one of the ``DeepSpec`` models from [1] (see also repo
`directional_cnns <https://github.com/hendriks73/directional_cnns>`_), run

.. code-block:: console

    key -m deepspec --jams -i my_audio.wav

or,

.. code-block:: console

    key -m deepspec_k24 --jams -i my_audio.wav

if you want to use a higher capacity model (some ``k``-values are supported).
``deepsquare`` and ``shallowspec`` models may also be used.

For estimation using models trained for [2], you may run one of the following
model specs:

.. code-block:: console

    key -m winterreise -i my_audio.wav
    key -m winterreise_v -i my_audio.wav
    key -m winterreise_s -i my_audio.wav
    key -m winterreise_v_fold0 -i my_audio.wav
    key -m winterreise_s_fold1 -i my_audio.wav

For more model names and split training split definitions, please see the `models directory
in the GitHub repo <https://github.com/hendriks73/key-cnn/tree/master/keycnn/models>`_
(just remove the ``.h5`` from the file name to use as model name).
The groundtruth annotations for Winterreise models may be found
`here <https://github.com/hendriks73/key-cnn/tree/master/annotations/winterreise>`_.

For batch processing, you may want to run ``key`` like this:

.. code-block:: console

    find /your_audio_dir/ -name '*.wav' -print0 | xargs -0 key -d /output_dir/ -i

This will recursively search for all ``.wav`` files in ``/your_audio_dir/``, analyze then
and write the results to individual files in ``/output_dir/``. Because the model is only
loaded once, this method of processing is much faster than individual program starts.

Instead of estimating a global key, Key-CNN can also estimate local keys in the
form of a keygram. This can be useful for identifying modulations.
To create such a keygram, run

.. code-block:: console

    keygram -p my_audio.wav

As output, ``keygram`` will create a ``.png`` file. Additional options to select different models
and output formats are available.

You may use the ``--csv`` option to export local key estimates in a parseable format and the
``--hop-length`` option to change temporal resolution.
The parameters ``--sharpen`` and ``--norm-frame`` let you post-process the image.


Installation
============

Clone this repo and run ``setup.py install`` using Python 3.6:

.. code-block:: console

    git clone https://github.com/hendriks73/key-cnn.git
    cd key-cnn
    python setup.py install

You may need to install TensorFlow using ``pip`` from the command line.

License
=======

Source code and models can be licensed under the GNU AFFERO GENERAL PUBLIC LICENSE v3.
For details, please see the `LICENSE <LICENSE>`_ file.


Citation
========

If you use Key-CNN in your work, please consider citing it.
ShallowSpec, DeepSpec, and DeepSquare models:

.. code-block:: latex

   @inproceedings{SchreiberM19_CNNKeyTempo_SMC,
      Title = {Musical Tempo and Key Estimation using Convolutional Neural Networks with Directional Filters},
      Author = {Hendrik Schreiber and Meinard M{\"u}ller},
      Booktitle = {Proceedings of the Sound and Music Computing Conference ({SMC})},
      Pages = {47--54},
      Year = {2019},
      Address = {M{\'a}laga, Spain}
   }


All Winterreise [2] models and annotations:

.. code-block:: latex

   @inproceedings{SchreiberWM20_HMMCNNLocalKey_ICASSP,
      Title = {Local Key Estimation in Classical Music Recordings: A Cross-Version Study on {Schubert's} {Winterreise}},
      Author = {Hendrik Schreiber, Christof Wei{\ss}, Meinard M{\"u}ller},
      Booktitle = {Proceedings of the {IEEE} International Conference on Acoustics, Speech, and Signal Processing ({ICASSP})},
      Year = {2020},
      Address = {Barcelona, Spain}
   }

References
==========

.. [1] Hendrik Schreiber, Meinard Müller, `Musical Tempo and Key Estimation using Convolutional
    Neural Networks with Directional Filters
    <http://smc2019.uma.es/articles/P1/P1_07_SMC2019_paper.pdf>`_
    Proceedings of the Sound and Music Computing Conference (SMC),
    Málaga, Spain, 2019.
.. [2] Hendrik Schreiber, Christof Weiß, Meinard Müller, `Local Key Estimation in Classical Music
    Recordings: A Cross-Version Study on Schubert's Winterreise.
    <https://ieeexplore.ieee.org/document/9054642>`_
    Proceedings of the IEEE International Conference on Acoustics, Speech, and Signal Processing (ICASSP),
    Barcelona, Spain, 2020.
