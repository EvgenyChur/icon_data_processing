# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import xarray as xr
import pandas as pd


def prep_ndep(path, year):
    
    # Local variables:
    # -- Input path:
    pin = path + f'/ndep_{year}.nc'
    
    # -- Coefficients
    kg2mg    = 1e6   # mg in 1 kg
    sec_1day = 86400 # seconds in 1 day

    # Time intervals:
    year_start = year
    year_stop  = year_start + 1

    ncfile = (
        xr.open_dataset(pin, decode_times = False)
          # Create monthly time steps:
          .assign_coords(
              {'time': pd.date_range(
                  f'{year_start}-01-01',
                  f'{year_stop}-01-01',
                  freq = '1M', 
                  )
              }
          )
    ) 

    nc_nhx = (
        ncfile['NHx_deposition'] * int(kg2mg) * int(sec_1day) * 
        ncfile['NHx_deposition'].time.dt.days_in_month
    )
    
    nc_noy = (
        ncfile['NOy_deposition'] * int(kg2mg) * int(sec_1day) * 
        ncfile['NOy_deposition'].time.dt.days_in_month
    )
    
    # Apply attribute settings:
    nc_nhx.name = 'NHx_deposition'
    nc_nhx.attrs['units'] = 'mg/m2/month'
    
    nc_noy.name = 'NOy_deposition'
    nc_noy.attrs['units'] = 'mg/m2/month'
    
    return nc_nhx, nc_noy


if __name__ == '__main__':
    
    # Input and output parameters
    pin  = 'C:/Users/evchur/Desktop/masks/N-P_deposition/NDEP'
    pout = 'C:/Users/evchur/Desktop/masks/N-P_deposition/test'
    act_year = 1850
    
    # Get data:
    nhx, noy = prep_ndep(pin, act_year)
    
    # Create output dataset:
    ds = xr.Dataset(
        data_vars = {
            'lon'  : nhx.lon, 'lat'  : nhx.lat, 'time' : nhx.time,
            'NHx_deposition' : nhx, 'NOy_deposition' : noy,
        },
    )

    # write to file
    ds.to_netcdf(pout + f'/ndep_{act_year}.nc')
    

