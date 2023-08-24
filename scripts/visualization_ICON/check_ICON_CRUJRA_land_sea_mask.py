# -*- coding: utf-8 -*-
"""
Description: Comparison of land/sea masks of CRUJRA datasets with tmin and tswrf (fd).

After that program start quality control test for clat, clon and var.
If all values are the same, program create a new NetCDF file and one 
additional plot with land / sea mask.

Acknowledgements: DKRZ wiki 
(https://docs.dkrz.de/doc/visualization/sw/python/index.html)
    
Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    23.02.2023 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    22.08.2023 Evgenii Churiulin, MPI-BGC
           Script was fully updated 
"""

# =============================     Import modules     ===================
# 1.1: Standard modules
import sys
import xarray as xr
import numpy as np
import pandas as pd

import lib4processing as l4p
import lib4sys_support as l4s
import lib4visualization as l4v
# ============================  Personal functions  ======================

def get_param(
        # Intup variables:
        set4plot:dict,              # User settings for plots
        **kwargs,                   # other parameters (pin, var, dims)
        # Output variables:
        ) -> tuple[
            xr.DataArray,           # research parameter (2D field)
            np.array,               # longitudes
            np.array,               # latitudes
        ]:
    """Read data from: 
        1 - reference dataset (for example: ICON t2m) and 
        2 - Research dataset (tswrf or fd). Script get ICON data create 2 
            plots for selected parameters, after that all
            != None values set to 1, NaN values set to 0."""
    # -- Local variables:
    int_type = 'int'
    # -- Get ICON data for parameter:
    ds4param, clon, clat = l4p.get_ICON_data(
        kwargs['pin'],
        kwargs['var'],
        kwargs['dims'],
    )
    # -- Create 2D map for paramter:
    l4v.icon_data(
        ds4param,
        clon,
        clat, 
        set4plot.get(kwargs['var']),
        var = kwargs['var'],
    )
    # -- Convert non nan values to 1 and nan values to 0 (create land/sea mask)
    df = pd.DataFrame(data = ds4param, columns = [kwargs['var']])
    # -- Get general information about data:
    print('*' * 50)
    print (f'Dataset with {var1}', df.info())
    print('')
    print('NaN values in datasets : ', df.isnull().sum())
    print('')
    #-- Replace NaN and not nan values to (0 and 1) and check values:
    ds4param = (
        df.notnull()
          .astype(int_type)[kwargs['var']]
          .to_numpy()
    )
    return ds4param, clon, clat

# ================   User settings (have to be adapted)  ==============

# If you want to run script without shell running script: Use these 3 code line
#-- NetCDF attributes
var1 = 'tmin'
var2 = 'tswrf' # 'fd'
var3 = 'ls_mask'
# otherwise:
#var1 = sys.argv[1]
#var2 = sys.argv[2]
#var3 = sys.argv[3]
dims = 20

# Input paths:
pin1 = f'{l4s.input_path()}/DATA/crujra_v2.3_R2B4_{var1}_2021.nc'
pin2 = f'{l4s.input_path()}/DATA/crujra_v2.3_R2B4_{var2}_2021.nc'

# output paths
fout = f'{l4s.output_path()}/check_lsm'
nout = fout + '/ls_mask.nc'

#-- Settings for ICON sea/land or land/sea mask
set4mask_plots = {
    'title' : 'ICON sea/land mask',
    'sea_color' : 'aqua',
    'land_color': 'peru',
    'labels' : ['Water cover', 'Land cover'],
    'vmin' : 0,
    'vmax' : 1,
    'pout_map' : f'{fout}/ICON_{var3}_new',
    'lcoastline': True,
    'lgrid_map' : True,
}

#-- Settings for other parameters in NetCDF (all data has values in range 0 - 1)
set4plot = {
    # Settings for tmin:
    'tmin' : {
        'title' : 'ICON tricontourf plot',
        'cmap' : 'Spectral_r',
        'varMin' : -50.0,
        'varMax' :  30.0,
        'varInt' :   5.0,
        'units' : 'deg C',
        'lcoastline':True,
        'lgrid_map': True,
        'pout_map' : f'{fout}/plot_ICON_tmin',
    },
    # Settings for tswrf:
    'tswrf' : {
        'title' : 'ICON tricontourf plot',
        'cmap' : 'Spectral_r',
        'varMin' :    0.0,
        'varMax' : 1000.0,
        'varInt' :   50.0,
        'units' : 'W m-2',
        'lcoastline':True,
        'lgrid_map': True,
        'pout_map' : f'{fout}/plot_ICON_tswrf',
    },
    # Settings for fd:
    'fd' : {
        'title' : 'ICON tricontourf plot',
        'cmap' : 'Spectral_r',
        'varMin' :   0.0,
        'varMax' :   1.0,
        'varInt' :   0.1,
        'units' : '--',
        'lcoastline':True,
        'lgrid_map': True,
        'pout_map' : f'{fout}/plot_ICON_fd',
    },
}

# =============================    Main program   =====================
if __name__ == '__main__':
    # -- Create output folder:
    output_folder = l4s.makefolder(fout)

    # -- 1. Get ICON data and create 2d mao (tmin, tswrf or fd datasets):
    ds4param1, clon1, clat1 = get_param(
        set4plot, pin = pin1, var = var1, dims = dims)
    ds4param2, clon2, clat2 = get_param(
        set4plot, pin = pin2, var = var2, dims = dims)

    # -- 2. Run quality control test (lat, lon, param):
    check_lat = l4p.check_param(clat1, clat2, 'clat')
    check_lon = l4p.check_param(clon1, clon2, 'clon')
    check_var = l4p.check_param(ds4param1, ds4param2, 'land/water')

    # -- 3. Create land/see mask:
    clon_bnds1, clat_bnds1 = l4p.get_ICON_bnds(pin1)
    mask = xr.DataArray(ds4param1)
    # Rename attributes:
    mask.name = var3
    mask.attrs['long_name'] = 'Land - Sea mask'
    mask.attrs['units'] = ' 1 - 0 '
    mask.attrs['coordinates'] = 'clat clon'
    mask = xr.DataArray.to_dataset(mask)
    # Add coordinates:
    mask['clat_bnds'] = clat_bnds1
    mask['clon_bnds'] = clon_bnds1
    # Save new netcdf:
    mask.to_netcdf(nout)

    # -- 4. Visualization land/sea mask:
    l4v.plot_mask(
        mask[var3], 
        np.rad2deg(mask.clon.values), 
        np.rad2deg(mask.clat.values),
        set4mask_plots,
        var = var3,
    )
# =============================    End of program   ====================
