#!/usr/bin/env python

import xarray as xr
import netCDF4
import numpy as np
import pandas as pd 
import pyeto as pt
import glob, os
import aasi as ai

# User-supplied
mapfile = '/glade/p/work/manab/ff/forcinggeneration/mappingislandpark.nc'
forcdir = '/glade/p/work/manab/ff/islandpark/rawinput'
concatdir = '/glade/p/work/manab/ff/islandpark/rawinputconcat/'
obsfile = '/glade/p/work/manab/ff/forcinggeneration/pilot_basin_data/isli_bor_flow_data.txt'
outdir = '/glade/p/work/manab/ff/islandpark/inputnew/'
obsvar = 'unregflow'
starttime = '1970-01-01'
endtime = '2016-12-31'

def calcWeightedAvg(ncdat, varname):
    '''
    Calculates the weighted average 
    of any <varname> in the mapping file
    '''
    wAvg = sum(ncdat[varname]*ncdat['weight'])
    return(wAvg)

def calcPET(lat, time, tmin, tmax, tmean):
    '''
    Calculates Potential Evapotranspiration using 
    Hargreaves equation (Hargreaves and Samani, 1985) 
    '''
    
    latrad = pt.deg2rad(lat)                             #Latitude to radians
    dayofyear = pd.Series(time).dt.day.values
    etrad = []
    pet = []
    
    # Calculate ET radiation
    for x in np.nditer(dayofyear):
        soldec = pt.sol_dec(x)                           #Solar declination
        sha = pt.sunset_hour_angle(latrad, soldec)       #Sunset hour aingle
        ird = pt.inv_rel_dist_earth_sun(x)               #Inverse relative distance Earth-Sun
        etrad.append(pt.et_rad(latrad, soldec, sha, ird))#Extraterrestrial radiation
    
    # Calculate PET using hargreaves
    for x in range(0, len(etrad)):
        pet.append(pt.hargreaves(tmin[x], tmax[x], tmean[x], etrad[x]))
    
    pet = np.array(pet)
    return(pet)

def ncextract(ncfile):
    '''
    Open each forcing netCDF file
    '''
    forcdat = xr.open_dataset(ncfile)
    
    # Extracts the variables values from forcing file
    prcp = forcdat['prcp'].values
    tmax = forcdat['tmax'].values
    tmin = forcdat['tmin'].values
    time = forcdat['time'].values
    tmean = (tmax+tmin)/2
    return(forcdat, prcp, time, tmin, tmax, tmean)

if __name__ == '__main__':
    
    mapdat = xr.open_dataset(mapfile)
    lat = calcWeightedAvg(mapdat, 'latitude')
    lon = calcWeightedAvg(mapdat, 'longitude')

    # Processing forcing files
    forcfiles = glob.glob(forcdir + '/*.nc') #List of all forcing files
    forcfiles.sort()

    srchlist = glob.glob(forcdir + '/*ens_forc.PNW.0625.2010*.nc')   #Search string list
    srchlist.sort()

    # Concatenates ensembles by time and exports to concatdir
    for count, value in enumerate(srchlist):
        srchstring = srchlist[count].split('.')[-2]+ '.' + srchlist[count].split('.')[-1] #Search string for each ensemble,002.nc

        enslist = []
        # Searches for a string in a list, concatenates all files corresponding to that string, and writes out netCDF file
        for count, value in enumerate(forcfiles):
            if value.endswith(srchstring):
                enslist.append(value)

        ncconcat_time = xr.open_mfdataset(enslist, concat_dim='time')
        ncconcat_time.sortby('time')
        ncconcat_time.to_netcdf(concatdir+srchstring)
        print("Creating concatenated FUSE forcing file " , count+1, " of ", len(srchlist))
 
    # Processing forcing files
    concatforcfiles = glob.glob(concatdir + '/*.nc') #List of all files
    concatforcfiles.sort()


    #Import Flow observation for the period
    obs = pd.read_table(obsfile, skiprows = 14, header = None, 
            names = ['time', 'gaugeheight', 'resinflow', 'dailydisc', 'unregflow'])
    obs['time'] = pd.to_datetime(obs['time'])
    obs = obs.set_index(['time'])   #Set time as index
    obs = obs.loc[starttime:endtime]
    #obs = pd.to_numeric(obs[obsvar].values)    # CFS
    obs = pd.to_numeric(obs['unregflow'], errors = 'coerce')
    obs[obs<0] = 0  #Convert all negative values to zero 
    obs = ((obs*0.028316847)/1279729289.0710001)*8.64e+7  #CFS -> CMS(*0.028316847) -> m/s (/1279729289.0710001) -> mm/day (*8.64e+7)
    obs2 = np.reshape(obs,(obs.shape[0],1,1))
    
    # Processes all concatenated files and puts them in the final input directory
    for count, value in enumerate(concatforcfiles):
        [forcdat, prcp, time, tmin, tmax, tmean] = ncextract(value)
        
        pet = calcPET(lat, time, tmin, tmax, tmean)
        prcp = np.reshape(prcp,(prcp.shape[0],1,1))   #mm/day
        pet = np.reshape(pet,(pet.shape[0],1,1))      #mm/day
        tmean = np.reshape(tmean,(tmean.shape[0],1,1)) # degree C

        obs2 = np.reshape(obs,(obs.shape[0],1,1))
        
        # Create new netCDF file
        f = xr.Dataset({'pr': (['time','latitude', 'longitude'],  prcp),
                        'pet': (['time','latitude', 'longitude'],  pet),
                        'temp': (['time','latitude', 'longitude'],  tmean),
                        'q_obs': (['time','latitude', 'longitude'],  obs2)
                       },
                       coords={'time': time,
                               'latitude':[lat],
                               'longitude':[lon]}
                      )

        f.to_netcdf(outdir+os.path.basename(value))  
        print("Creating final FUSE forcing file " , count+1, " of ", len(concatforcfiles))
