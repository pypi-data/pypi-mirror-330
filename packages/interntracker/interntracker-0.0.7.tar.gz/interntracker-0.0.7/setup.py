# -*- coding: utf-8 -*-

import os

from setuptools import find_packages, setup

pwd = os.path.dirname(__file__)


def readme():
    with open(os.path.join(pwd, "README.md"), encoding="utf-8") as f:
        content = f.read()
    return content


def version():
    with open(os.path.join(pwd, "version.txt"), encoding="utf-8") as f:
        content = f.read()
    return content


def requirements():
    with open(os.path.join(pwd, "requirements.txt"), encoding="utf-8") as f:
        content = f.read()
    return content


setup(
    name="interntracker",
    version=version(),
    description="a python library wrapping http request submission for interntrack",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements().splitlines(),
    url="https://github.com/MCplayerFromPRC/tracker-python",
    author="MCplayerFromPRC",
    author_email="1953414760@qq.com",
    keywords="interntrack request submission",
    license="Apache License 2.0",
)
