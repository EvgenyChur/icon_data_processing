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


def get_ICON_data(
    # Input parameters:
    pin:str,                         # Input path
    param:str,                       # Research parameter
    dim:int,                         # Dinemsion of data:
                                     # dim = 1  --> parameter has only 1 dimension (in case of ICON - only cell)
                                     # dim = 2  --> parameter has 2 dimensions (in case of ICON - time, cell)
                                     # dim = 20 --> parameter has 2 dimensions (time, cell), but you want
                                     # to get data from 0 moment of time
    # Output parameters
    ) -> tuple[
        np.array,                    # Array with research parameter
        np.array,                    # Array with Longitudes (in degree)
        np.array,                    # Array with Latitudes (in degree)
    ]:
    """ Get ICON data """
    # -- Open NetCDf:
    nc  = xr.open_dataset(pin)
    # -- Get variable:
    if dim == 1:
        var = nc[param][:].values
    elif dim == 2:
        var = nc[param][:,:].values
    elif dim == 3:
        var = nc[param][:,0,0].values
    elif dim == 20:
        var = nc[param][0,:].values
    else:
        sys.exit('Dimension format for ICON data is incorrect')
    # -- Use additional data corrections:
    if param in ('tmin', 'tmax'):
        var = var - 273.15
    # -- Get coordinates and convert radians to degrees
    clon = np.rad2deg(nc.clon.values)
    clat = np.rad2deg(nc.clat.values)
    return var, clon, clat


def get_ICON_bnds(
    # Input variables:
    pin:str,                         # Input path
    # Output variables:
    ) -> tuple[
        xr.DataArray,                # Longutite boundaries.
        xr.DataArray,                # Latitude boundaries.
    ]:
    """ Get ICON bnds values for longitude and latitude """
    nc  = xr.open_dataset(pin)
    return nc.clon_bnds, nc.clat_bnds


def check_param(
    # Input variables:
    var1 : xr.DataArray,             # First dataset
    var2 : xr.DataArray,             # Second dataset
    pname : str,                     # Research parameter
    # Output variables:
    ) -> list[int]:                  # In case of different values all
                                     # problematic indexis will be presented
                                     # in this data list
    """ Quality control of the research data"""
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
