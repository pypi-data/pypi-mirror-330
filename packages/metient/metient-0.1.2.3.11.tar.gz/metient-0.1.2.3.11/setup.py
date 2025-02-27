from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='metient', version='0.1.2.3.11', url="https://github.com/divyakoyy/metient.git", 
      packages=['metient', 'metient.util', 'metient.lib'], install_requires=requirements)