# -*- coding: utf-8 -*-
"""
Description: Module with processing functions for working with ICON data

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    07.03.2022 Evgenii Churiulin, MPI-BGC
           Initial release
"""
# =============================     Import modules     ======================
import sys
import numpy as np
import pandas as pd
import xarray as xr
import warnings
warnings.filterwarnings("ignore")

# 1. Function --> get_ICON_data
def get_ICON_data(pin, param, dim):
    '''
    Task: Get ICON data

    Parameters
    ----------
    pin : str
        Input path
    param : str
        Research parameter
    dim : int
        Dinemsion of data:
            dim = 1  --> parameter has only 1 dimension (in case of ICON - only cell)
            dim = 2  --> parameter has 2 dimensions (in case of ICON - time, cell)
            dim = 20 --> parameter has 2 dimensions (time, cell), but you want
                         to get data from 0 moment of time

    Returns
    -------
    var : Array
        Array with research parameter
    clon : Array
        Longitudes (in degree)
    clat : Array
        Latitudes (in degree)
    '''
    # -- Open NetCDf
    #nc  = xr.open_dataset(pin, )
    nc  = xr.open_dataset(pin)
    #-- get variable
    if dim == 1:
        var = nc[param][:].values
    elif dim == 2:
        var = nc[param][:,:].values
    elif dim == 20:
        var = nc[param][0,:].values
    elif dim == 3:
        var = nc[param][:,0,0].values
        
    else:
        sys.exit('Dimension format for ICON data is incorrect')

    #-- Use additional data corrections:
    if param in ('tmin', 'tmax'):
        var = var - 273.15

    #-- get coordinates and convert radians to degrees
    clon = np.rad2deg(nc.clon.values)
    clat = np.rad2deg(nc.clat.values)
    
    return var, clon, clat

# 2. Function --> get_ICON_bnds
def get_ICON_bnds(pin):
    '''
    Task: Get ICON bnds values for longitude and latitude

    Parameters
    ----------
    pin : str
        Input path

    Returns
    -------
    clon: xarray
        Longutite boundaries.
    clat: xarray
        Latitude boundaries.
    '''
    nc  = xr.open_dataset(pin)
    return nc.clon_bnds, nc.clat_bnds

# 3. Function --> check_param
def check_param(var1, var2, pname):
    '''
    Task: Quality control of the research data

    Parameters
    ----------
    var1 : DataArray or Dataframe
        First dataset
    var2 : DataArray or Dataframe
        Second dataset
    pname : str
        Research parameter

    Returns
    -------
    prb_list : list
        In case of different values all problematic indexis will be presented
        in this data list
    '''
    prb_list = []
    if len(var1) == len(var2):
        for i in range(len(var1)):
            if pname not in ('clat', 'clon'):
                if var1[i] != var2[i]:
                    prb_list.append(i)
            else:
                if var1[i] != var2[i]:
                    prb_list.append(i)

    if len(prb_list) == 0:
        print(f'{pname} values in datasets are the same! \n')
    else:
        return prb_list
        sys.exit(f'{pname} data in files are different')
