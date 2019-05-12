# fprl [![v0.0.1](https://img.shields.io/badge/version-0.0.1-blue.svg)](https://github.com/bnbalsamo/fprl/releases) 

[![Build Status](https://travis-ci.org/bnbalsamo/fprl.svg?branch=master)](https://travis-ci.org/bnbalsamo/fprl) [![Coverage Status](https://coveralls.io/repos/github/bnbalsamo/fprl/badge.svg?branch=master)](https://coveralls.io/github/bnbalsamo/fprl?branch=master) [![Documentation Status](https://readthedocs.org/projects/fprl/badge/?version=latest)](http://fprl.readthedocs.io/en/latest/?badge=latest) [![Updates](https://pyup.io/repos/github/bnbalsamo/fprl/shield.svg)](https://pyup.io/repos/github/bnbalsamo/fprl/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

A library for implementing logs per flask request.

See the full documentation at https://fprl.readthedocs.io


# Installation
- ```$ git clone https://github.com/bnbalsamo/fprl.git```
- ```$ cd fprl```
- ```$ python setup.py install```

# Development
## Running Tests
```
$ pip install -r requirements/requirements_tests.txt
$ tox
```
Note: Tox will run tests against the version of the software installed via ```python setup.py install```.
To test against pinned dependencies add ```-r requirements.txt``` to the deps array of the tox.ini testenv
section.

## Updating Dependencies
- ```pip install -r requirements/requirements_dev.txt```
- Review ```requirements/requirements_loose.txt```
- ```tox -e pindeps```
- ```cp .tox/requirements.txt .```
- Copy minimally pinned requirements into ```setup.py```

# Author
Brian Balsamo <Brian@BrianBalsamo.com>
