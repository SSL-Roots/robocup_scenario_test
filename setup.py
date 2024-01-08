# This file defines a custom installation procedure for the package.
from setuptools import setup
from setuptools.command.install import install
import subprocess


class CustomInstallCommand(install):
    def run(self):
        subprocess.run('./srssl/compile_proto.sh', check=True)
        install.run(self)


setup(
    cmdclass={
        'install': CustomInstallCommand,
    }
)
