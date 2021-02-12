from setuptools import find_packages, setup

setup(
    name='psrtradelib',
    packages=find_packages(include=['psrtradelib']),
    version='0.1.0',
    description='Trading and Backtesting Library',
    author='Phillip Rearick',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
