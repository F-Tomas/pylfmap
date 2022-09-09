import subprocess
import healpy as hp
import numpy as np
from astropy.wcs import WCS
from astropy.io import fits

LFmapPath='/home/tomas/Documents/jupyterFiles/RDPerformanceOverviewDebugTool/sidereal-modulation-simulator/LFmap/pylfmap/'

def fits2healpyFits(fitFile):
    nside=64
    hdulist = fits.open(fitFile)
    hdu = hdulist[0]
    x = np.arange(hdu.header['CRVAL1'],hdu.header['NAXIS1'])
    y = np.arange(hdu.header['CRVAL2'],hdu.header['NAXIS2'])
    X, Y = np.meshgrid(x, y)
    w = WCS(hdu.header)
    ra, dec = w.wcs_pix2world(X, Y, 0)
    ra = ra*hdu.header['CDELT1']
    dec = dec*hdu.header['CDELT2']
    pixel_indices = hp.ang2pix(nside, np.deg2rad(dec+90)[::-1],np.deg2rad(ra))
    m = np.zeros(hp.nside2npix(nside))
    m[pixel_indices] = hdu.data
    healpyFile = (fitFile).split('.fits')[0]+"_healpy.fits"
    hp.write_map(healpyFile,m, coord='Celestial',overwrite=True)
    print('File converted to '+healpyFile)
    return None


def setStartFrequency(startFrequency):
    print(startFrequency)
    fullCommand="\
    delta=1;\
    frequency=`grep FINALFREQ "+LFmapPath+"LFmap.config | awk '{print $2}'`;\
    echo $frequency;\
    new_frequency="+startFrequency+";\
    echo $new_frequency;\
    sed -i \"s|$frequency|$new_frequency|\" "+LFmapPath+"/LFmap.config;\
    "
    result = subprocess.run(fullCommand, shell=True,capture_output=True)
    finfo = result.stdout.decode().splitlines()
    print("LFmap.config frequency changed from "+finfo[0]+" to "+finfo[1])
    return None

def increaseLFmapConfigOutFrequency(fdelta):
    fullCommand="\
    delta=1;\
    frequency=`grep FINALFREQ "+LFmapPath+"/LFmap.config | awk '{print $2}'`;\
    echo $frequency;\
    new_frequency=`echo \"$frequency + "+str(fdelta)+"\" |bc`;\
    echo $new_frequency;\
    sed -i \"s|$frequency|$new_frequency|\" "+LFmapPath+"/LFmap.config;\
    "
    result = subprocess.run(fullCommand, shell=True,capture_output=True)
    finfo = result.stdout.decode().splitlines()
    print("LFmap.config frequency changed from "+finfo[0]+" to "+finfo[1])
    return None

def setOUTFORM():
    fullCommand="\
    outformVar=`grep \"OUTFORM\" "+LFmapPath+"/LFmap.config |awk '{print$2}'`;\
    echo Chaning OUTFORM from $outformVar to 4;\
    sed -i \"s|OUTFORM $outformVar|OUTFORM 4|\" "+LFmapPath+"/LFmap.config;\
    "
    result = subprocess.run(fullCommand, shell=True,capture_output=True)
    print(result.stdout.decode())
    print(result.stderr.decode())
    return None

def main(startFrequency = '30.0', endFrequency = '80.0', fdelta = 0.1, path="pylfmap/LFmap/"):
    
    global LFmapPath
    LFmapPath = path
    #LFmapPath='/home/tomas/Documents/jupyterFiles/RDPerformanceOverviewDebugTool/sidereal-modulation-simulator/pylfmap/LFmap/'
    cd_to_lfmap_folder='cd '+LFmapPath+'; '
    
    # set starting frequency
    setStartFrequency(startFrequency)
    # set OUTFORM to 4
    setOUTFORM()
    # run the LFmap executable in loop
    currentFrequency = float(startFrequency)
    print(currentFrequency)
    while currentFrequency <= float(endFrequency):
        p=subprocess.run(cd_to_lfmap_folder+' ./LFmap', shell=True, capture_output=True)
        print(p.stdout.decode())
        print(p.stderr.decode())
        currentFrequency = float(p.stdout.decode().splitlines()[1].split(" ")[-1])+fdelta
        fitsFileName=p.stdout.decode().splitlines()[10]
        # convert created fits to healpy fits
        fits2healpyFits(LFmapPath+fitsFileName)
        increaseLFmapConfigOutFrequency(fdelta)

    res = subprocess.run("mkdir "+LFmapPath+"/healpyFits", shell=True,capture_output=True)
    print(res.stdout.decode())
    print(res.stderr.decode())
    res = subprocess.run("mkdir "+LFmapPath+"/fits", shell=True,capture_output=True)
    print(res.stdout.decode())
    print(res.stderr.decode())
    print("Moving generated *_healpy.fits files to "+LFmapPath+"/healpyFits")
    res = subprocess.run("mv "+LFmapPath+"*healpy.fits "+LFmapPath+"/healpyFits", shell=True,capture_output=True)
    print(res.stdout.decode())
    print(res.stderr.decode())
    print("Moving generated *.fits files to "+LFmapPath+"/fits")
    res = subprocess.run("mv "+LFmapPath+"LFmap*.fits "+LFmapPath+"/fits", shell=True,capture_output=True)

    return 0

if __name__ == '__main__':
    import sys    
    import os
    import argparse

    ap = argparse.ArgumentParser()
    ap._action_groups.pop()
    required = ap.add_argument_group('required arguments')
    optional = ap.add_argument_group('optional arguments')

    # Construct the argument parser
    # Add the arguments to the parser
    optional.add_argument("-p", "--path", nargs='?', default='./',
       help="Path to LFmap.")
    optional.add_argument("-sf", "--startfreq", nargs='?', default='30.0',
       help="Start frequency.")
    optional.add_argument("-ef", "--endfreq", nargs='?', default='80.0',
       help="End frequency.")
    optional.add_argument("-d", "--deltafreq", nargs='?', default=0.1, 
       help="Frequency step")
    args = vars(ap.parse_args())
        
    # what is required: file, fixed variable (def:frequency), range of the fixed variable (def:45), power(def:1)
    # only required arg by user is "files"

    lfmap_path = str(args['path'])
    startFrequency = args['startfreq']
    endFrequency = args['endfreq']
    fdelta = args['deltafreq']
    
    main(startFrequency=startFrequency, endFrequency=endFrequency, fdelta=fdelta, path=lfmap_path)

    sys.exit(main())



