# Making a Python Library

## Resources:
https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f

## make project directory can change to it

`mkdir psrtrade`

`cd psrtrade`

## make a virtual environment named venv

`python3 -m venv venv`

## Install necessary core packages

`pip install wheel`

`pip install setuptools`

`pip install twine`

## Setup directory structure

### Core Files

`touch setup.py`

`touch README.md`

`mkdir psrtradelib`

`touch psrtradelib/__init__.py`

`touch psrtradelib/main.py`

### Optional Files for Testing

`mkdir tests`

`touch tests/__init__.py`

`touch tests/test_psrtradelib.py`

## Install Testing Packages If Writing Tests

`pip install pytest`

`pip install pytest-runner`

## Optionally, Scaffold a Helpers Directory

`mkdir psrtradelib/helpers`

`touch psrtradelib/helpers/__init__.py`

`touch psrtradelib/helpers/Logger.py`

## Build the Package

`python setup.py bdist_wheel`

## Install the Package

`pip install dist/psrtradelib-0.1.0-py3-none-any.whl # or whatever the wheel file was named`


## File Contents

### /psrtradelib/main.py
```py
import helpers.Logger

def main():
    logger = helpers.Logger.Logger()
    logger.Log("python main function")


if __name__ == '__main__':
    main()
```

### /setup.py
```py
from setuptools import find_packages, setup

setup(
    name='psrtradelib',
    packages=find_packages(include=['psrtradelib']),
    version='0.1.0',
    description='Trading and Backtesting Library',
    author='Phillip Rearick',
    license='MIT',
    install_requires=[],
    setup_requires=[‘pytest-runner’],
    tests_require=[‘pytest’],
    test_suite=’tests’,
)
```

### /psrtradelib/helpers/Logger.py
```py
class Logger():
    def Log(self, text):
        print(text)
    
    def Warning(self, text):
        print(f"{bcolors.WARNING}{text}{bcolors.ENDC}")

    def Error(self, text):
        print(f"{bcolors.FAIL}{text}{bcolors.ENDC}")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\u001b[31m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
```
