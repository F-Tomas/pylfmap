# pylfmap

This code provides a python interface for the [LFmap](https://github.com/epolisensky/LFmap) galaxy radio sky map generator. For more about LFmap read [here](https://leo.phys.unm.edu/~lwa/memos/memo/lwa0111.pdf). With the pylfmap class one can use all the features provided by the [healpy](https://github.com/healpy/healpy) (or other relevant python packages).

## Install

The most convenient install method is to use pip which retrieves the latest version of the software and also takes care of any missing dependencies:

        pip install pylfmap

or install using the git:

        pip install git+https://github.com/F-Tomas/pylfmap

Alternatively, clone the directory and run the setup.py:

        git clone https://github.com/F-Tomas/pylfmap
        python setup.py install
        
During the installation, the original C++ LFmap will be downloaded, and on the first run, sky model data in the range from 30 to 80 MHz with 0.1 MHz spacing will be generated.

## Examples

Checkout the `working_example.ipynb` jupyter notebook example.


