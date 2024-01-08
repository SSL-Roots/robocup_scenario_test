from setuptools.command.install import install as InstallCommand
import subprocess
from setuptools import setup, find_packages


class CustomInstallCommand(InstallCommand):
    def run(self):
        subprocess.run('./srssl/compile_proto.sh', shell=True)
        InstallCommand.run(self)


setup(
    name='srssl',
    version='0.1.0',
    packages=find_packages(),
    cmdclass={
        'install': CustomInstallCommand,
    }
)
