#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pylfmap.py

# first check if the lfmap is downloaded and then check if it is converted to healpy
# http://www.astro.umd.edu/~emilp/LFmap/LFmap_1.0.tar

import os
import sys
import numpy as np
import importlib
import healpy as hp
from healpy.rotator import Rotator
import wget
from os.path import exists
import tarfile
import subprocess
from . import LFmap_healpyFitsConvertorAndGenerator


ftar = "LFmap_1.0.tar"
hpfits_folder = "healpyFits"

# this needs absolute path to the folder
pylfmap_path = os.path.dirname(__file__)
# path to various files and folders
lfmap_abs_path = os.path.join(pylfmap_path, "LFmap/")
lfdir = lfmap_abs_path
ftar_path = os.path.join(pylfmap_path, ftar)

# later for the shell
cd_to_lfmap_folder = "cd " + lfmap_abs_path + "; "

# first check if LFmap was converted to healpy by checking if folder "healpyFits" exists
# reverse order check: converted?->compiled?->downloaded?

do_compile = False
do_convert = False

if exists(os.path.join(lfdir, hpfits_folder)):
    print("[INFO] LFmap: Import successful.")
else:
    print(
        "[INFO] Folder contaning converted fits does not exists. First run? Checking whether LFmap was compiled..."
    )
    do_convert = True
    if exists(os.path.join(lfdir, "LFmap")):
        print("[INFO] LFmap was compiled, I will just do the conversion...")
    else:
        print("Not compiled! Checking whether it at least exits...")
        do_compile = True
        if exists(os.path.join(lfdir, "LFmap.c")):
            print("[INFO] LFmap files should exists. I will compile and convert then.")
        else:
            print(
                "[INFO] LFmap folder does not exists. I will download the tar, untar it, compile and convert."
            )
            if not exists(ftar_path):
                os.mkdir(lfdir)
                URL = "http://www.astro.umd.edu/~emilp/LFmap/" + ftar
                response = wget.download(URL, ftar_path)
            t = tarfile.open(ftar_path)
            t.extractall(lfdir)
            os.remove(ftar_path)

if do_compile == True:
    # subprocess.Popen(["make"], stdout=subprocess.PIPE, cwd=lfdir)
    result = subprocess.run(
        cd_to_lfmap_folder + "make", shell=True, capture_output=True
    )
    print(result.stdout.decode())
    print(result.stderr.decode())

if do_convert == True:
    print("[INFO] Generating and converting maps from 30 to 80 MHz in 0.1 MHz steps.")
    LFmap_healpyFitsConvertorAndGenerator.main(
        path=lfmap_abs_path,
        startFrequency="30.0",
        endFrequency="80.0",
        fdelta=0.1,
    )
    print(
        "[INFO] pylfmap was initialized with frequencies 30-80 MHz with step of 0.1 MHz. You can generate later your custom ranges and values."
    )


class LFmap:
    def __init__(self):
        self._path = os.path.join(lfdir, hpfits_folder)
        print("[INFO] Available frequencies are:")
        print(self.list_available_frequencies())
        print(
            "[INFO] To generate different ones use LFmap.generate_new_frequencies(your new frequency)."
        )

    def list_available_frequencies(self):
        """Lists all already converted maps."""
        flist = [
            f.strip("LFmap_").strip("_healpy.fits")
            for f in os.listdir(lfdir + "/healpyFits/")
        ]
        flist.sort()
        print(flist)

    def generate_new_frequencies(self, new_freq):
        """Use to generate new frequencies, input variable is list or a float."""
        # if list
        if isinstance(new_freq, list) or isinstance(new_freq, np.ndarray):
            for f in new_freq:
                f = "{:.1f}".format(f)
                print("[INFO] Generating new map at {} MHz".format(f))
                LFmap_healpyFitsConvertorAndGenerator.main(
                    path=lfmap_abs_path, startFrequency=f, endFrequency=f, fdelta=0.1
                )
        else:
            new_freq = "{:.1f}".format(new_freq)
            print("[INFO] Generating new map at {} MHz".format(new_freq))
            LFmap_healpyFitsConvertorAndGenerator.main(
                path=lfmap_abs_path,
                startFrequency=new_freq,
                endFrequency=new_freq,
                fdelta=0.1,
            )
        # if single value
        print("updated...")

    def generate(self, frequency):
        """Generate map at the choosen frequency."""
        if not isinstance(frequency, str):
            frequency = "{:.1f}".format(frequency)
        print("[INFO] Outputing map at {} MHz".format(frequency))
        path_to_fit_file = self._path + "/LFmap_" + str(frequency) + "_healpy.fits"
        if exists(path_to_fit_file):
            return hp.rotator.Rotator.rotate_map_pixel(Rotator(coord=["C", "G"]), hp.read_map(path_to_fit_file, verbose=True))
        else:
            print(
                "[ERROR] Required frequency '{}' does not exists! Use function LFmap.generate_new_frequencies() to generate it!".format(
                    frequency
                )
            )
