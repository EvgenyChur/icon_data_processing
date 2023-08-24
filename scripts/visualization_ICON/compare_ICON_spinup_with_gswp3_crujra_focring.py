# -*- coding: utf-8 -*-
"""
Description:

Authors: Evgenii Churiulin, Ana Bastos

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    15.04.2023 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    24.08.2023 Evgenii Churiulin, MPI-BGC
           Script was fully updated 
"""

# =============================     Import modules     =================
# 1.1: Standard modules
import os
import sys
import numpy as np
import pandas as pd
import xarray as xr
import warnings
warnings.filterwarnings("ignore")
# 1.2 Personal module
import lib4visualization as l4v
import lib4sys_support as l4s
import lib4processing as l4p

# =============================     Personal functions     =============

# =============================     User settings     ==================
# -- Type of output figures (don't change):
umode_linear ='lplot'
umode_2dmaps = '2dmap'

# -- Type of 2D maps (moment = mean --> mean over research period
#                     moment = 5 ... -> get values for one year, where 5 is year index)
moment = 5
#moment = 'mean'

# -- Varibles which are presented as fluxes:
fluxes = (
    'assimi_gross_assimilation_box',
    'sb_het_respiration_box',
    'sb_emission_n2o_box',
)

# -- Variables for comparison (main variable + difference variable)
var_set4line = [
    ['assimi_gross_assimilation_box', 'gpp_diff'],  
    ['pheno_lai_box', 'lai_diff'],
    ['veg_veg_pool_total_c_box', 'cveg_diff'],
]

# -- Input and output paths:
pin_area = f'{l4s.input_path()}/DATA_GSWP3_CRUJRA/test.nc'
fout = f'{l4s.output_path()}/check4gswp3_crujra'

# -- Time limits:
yr1 = '1985-01-01'
yr2 = '1995-01-01'
tstep = '1M'
years = pd.date_range(yr1, yr2, freq = '1Y')

# -- Settings for linear plots (common):
ln_title  = 'Comparison of ICON results based on CRUJRA_R2B4 and GSWP3_R2B4 forcing data by'
ln_xlabel = 'Years' 
labels = ['GSWP3', 'CRUJRA','CRUJRA_CO2']
colors = ['red', 'blue', 'orange']
styles = ['-', '-', '-']
rot = 0.0

# -- Settings for linear plots (uniq):
set4line_plot = {
    'assimi_gross_assimilation_box' : {
        'legends' : labels,
        'colors' : colors,
        'styles' : styles,
        'title' : 'Annual values of GPP (assimi_gross_assimilation_box) - global grid',
        'xlabel' : ln_xlabel,
        'ylabel' : 'GPP, PgC yr-1',
        'x_rotation' : rot,
        'ylim_num': [0, 250.1, 25.0],
        'llegend' : True,
        'lgrid' : True,
        'output' : f'{fout}/gpp',
    },
    'pheno_lai_box' : {
        'legends' : labels,
        'colors' : colors,
        'styles' : styles,
        'title' : 'Annual values of LAI (box) - global grid',
        'xlabel' : ln_xlabel,
        'ylabel' : 'LAI, m2 / m2',
        'x_rotation' : rot,
        'ylim_num': [0.0, 1.2, 0.1],
        'llegend' : True,
        'lgrid' : True,
        'output' : f'{fout}/LAI',
    },
    'veg_veg_pool_total_c_box' : {
        'legends' : labels,
        'colors' : colors,
        'styles' : styles,
        'title' : 'Annual values of cVeg (veg_pool_total_c_box) - global grid',
        'xlabel' : ln_xlabel,
        'ylabel' : 'cVeg, PgC',
        'x_rotation' : rot,
        'ylim_num': [0.0, 350.1, 25.0],
        'llegend' : True,
        'lgrid' : True,
        'output' : f'{fout}/veg_pool',
    },
}

# -- Settings for 2d maps:
set4plot_2dmap = {
    # Settings for GPP:
    'assimi_gross_assimilation_box' : {
        'title' : 'Annual GPP values. Year - 1990',
        'cmap' : 'gist_earth_r',
        'varMin' :    0.0,
        'varMax' : 5000.1,
        'varInt' :  100.0,
        'units' : 'gC m-2 yr-1',
        'lcoastline':True,
        'lgrid_map': True,
        'pout_map' : f'{fout}/gpp_map',
    },
    # Settings for GPP diff (CRUJRA_R2B4 - GSWP3_R2B4):
    'gpp_diff' : {
        'title' : 'Annual DIFF GPP values (DIFF = CRUJRA - GSWP3). Year - 1990',
        'cmap' : 'RdBu', #'Greens',
        'varMin' : -1500.01,
        'varMax' :  1500.01,
        'varInt' :    50.0,
        'units' : 'gC m-2 yr-1',
        'lcoastline':True,
        'lgrid_map': True,
        'pout_map' : f'{fout}/gpp_diff_map',
    },
    # Settings for LAI:
    'pheno_lai_box' : {
        'title' : 'Annual LAI values. Year - 1990',
        'cmap' :  'Greens',
        'varMin' :  0.0,
        'varMax' :  8.0,
        'varInt' :  0.005,
        'units' : 'm2 m-2',
        'lcoastline':True,
        'lgrid_map': True,
        'pout_map' : f'{fout}/lai_map',
    },
    # Settings for LAI diff (CRUJRA_R2B4 - GSWP3_R2B4):
    'lai_diff' : {
        'title' : 'Annual DIFF LAI values (DIFF = CRUJRA_R2B4 - GSWP3_R2B4). Year - 1990',
        'cmap' : 'RdBu', #'Greens',
        'varMin' : -3.5,
        'varMax' :  3.5,
        'varInt' :  0.05,
        'units' : 'm2 / m2',
        'lcoastline':True,
        'lgrid_map': True,
        'pout_map' : f'{fout}/lai_diff_map',
    },
    # Settings for cVEG:
    'veg_veg_pool_total_c_box' : {
        'title' : 'Annual cVeg values. Year - 1990',
        'cmap' : 'gist_earth_r',
        'varMin' :  0.0,
        'varMax' :  5.01,
        'varInt' :  0.25,
        'units'  : 'kgC m-2',
        'lcoastline':True,
        'lgrid_map': True,
        'pout_map' : f'{fout}/cveg_map',
    },
    # Settings for LAI diff (CRUJRA_R2B4 - GSWP3_R2B4):
    'cveg_diff' : {
        'title' : 'Annual DIFF cVeg values (DIFF = CRUJRA_R2B4 - GSWP3_R2B4). Year - 1990',
        'cmap' : 'RdBu', #'Greens',
        'varMin' : -1.5,
        'varMax' :  1.5,
        'varInt' :  0.01,
        'units' : 'kgC m-2',
        'lcoastline':True,
        'lgrid_map': True,
        'pout_map' : f'{fout}/cveg_diff_map',
    },
}

# =============================    Main program   ========================
if __name__ == '__main__':
    # -- Create output folders:
    output_folder = l4s.makefolder(fout)
    # -- Activate class for work with ICON - QUINCy data:
    gid = l4p.Get_ICON_QUINCY_data()

    # Cycle over parameter:
    for i in range(len(var_set4line)):
        param = var_set4line[i][0]
        diff_param = var_set4line[i][1]
        print(param, diff_param)
        # Get relevant paths to the input data:
        pin1 = f'{l4s.input_path()}/DATA_GSWP3_CRUJRA/QUINCY_GSWP3/{param}_1985_1994.nc'
        pin2 = f'{l4s.input_path()}/DATA_GSWP3_CRUJRA/QUINCY_CRUJRA/{param}_1985_1994.nc'
        pin3 = f'{l4s.input_path()}/DATA_GSWP3_CRUJRA/QUINCY_CRUJRA_CO2/{param}_1985_1994.nc'
        datasets = [pin1, pin2, pin3]

        # -- 2. Get data for linear plots:
        lst4ds = []
        for j in range(len(datasets)):
            # -- Get data (We can use them for linear plots)
            ds = gid.get_annual_ICON_data(
                umode_linear,                       # type plot (lplot)
                fluxes,                             # Research parameters presented as flux variable
                param,                              # Research variable
                dpath = datasets[j],                # Input dataset path
                apath = pin_area,                   # Input dataset path with cell area variable
                t1 = yr1,                           # First year of the research period 
                t2 = yr2,                           # Last year of the research period
                tstep = tstep,                      # Time frequency
            )
            # -- Prep data for linear plots:
            if param == 'assimi_gross_assimilation_box':
                ds_corr = list(map(lambda x: x.sum(dim = {'ncells'}), ds))
            elif param == 'veg_veg_pool_total_c_box':
                ds_corr = list(map(lambda x: x.sum(dim = {'ncells'}), ds))
            else:
                ds_corr = list(map(lambda x: x.mean(dim = {'ncells'}), ds))
            # -- Add prepared dataset to list:
            lst4ds.append(ds_corr)

        # -- Create linear plot:
        l4v.get_line_plot(
            'DataArray',
            set4line_plot.get(param),
            data_xr = lst4ds,
            years = years, 
        )

        # -- 3. Get data for 2D Maps:
        lst4ds = []
        for j in range(len(datasets)):
            # -- Get data (We can use them for linear plots)
            ds = gid.get_annual_ICON_data(
                    umode_2dmaps,                       # type plot (lplot)
                    fluxes,                             # Research parameters presented as flux variable
                    param,                              # Research variable
                    dpath = datasets[j],                # Input dataset path
                    t1 = yr1,                           # First year of the research period 
                    t2 = yr2,                           # Last year of the research period
                    tstep = tstep,                      # Time frequency
                )
            # -- Get mean data over time axis (nc_crujra has annual values):
            if moment == 'mean':
                ds_corr = ds.mean(dim = {'time'})
            else:
                ds_corr = ds[moment]
            lst4ds.append(ds_corr)
            # -- Create 2D maps for parameter:
            l4v.icon_data(
                ds_corr.values,
                np.rad2deg(ds_corr.clon.values),
                np.rad2deg(ds_corr.clat.values),
                set4plot_2dmap.get(param),
                var = param,
                prefix = f'{labels[j]}_{moment}'
            )

        # -- 4. Find difference between two datasets (CRUJRA - GSWP3):
        for i in range(len(lst4ds)):
            if i == 0:
                refer = lst4ds[0]
            else:
                print(f'Find difference between: {labels[i]} - GSWP3')
                diff = lst4ds[i] - refer
                # -- Create 2D maps for difference:
                l4v.icon_data(
                    diff.values,
                    np.rad2deg(diff.clon.values),
                    np.rad2deg(diff.clat.values),
                    set4plot_2dmap.get(diff_param),
                    var = diff_param,
                    prefix = f'{labels[i]}_{moment}_{diff_param}'
                )
        print('*'*75, '\n')
# =============================    End program   ========================
