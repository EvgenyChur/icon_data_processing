# -*- coding: utf-8 -*-
"""
Description: Initial preprocessing of phosphorus deposition fields

Authors: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    19.04.2023 Evgenii Churiulin, MPI-BGC
           Initial release
"""

#=============================     Import modules     ==========================
# 1.1: Standard modules
import pandas as pd
import xarray as xr
import sys

def check_before(ds_orig, var):
    return ds_orig[var].sum(dim = {'lat', 'lon'}).data


def check_after(ds_new):
    return ds_new.sum(dim = {'lat', 'lon','time'}).data
    


def get_var(ds_orig, var):
    
    # Create monthly time steps:
    years = pd.date_range('1850-01-01', '1851-01-01', freq = '1M')
    
    # Get actual values for parameter:
    lats    = ds_orig.lat
    lons    = ds_orig.lon
    ds_orig = ds_orig[var]    
    
    list4month = []
    for tstep in range(len(years)):
       
        # Convert data from annual to monthly timestep
        #vals = ds_orig / len(years)
        vals = ds_orig / 365 / 24 / 3600 / 1000000
        
        # Create new data 
        ds_new = xr.DataArray(vals, coords = {'lat': lats, 'lon': lons},
                                    dims   = ["lat", "lon"])  
        # Add time step
        ds_new = ds_new.assign_coords(time = years[tstep] )
        ds_new = ds_new.expand_dims(dim = "time")
        
        # Add final data to the list over timesteps
        list4month.append(ds_new)
    
    # Get new dataset with 0.5 resolution grid (Burned area)
    pdep_mon = xr.concat(list4month, dim = 'time')
    
    # Apply attribute settings: 
    pdep_mon.name = var
    pdep_mon.attrs['units'] = 'mg/m2/month'
       
    return pdep_mon

x = 1 / 365 / 24 / 3600 / 1000000 


#pin = 'C:/Users/evchur/Desktop/masks/N-P_deposition/P-DEP/nitrogenandphosphorus2x2annualdep.nc'
pin = 'C:/Users/evchur/Desktop/masks/N-P_deposition/P-DEP/nitrogenandphosphorus_annualdep_0.5x0.5.nc'
nc  = xr.open_dataset(pin)

pdep_a = nc['pdep'].sum(dim = {'lat', 'lon'}).data

pdep2_a =  pdep_a / (365 * 24 * 3600 * 1000000) 

pdep_m_a = pdep2_a / 12
pdep_m2_a =  pdep_a / (365 * 24 * 30 * 3600 * 1000000)
"""
params = ['pdep', 'preindpdep']

pin = 'C:/Users/evchur/Desktop/masks/N-P_deposition/P-DEP/nitrogenandphosphorus2x2annualdep.nc'
nc  = xr.open_dataset(pin)
lst4var = []
for param in params:
    # Get values and compare them with previous results:
    tinfo = f'{param} values (annual, monthly) are the same'
    lst4var.append(get_var(nc, param))
    # Run fast quality control
    print(check_before(nc, param))
    print(check_after(get_var(nc, param)))
    #(print(tinfo) if round(float(check_before(nc, param)), 8) == round(float(check_after(get_var(nc, param))), 8) 
    #              else sys.exit(f'Error: {param} values are different'))

# Create dataset:
ds = xr.Dataset(       
    data_vars = {
        'lon'        : lst4var[0].lon,
        'lat'        : lst4var[0].lat,
        'time'       : lst4var[0].time,
        'pdep'       : lst4var[0],
        'preindpdep' : lst4var[1], 
    },
)

# write to file
ds.to_netcdf('ECOCLIMAP_SG.nc') 
"""