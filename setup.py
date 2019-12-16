#!/usr/bin/env python
# encoding: utf-8
"""
This file contains the setup for setuptools to distribute everything as a
(PyPI) package.

"""

from setuptools import setup, find_packages

import glob

# define version
version = '0.0.1'

# define scripts to be installed by the PyPI package
scripts = glob.glob('bin/*')

# define the models to be included in the PyPI package
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
                'numpy==1.14.5',
                'tensorflow==1.15.0',
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
