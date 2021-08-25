#!/usr/bin/env python
# encoding: utf-8
"""
This file contains the setup for setuptools to distribute everything as a
(PyPI) package.

"""

from setuptools import setup, find_packages

import glob

# define version
version = '0.0.2'

# define scripts to be installed by the PyPI package
scripts = glob.glob('bin/*')

# define the models to be included in the PyPI package
# TODO: add models via wildcard
package_data = ['models/deepsquare_k1.h5',
                'models/deepsquare_k2.h5',
                'models/deepsquare_k4.h5',
                'models/deepsquare_k8.h5',
                'models/deepsquare_k16.h5',
                'models/deepsquare_k24.h5',
                'models/deepspec_k2.h5',
                'models/deepspec_k4.h5',
                'models/deepspec_k8.h5',
                'models/deepspec_k16.h5',
                'models/deepspec_k24.h5',
                'models/shallowspec_k1.h5',
                'models/shallowspec_k2.h5',
                'models/shallowspec_k4.h5',
                'models/shallowspec_k6.h5',
                'models/shallowspec_k8.h5',
                'models/shallowspec_k12.h5',
                'models/ds_winterreise_n_fold_NOT_AL98_FI55_FI66_01_02_03_FI80_HU33_04_05.h5',
                'models/ds_winterreise_n_fold_NOT_AL98_FI55_FI66_04_05_06_FI80_HU33_07_08.h5',
                'models/ds_winterreise_n_fold_NOT_AL98_FI55_FI66_07_08_09_FI80_HU33_10_11.h5',
                'models/ds_winterreise_n_fold_NOT_AL98_FI55_FI66_10_11_12_FI80_HU33_13_14.h5',
                'models/ds_winterreise_n_fold_NOT_AL98_FI55_FI66_13_14_15_FI80_HU33_16_17.h5',
                'models/ds_winterreise_n_fold_NOT_AL98_FI55_FI66_16_17_18_FI80_HU33_19_20.h5',
                'models/ds_winterreise_n_fold_NOT_AL98_FI55_FI66_19_20_21_FI80_HU33_22_23.h5',
                'models/ds_winterreise_n_fold_NOT_AL98_FI55_FI66_22_23_24_FI80_HU33_01_02.h5',
                'models/ds_winterreise_n_fold_NOT_FI80_HU33_OL06_01_02_03_QU98_SC06_04_05.h5',
                'models/ds_winterreise_n_fold_NOT_FI80_HU33_OL06_04_05_06_QU98_SC06_07_08.h5',
                'models/ds_winterreise_n_fold_NOT_FI80_HU33_OL06_07_08_09_QU98_SC06_10_11.h5',
                'models/ds_winterreise_n_fold_NOT_FI80_HU33_OL06_10_11_12_QU98_SC06_13_14.h5',
                'models/ds_winterreise_n_fold_NOT_FI80_HU33_OL06_13_14_15_QU98_SC06_16_17.h5',
                'models/ds_winterreise_n_fold_NOT_FI80_HU33_OL06_16_17_18_QU98_SC06_19_20.h5',
                'models/ds_winterreise_n_fold_NOT_FI80_HU33_OL06_19_20_21_QU98_SC06_22_23.h5',
                'models/ds_winterreise_n_fold_NOT_FI80_HU33_OL06_22_23_24_QU98_SC06_01_02.h5',
                'models/ds_winterreise_n_fold_NOT_QU98_SC06_TR99_01_02_03_AL98_FI55_04_05.h5',
                'models/ds_winterreise_n_fold_NOT_QU98_SC06_TR99_04_05_06_AL98_FI55_07_08.h5',
                'models/ds_winterreise_n_fold_NOT_QU98_SC06_TR99_07_08_09_AL98_FI55_10_11.h5',
                'models/ds_winterreise_n_fold_NOT_QU98_SC06_TR99_10_11_12_AL98_FI55_13_14.h5',
                'models/ds_winterreise_n_fold_NOT_QU98_SC06_TR99_13_14_15_AL98_FI55_16_17.h5',
                'models/ds_winterreise_n_fold_NOT_QU98_SC06_TR99_16_17_18_AL98_FI55_19_20.h5',
                'models/ds_winterreise_n_fold_NOT_QU98_SC06_TR99_19_20_21_AL98_FI55_22_23.h5',
                'models/ds_winterreise_n_fold_NOT_QU98_SC06_TR99_22_23_24_AL98_FI55_01_02.h5',
                'models/ds_winterreise_s_fold0_12_13_14_15_16_17_18_19_20_21_22_23_24.h5',
                'models/ds_winterreise_s_fold1_20_21_22_23_24_01_02_03_04_05_06_07_08.h5',
                'models/ds_winterreise_s_fold2_04_05_06_07_08_09_10_11_12_13_14_15_16.h5',
                'models/ds_winterreise_v_fold0_HU33_OL06_QU98_SC06_TR99.h5',
                'models/ds_winterreise_v_fold1_SC06_TR99_AL98_FI55_FI66.h5',
                'models/ds_winterreise_v_fold2_FI55_FI66_FI80_HU33_OL06.h5',
                ]

# some PyPI metadata
classifiers = ['Development Status :: 3 - Alpha',
               'Programming Language :: Python :: 3.6',
               'Environment :: Console',
               'License :: OSI Approved :: GNU Affero General Public License v3',
               'Topic :: Multimedia :: Sound/Audio :: Analysis',
               'Topic :: Scientific/Engineering :: Artificial Intelligence']

# requirements
requirements = ['scipy>=1.0.1',
                'numpy==1.16.0',
                'tensorflow==2.5.1',
                'librosa==0.6.2',
                'jams>=0.3.1',
                'matplotlib>=3.0.0',
                'h5py>=2.7.0',
                ]

# docs to be included
try:
    long_description = open('README.rst', encoding='utf-8').read()
    long_description += '\n' + open('CHANGES.rst', encoding='utf-8').read()
except TypeError:
    long_description = open('README.rst').read()
    long_description += '\n' + open('CHANGES.rst').read()

# the actual setup routine
setup(name='keycnn',
      version=version,
      description='Python audio signal processing library',
      long_description=long_description,
      author='Hendrik Schreiber '
             'tagtraum industries incorporated, '
             'Raleigh, NC, USA',
      author_email='hs@tagtraum.com',
      url='https://github.com/hendriks73/key-cnn',
      license='AGPL',
      packages=find_packages(exclude=['tests', 'docs']),
      package_data={'keycnn': package_data},
      exclude_package_data={'': ['tests', 'docs']},
      scripts=scripts,
      install_requires=requirements,
      test_suite='nose.collector',
      classifiers=classifiers)
