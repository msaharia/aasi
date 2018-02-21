#!/usr/bin/env python

import glob, os
import subprocess
import multiprocessing as mp

# User-supplied
metdir = '/d3/hydrofcst/overtheloop/data/forcing/retro/forc_nc/PNW'
p2ptimeseries = '/d3/msaharia/ffreq/forcinggeneration/poly2poly/poly2poly.map_timeseries.py'
mappingfile = '/d3/msaharia/ffreq/forcinggeneration/mappingislandpark.nc'
outdir = '/d3/msaharia/ffreq/forcinggeneration/islandpark/'

metens = glob.glob(metdir + '/ens_forc.PNW.0625*.nc') #List of all files
metens.sort()

def convertEns(enslist):
    subprocess.call(['python2.7', p2ptimeseries, mappingfile, enslist, outdir + os.path.basename(enslist)])
    print("Finished", enslist)

#for count, value in enumerate(metens):
#    subprocess.call(['python2.7', p2ptimeseries, mappingfile, metens[count], outdir + os.path.basename(metens[count])])
#    print("Finished", count+1, " out of ", len(metens), " ensembles")

if __name__ == '__main__':
        #pool =  mp.Pool(.cpu_count()-1) # Create a multiprocessing Pool
        pool =  mp.Pool(5) # Create a multiprocessing Pool
        pool.imap_unordered(convertEns, metens)  # proces data_inputs iterable with pool
        pool.close()
        pool.join()
