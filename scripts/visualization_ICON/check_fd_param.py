# -*- coding: utf-8 -*-
"""
Description: Control of fd values before and after filtering night values

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    20.03.2023 Evgenii Churiulin, MPI-BGC
           Initial release
"""
# =============================     Import modules     =================
# 1.1: Standard modules
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

import lib4sys_support as l4s
# ============================  Personal functions  ======================
def get_data(pin:str, param:str):
    """ Get data from netcdf """
    global days
    nc  = xr.open_dataset(pin)
    return pd.DataFrame(nc[param][:,0,0].values).rolling(days).mean().dropna()


# ====================   User settings (have to be adapted)   ==========
#-- FD values without night filter:
pin1 = f'{l4s.input_path()}/fd_1901-2021_daily_fld.nc'
#-- FD values with night filter:
pin2 = f'{l4s.input_path()}/crujra_dmean_fld.nc'
pout = f'{l4s.output_path()}/res4fd'

days = 150
# =============================    Main program   ======================
if __name__ == '__main__':
    #-- Create output folder:
    pout = l4s.makefolder(pout)
    # -- Get input data:
    var1 = get_data(pin1, 'fdsw')
    var2 = get_data(pin2, 'fdsw')
    # -- Create simple plot:
    fig = plt.figure(figsize = (12,7))
    ax  = fig.add_subplot(111)
    ax.plot(var1, label = 'wd_corr' , color = 'r')
    ax.plot(var2, label = 'wot_corr', color = 'b')
    ax.legend()
    plt.savefig(pout + 'fd_filter_diff.png', bbox_inches = 'tight', dpi = 150)
# =============================    End of program   =====================
