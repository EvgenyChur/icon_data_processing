# -*- coding: utf-8 -*-
"""
Description: Check N and P deposition values

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    19.04.2023 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    28.04.2023 Evgenii Churiulin, MPI-BGC
           Code refactoring 
"""

# =============================     Import modules     ===================
# 1.1: Standard modules
import numpy as np
import pandas as pd
import xarray as xr
import warnings
warnings.filterwarnings("ignore")
# 1.2 Personal module
import lib4sys_support as l4s
import lib4visualization as l4v

# =============================   Personal functions   ===================

# ================   User settings (have to be adapted)  =================
# Logical settings:
lplot_ndep = True
lplot_pdep = False

# -- Input and output paths:
pin  = f'{l4s.input_path()}/DATA_NDEP_PDEP/R2B4_npdep_1850_2021_1p_annual.nc'
fout = f'{l4s.output_path()}/check4ndep_pdep'

# User settings for time scale (x axis):
yr1 = 1850
yr2 = 2022
tstep = '1Y'

# Additional plot settings:
if lplot_ndep is True:
    var1 = 'NHx_deposition'
    var2 = 'NOy_deposition'
    var_set4line = 'ndep'
if lplot_pdep is True:
    var1 = 'pdep'
    var2 = 'preindpdep'
    var_set4line = 'pdep'

#-- Plot settings:
ln_title  = 'Comparison of ICON results based on CRUJRA_R2B4 and GSWP3_R2B4 forcing data by'
ln_xlabel = 'Years'
set4line_plot = {
    # Settings for NDEP plot:
    'ndep' : {
        'legends' : [var1 , var2], 
        'colors' : ['red', 'blue'],
        'styles' : ['-'  , '-'   ], 
        'title' : 'Annual values of nitrogen deposition',
        'xlabel' : ln_xlabel,
        'ylabel' : 'NDEP, kg/m2/s',
        'x_rotation' : 0,
        'ylim_num': [0, 4.1e-12, 5e-13],
        'llegend' : True,
        'lgrid' : True,
        'output' : f'{fout}/ndep',
    },
    # Settings for PDEP plot:
    'pdep' : {
        'legends' : [var1, var2, 'pdep4model'], 
        'colors' : ['black', 'black', 'red'],
        'styles' : ['-.', '--', ':'], 
        'title' : 'Annual values of phosphorus deposition',
        'xlabel' : ln_xlabel,
        'ylabel' : 'PDEP, kg/m2/s',
        'x_rotation' : 0,
        'ylim_num': [1e-13, 2.01e-13, 5e-15],
        'llegend' : True,
        'lgrid' : True,
        'output' : f'{fout}/pdep',
    },
}

# =============================    Main program   ========================
if __name__ == '__main__':
    # -- Create output folders:
    output_folder = l4s.makefolder(fout)
    # -- Get data from NetCDF
    nc = xr.open_dataset(pin)
    # --Time periods (create time range):
    years = pd.date_range(f'{yr1}-01-01', f'{yr2}-01-01', freq = tstep)

    #-- Get data list with NDEP or PDEP data (legend, should be with tha same order):
    if lplot_ndep is True:
        lst4ds = [nc[var1][:,0], nc[var2][:,0]]

    if lplot_pdep is True:
        # Create additional variable for p-dep plot (only)
        var4model = np.zeros(len(nc[var1][:,0]))
        for i in range(len(var4model)):
            var4model[i] = nc['preindpdep'][:,0][i].data if nc[var1][:,0][i].time.dt.year <= 1900 else nc['pdep'][:,0][i].data
        lst4ds = [nc[var1][:,0], nc[var2][:,0], var4model]

    # -- Create plots:
    l4v.get_line_plot(
        'DataArray',
        set4line_plot.get(var_set4line),
        data_xr = lst4ds,
        years = years,
    )
# =============================    End of program   ======================