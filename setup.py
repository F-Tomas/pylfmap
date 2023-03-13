#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="pylfmap",
    version="0.1",
    description="Python wrapper for LFmap software",
    long_description=readme(),
    author="T. Fodran",
    author_email="t.fodran@astro.ru.nl",
    url="https://gitlab.iap.kit.edu/auger-observatory/sandboxes/t.fodran/radiocalibrationtoolkit",
    packages=find_packages(),
    install_requires=["healpy", "numpy", "astropy", "wget"],
)
