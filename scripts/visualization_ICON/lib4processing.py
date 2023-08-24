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

import lib4unit_conversion as l4cnv
# =============================   Personal functions   =================
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


class Get_ICON_QUINCY_data:
    def __init__(self):
        self.model = 'QUINCY'


    def get_annual_ICON_data(
            # Input variables:
            self,
            mode:str,                     # Mode (lplot or 2dmap)
            fluxes:tuple[str],            # Research parameters presented as flux variable
            var:str,                      # Research variable
            **kwargs,                     # Other parameters (input paths, time limits)
            # Output variables:
        ) -> xr.DataArray:                # Annual values of the research parameters
        """Get research ICON data for linear plots and 2D maps"""
        # -- Local variables:
        time_step = 'A'     # step for resample (A - annual)
        time_axis = 'time'
        area_var = 'cell_area'
        # -- Get actual dataset path:
        if 'dpath' in kwargs and len(kwargs['dpath']) > 0:
            ds_path = kwargs['dpath']
        else:
            sys.exit('Add input path to the dataset')
        # -- Get actual path to the dataset with cell area (only for lplot mode):
        if 'apath' in kwargs and len(kwargs['apath']) > 0 and mode == 'lplot':
            area_path = kwargs['apath']
        # -- Control input time range
        if 't1' not in kwargs and 't2' not in kwargs and 'tstep' not in kwargs:
            sys.exit('Add time range for datasets (e.q.: "t1 = t2 = 1990-01-01" and tstep = "1M"' )

        # -- Activate unit converter
        cnv_units = l4cnv.UnitConverter()

        # -- Step 1: Get input data for work (research data)
        nc = (
            xr.open_dataset(ds_path, decode_times = False)
              .assign_coords(
                  {time_axis: pd.date_range(
                    kwargs['t1'],
                    kwargs['t2'],
                    freq = kwargs['tstep'],
                )}
            )
        )
        # Get extra data for linear plots:
        if mode == 'lplot':
            # -- Step 1.1: Get input data for work (research data and area_cell)
            nc_area = xr.open_dataset(area_path)[area_var]
            # -- Step 1.2: Fast control, if lat and lon values in two datasets are the same
            if ((np.array_equal(np.rad2deg(nc.clon.values), np.rad2deg(nc_area.clon.values))) and
                (np.array_equal(np.rad2deg(nc.clat.values), np.rad2deg(nc_area.clat.values)))) is True:
                print ('Longutides and Latitudes are the same')
            else:
                sys.exit('Problem with grid cell lat or lon values!')
            # -- Step 1.3: Add cell area values to dataset
            nc['area'] = nc_area

        # -- Step 2: Get correct units for linear plots
        if var == 'assimi_gross_assimilation_box':
            nc = cnv_units.gpp_converter(nc, var, mode)
        elif var == 'veg_veg_pool_total_c_box':
            nc = cnv_units.cveg_converter(nc, var, mode)
        elif var == 'sb_emission_n2o_box':
            nc = cnv_units.n2o_converter(nc, var, mode)
        elif  var == 'sb_het_respiration_box':
            nc = cnv_units.het_resp_converter(nc, var, mode)

        # -- Step 3: Get annual values
        if var in fluxes:
            ds_new = nc[var].resample(time = time_step).sum(time_axis)
        else:
            ds_new = nc[var].resample(time = time_step).mean(time_axis)
        return ds_new
