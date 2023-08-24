# -*- coding: utf-8 -*-
"""
Description: Create linear plots for ICON spinup output parameters (land_model: QUINCY):

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    17.04.2023 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    23.08.2023 Evgenii Churiulin, MPI-BGC
           Script was fully updated
"""

# =============================     Import modules     =================
# -- Standard:
import os
import sys
import numpy as np
import pandas as pd
import xarray as xr
import warnings
warnings.filterwarnings("ignore")
# -- Personal:
sys.path.append(os.path.join(os.getcwd(), '..'))
import lib4visualization as l4v
import lib4sys_support as l4s
import lib4processing as l4p
# =============================   Personal functions   =================

# ================   User settings (have to be adapted)  ===============
# -- Type of output figures (don't change):
umode = 'lplot'

# -- Variables for analysis:
var_set4line = [
    'pheno_lai_box', 
    'assimi_gross_assimilation_box',
    'veg_veg_pool_total_c_box',
    'sb_het_respiration_box',
    'sb_emission_n2o_box',
]

# -- Varibles which are presented as fluxes:
fluxes = (
    'assimi_gross_assimilation_box',
    'sb_het_respiration_box',
    'sb_emission_n2o_box',
)

# -- Time settings:
tstart = 1901
tstop = 1948
start_year = f'{tstart}-01-01'
end_year = f'{tstop+1}-01-01'
tstep = '1M'
an_tstep = '1Y'
# -- Time scale for linear plot with annual values:
years4plot = pd.date_range(start_year, end_year, freq = an_tstep)

# -- Input and output paths:
# Dataset paths:
lst4path = []
for var in var_set4line:
    lst4path.append(
        l4s.input_path() +
        f'/DATA_SPINUP_CORR/1901-1948/lplot/{var}_{tstart}_{tstop}_map.nc')
# Input area path:
pin_area = l4s.input_path() + '/DATA_SPINUP_CORR/1901-1948/lplot/cell_area.nc'
# Output path:
fout = f'{l4s.output_path()}/check4spinup_corr'

# -- Settings for linear plots (common):
param = 'SPINUP_CRUJRA_CO2'
labels = [param]
colors = ['red']
styles = ['-']
rotat = 0.0
# -- Settings for linear plots (uniq):
set4line_plot = {
    # Settings for LAI plot:
    'pheno_lai_box' : {
        'legends' : labels,
        'colors' : colors,
        'styles' : styles,
        'title'  : 'Annual values of LAI - global grid',
        'xlabel' : 'Years',
        'ylabel' : 'LAI, m2 / m2',
        'x_rotation' : 0,
        'ylim_num': [0.0, 3.01, 0.2],
        'llegend' : True,
        'lgrid' : True,
        'output' : f'{fout}/lai',
    },
    # Settings for GPP:
    'assimi_gross_assimilation_box'  : {
        'legends' : labels,
        'colors' : colors,
        'styles' : styles,
        'title'  : 'Annual values of GPP - global grid',
        'xlabel' : 'Years',
        'ylabel' : 'GPP, Pg C yr\u207b\u00B9',
        'x_rotation' : 0,
        'ylim_num': [0, 250.1, 25.0],
        'llegend' : True,
        'lgrid' : True,
        'output' : f'{fout}/gpp',
    },
    # Settings for cVeg:
    'veg_veg_pool_total_c_box' : {
        'legends' : labels,
        'colors' : colors,
        'styles' : styles,
        'title'  : 'Annual values of cVeg - global grid',
        'xlabel' : 'Years',
        'ylabel' : 'cVeg, Pg C',
        'x_rotation' : 0,
        'ylim_num': [0.0, 350.1, 25.0],
        'llegend' : True,
        'lgrid' : True,
        'output' : f'{fout}/cveg',
    },
    # Settings for heterotrophic respiration:
    'sb_het_respiration_box' : {
        'legends' : labels,
        'colors' : colors,
        'styles' : styles,
        'title'  : 'Annual values of het_respiration - global grid',
        'xlabel' : 'Years',
        'ylabel' : 'Het_Respiration,  PgC yr\u207b\u00B9',
        'x_rotation' : 0,
        'ylim_num': [0.0, 35.1, 5.0],
        'llegend' : True,
        'lgrid' : True,
        'output' : f'{fout}/het_respiration',
    },
    # Settings for cVeg:
    'sb_emission_n2o_box' : {
        'legends' : labels,
        'colors' : colors,
        'styles' : styles,
        'title'  : 'Annual values of N2O emission - global grid',
        'xlabel' : 'Years',
        'ylabel' : 'N2O (Tg N yr\u207b\u00B9)',
        'x_rotation' : 0,
        'ylim_num': [0.0, 2500.1, 500.0],
        'llegend' : True,
        'lgrid' : True,
        'output' : f'{fout}/n2o_emission',
    },
}

# =============================    Main program   =====================
if __name__ == '__main__':
    # -- Create output folders:
    output_folder = l4s.makefolder(fout)
    # -- Activate class for work with ICON - QUINCy data:
    gid = l4p.Get_ICON_QUINCY_data()
    # -- Get data (We can use them for linear plots):
    for i in range(len(lst4path)):
        ds = gid.get_annual_ICON_data(
            umode,                              # type plot (lplot)
            fluxes,                             # Research parameters presented as flux variable
            var_set4line[i],                    # Research variable
            dpath = lst4path[i],                # Input dataset path
            apath = pin_area,                   # Input dataset path with cell area variable
            t1 = start_year,                    # First year of the research period
            t2 = end_year,                      # Last year of the research period
            tstep = tstep,                      # Time frequency
        )
        # -- Prep data for linear plots:
        if var_set4line[i] == 'pheno_lai_box':
            amean = ds.mean(dim = {'ncells'})
        else:
            amean = ds.sum(dim = {'ncells'})
        # -- Create linear plot:
        l4v.get_line_plot(
            'DataArray',
            set4line_plot.get(var_set4line[i]),
            data_xr = [amean],
            years = years4plot,
        )
