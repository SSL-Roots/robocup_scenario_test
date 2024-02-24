from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import subprocess


class CustomBuildPy(build_py):
    def run(self):
        subprocess.run('./rcst/compile_proto.sh', check=True)
        build_py.run(self)


setup(
    name='rcst',
    version='0.1.0',
    author='Shotak Aoki',
    author_email='macakasit@gmail.com',
    packages=find_packages(),
    license='LICENSE',
    description='Simple Python library for RoboCup SSL',
    long_description=open('README.md').read(),
    install_requires=[
        "protobuf <= 3.20",
        "typing_extensions= >= 4.9.0",
    ],
    extras_require={
        'dev': [
            'flake8 >= 3.7.9',
            'pytest >= 5.4.1',
            'pytest-cov >= 3.0.0',
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
        'build_py': CustomBuildPy
    },
    entry_points={
        'pytest11': [
            'rcst = rcst.rcst_plugin',
        ],
    },
)
