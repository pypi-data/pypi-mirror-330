from setuptools import setup, find_packages
import os
import shutil
from setuptools.command.install import install
from setuptools.command.develop import develop

PACKAGE_DATA_DIR = os.path.join('metient', 'lib', 'projectppm')

def copy_projectppm():
    """Copy projectppm files to package"""
    if not os.path.exists(PACKAGE_DATA_DIR):
        os.makedirs(PACKAGE_DATA_DIR)
        # Copy the files you need
        shutil.copy('projectppm/make.sh', os.path.join(PACKAGE_DATA_DIR, 'make.sh'))
        # Copy other necessary files
        # shutil.copy('projectppm/other_file', os.path.join(PACKAGE_DATA_DIR, 'other_file'))

class CustomInstall(install):
    def run(self):
        copy_projectppm()
        install.run(self)

class CustomDevelop(develop):
    def run(self):
        copy_projectppm()
        develop.run(self)

setup(
    name='metient',
    version='0.1.2.3.12',
    url="https://github.com/divyakoyy/metient.git",
    packages=['metient', 'metient.util', 'metient.lib'],
    package_data={
        'metient.lib': ['projectppm/*'],  # Include all projectppm files
    },
    include_package_data=True,
    cmdclass={
        'install': CustomInstall,
        'develop': CustomDevelop,
    }
)