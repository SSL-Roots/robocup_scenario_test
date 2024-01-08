from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess


class CustomInstallCommand(install):
    def run(self):
        subprocess.run('./srssl/compile_proto.sh', check=True)
        install.run(self)


setup(
    name='srssl',
    version='0.1.0',
    author='Shotak Aoki',
    author_email='macakasit@gmail.com',
    packages=find_packages(),
    license='LICENSE',
    description='Simple Python library for RoboCup SSL',
    long_description=open('README.md').read(),
    install_requires=[
        "protobuf >= 3.12",
    ],
    extras_require={
        'dev': [
            'flake8 >= 3.7.9',
            'pytest >= 5.4.1'
        ]
    },
    python_requires='>=3.6',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    cmdclass={
        'install': CustomInstallCommand,
    }
)
