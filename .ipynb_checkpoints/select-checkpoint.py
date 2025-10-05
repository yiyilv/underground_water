import icepyx as ipx
import numpy as np
import xarray as xr
import pandas as pd
import h5py
import os,json
from pprint import pprint
import dask.dataframe as dd
# put the full filepath to a data file here. You can get this in JupyterHub by navigating to the file,
# right clicking, and selecting copy path. Then you can paste the path in the quotes below.
fname = r'./dataset/ATL08_20210601183700_10531105_004_01.h5'
def read_atl08(fname, bbox=None):
   """
   Read 1 ATL08 file and output 6 reduced files.

   Extract variables of interest and separate the ATL08 file
   into each beam (ground track) and ascending/descending orbits.
   """
   # Each beam is a group
   group = ['/gt1l', '/gt1r', '/gt2l', '/gt2r', '/gt3l', '/gt3r']
   # Loop trough beams
   for k,g in enumerate(group):
       #-----------------------------------#
       # 1) Read in data for a single beam #
       #-----------------------------------#
       # Load variables into memory (more can be added!)
       with h5py.File(fname, 'r') as fi:
           lat = fi[g+'/land_segments/latitude'][:]
           lon = fi[g+'/land_segments/longitude'][:]
           canopy_h_metrics = fi[g+'/land_segments/canopy/canopy_h_metrics'][:]
           canopy_openness = fi[g+'/land_segments/canopy/canopy_openness'][:]
           h_canopy_quad = fi[g+'/land_segments/canopy/h_canopy_quad'][:]
       #---------------------------------------------#
       # 2) Filter data according region and quality #
       #---------------------------------------------#
       # Select a region of interest
       if bbox:
           lonmin, lonmax, latmin, latmax = bbox
           bbox_mask = (lon >= lonmin) & (lon <= lonmax) & \
                       (lat >= latmin) & (lat <= latmax)
       else:
           bbox_mask = np.ones_like(lat, dtype=bool)  # get all
       # Test for no data
       if len(canopy_h_metrics) == 0: continue
       #-----------------------#
       # 4) Save selected data #
       #-----------------------#
       # Define output file name
       ofile = fname.replace('.h5', '_'+g[1:]+'.h5')
       # Save variables
       with h5py.File(ofile, 'w') as f:
           f['lon'] = lon
           f['lat'] = lat
           f['canopy_h_metrics'] = canopy_h_metrics
           f['canopy_openness'] = canopy_openness
           f['h_canopy_quad'] = h_canopy_quad
           print('out ->', ofile)
       # save as csv
       ofilecsv = fname.replace('.h5', '_'+g[1:]+'.csv')
       result = pd.DataFrame()
       result['lon'] = lon
       result['lat'] = lat
       result['canopy_h_metrics_0'] = canopy_h_metrics[:,0]
       result['canopy_h_metrics_1'] = canopy_h_metrics[:,1]
       result['canopy_h_metrics_2'] = canopy_h_metrics[:,2]
       result['canopy_h_metrics_3'] = canopy_h_metrics[:,3]
       result['canopy_h_metrics_4'] = canopy_h_metrics[:,4]
       result['canopy_h_metrics_5'] = canopy_h_metrics[:,5]
       result['canopy_h_metrics_6'] = canopy_h_metrics[:,6]
       result['canopy_h_metrics_7'] = canopy_h_metrics[:,7]
       result['canopy_h_metrics_8'] = canopy_h_metrics[:,8]
       result['canopy_openness'] = canopy_openness
       result['h_canopy_quad'] = h_canopy_quad

       print('out ->', ofilecsv)
       result.to_csv(ofilecsv,index=None)
read_atl08(fname, None) 作者：我是水怪的哥 https://www.bilibili.com/read/cv13315751/ 出处：bilibili