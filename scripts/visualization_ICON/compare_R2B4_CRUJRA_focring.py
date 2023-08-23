# -*- coding: utf-8 -*-
"""
Description: Comparison of annual CRUJRA data presented on ICON_R2B4 land/sea
             mask with CRUJRA data presented on T63 land/sea mask

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    09.03.2023 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    23.08.2023 Evgenii Churiulin, MPI-BGC
           Updated according to the changes into lib4visualization.py
"""

# =============================     Import modules     ==================
# 1.1: Standard modules
import numpy as np
import pandas as pd
import xarray as xr
import warnings
warnings.filterwarnings("ignore")
# 1.2 Personal module
import lib4sys_support as l4s
import lib4visualization as l4v

# =============================   Personal functions   ==================


# ================   User settings (have to be adapted)  ================

# -- Input and output paths:
com_path = 'C:/Users/evchur'
main = f'{com_path}/Desktop/DATA/FORCING_QUINCY'
pin1 = main + '/climate_crujra_v2.3_R2B4_1901-2021_zone_1p_annual.nc'
pin2 = main + '/climate_crujra_v2.3_T63_1901-2021_zone_1p_annual.nc'
fout = f'{com_path}/Python/scripts/github/icon_data_processing/RESULTS/check4forcing'

# -- Parameters for comparison (forcing):
parameters = [
    'longwave', 'shortwave', 'tmin', 'tmax', 'qair', 'precip', 'wspeed']

# -- Plot settings (common for all parmaeters):
tstart = 1901
tstop = 2022
freq = 1

labels = ['T63_v2.3', 'R2B4_v2.3']                                             # legend labels (option 1)
#labels = ['T63_v2.3', 'T63_v2.3_z']                                           # legend labels (option 2) 
colors = ['red', 'blue']                                                       # line colors 
styles = ['-', '-']                                                            # line styles
rotation = 0.0                                                                 # Rotation of x axis labels 
ln_title = 'Comparison of CRUJRA_T63_v2.3 and CRUJRA_R2B4_v2.3 forcing data by'# Plot title
ln_xlabel = 'Years'                                                            # X label

# -- Plot settings (uniq for parameter):
set4line_plot = {
    'longwave' : {
        'legends' : labels,
        'colors' : colors,
        'styles' : styles,
        'title' : f'{ln_title} longwave',
        'xlabel' : ln_xlabel,
        'ylabel' : 'Longwave radiation, W/m2',
        'x_rotation': rotation,
        'ylim_num': [305.0, 340.1, 5.0],
        'llegend' : True,
        'lgrid' : True,
        'output' : f'{fout}/longwave',
    },
    'shortwave' : {
        'legends' : labels,
        'colors' : colors,
        'styles' : styles,
        'title'  : f'{ln_title} shortwave',
        'xlabel' : ln_xlabel,
        'ylabel' : 'Shortwave radiation, W/m2',
        'x_rotation': rotation,
        'ylim_num': [198.0, 212.1, 2.0],
        'llegend' : True,
        'lgrid' : True,
        'output' : f'{fout}/shortwave',
    },
    'tmin' : {
        'legends' : labels,
        'colors' : colors,
        'styles' : styles,
        'title' : f'{ln_title} tmin',
        'xlabel' : ln_xlabel,
        'ylabel' : 'Min temperature, degC',
        'x_rotation': rotation,
        'ylim_num': [6.0, 10.1, 1.0],
        'llegend' : True,
        'lgrid' : True,
        'output' : f'{fout}/tmin', 
    },
    'tmax' : {
        'legends' : labels,
        'colors' : colors,
        'styles' : styles,
        'title' : f'{ln_title} tmax',
        'xlabel' : ln_xlabel,
        'ylabel' : 'Max temperature, degC',
        'x_rotation': rotation,
        'ylim_num': [18.0, 21.1, 1.0],
        'llegend' : True,
        'lgrid' : True,
        'output' : f'{fout}/tmax',
    },
    'qair' : {
        'legends' : labels,
        'colors' : colors,
        'styles' : styles,
        'title' : f'{ln_title} qair',
        'xlabel' : ln_xlabel,
        'ylabel' : 'Air humidity, g/g',
        'x_rotation': rotation,
        'ylim_num': [0.005, 0.012, 0.001],
        'llegend' : True,
        'lgrid' : True,
        'output' : f'{fout}/qair',
    },
    'precip' : {
        'legends' : labels,
        'colors' : colors,
        'styles' : styles,
        'title' : f'{ln_title} precip',
        'xlabel' : ln_xlabel,
        'ylabel' : 'Total precipitation, mm/day',
        'x_rotation': rotation,
        'ylim_num': [2.0, 3.1, 0.25],
        'llegend': True,
        'lgrid' : True,
        'output' : f'{fout}/precip',
    },
    'wspeed'    : {
        'legends' : labels,
        'colors' : colors,
        'styles' : styles,
        'title'  : f'{ln_title} wspeed',
        'xlabel' : ln_xlabel,
        'ylabel' : 'Wind speed, m/s',
        'x_rotation': rotation,
        'ylim_num': [2.0, 4.1, 0.25],
        'llegend': True,
        'lgrid' : True,
        'output' : f'{fout}/wspeed',
        },
    'fd' : {
        'legends' : labels,
        'colors' : colors,
        'styles' : styles,
        'title'  : f'{ln_title} fd',
        'xlabel' : ln_xlabel,
        'ylabel' : 'Fraction diffuse',
        'x_rotation': rotation,
        'ylim_num': [5.0, 10.1, 1.0],
        'llegend': True,
        'lgrid' : True,
        'output' : f'{fout}/fd',
    },
}

# =============================    Main program   ============================
if __name__ == '__main__':
    # -- Create output folder:
    output_folder = l4s.makefolder(fout)
    # -- Create time range
    years = np.arange(tstart, tstop, freq)
    # -- Data processing over parameters:
    for param in parameters:
        # -- Open datasets:
        nc_t63 = xr.open_dataset(pin1)
        nc_r2b4 = xr.open_dataset(pin2)
        # -- Get data list with data (T63 --> R2B4). 
        #    Check legend, should be the same order.
        lst4ds = [nc_t63[param][:,0,0], nc_r2b4[param][:,0,0]]
        # -- Create line plots:
        l4v.get_line_plot(
            'DataArray',
            set4line_plot.get(param),
            data_xr = lst4ds,
            years = years,
        )
# =============================    End of program   ==========================
