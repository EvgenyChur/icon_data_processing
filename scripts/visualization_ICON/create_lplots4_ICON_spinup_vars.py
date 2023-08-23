# -*- coding: utf-8 -*-
"""
Description: Create linear plots for ICON output parameters

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
def get_data(ds_path, area_path, yr1, yr2, tstep, var):
        
    # -- local variables
    micromol2mol = 1e-6    # micro-mol in mole
    molc2gramm   = 12.0107 # mole C in gC
    moln2o_gramm = 44.0128 # mole N2O in gN2O
    moln2gramm   = 14.0067 # mole N to gN
    sec_1day     = 86400   # seconds in 1 day
    gc2kgc       = 1000    # gC in kgC
    gc2pgc       = 1e-15   # gC in PgC
    g2tg = 1e-12           # g in Tg (teragram)
    kg2pg = 1e-12          # kg in PgC
        
    #-- Read data
    nc = (xr.open_dataset(ds_path, decode_times = False)
            .assign_coords({'time': pd.date_range(yr1, yr2, freq = tstep )}))
    # -- Read data with cell area:
    nc_area = xr.open_dataset(area_path)['cell_area']
    # -- fast control, if lat and lon values the same:
    if ((np.array_equal(np.rad2deg(nc.clon.values), np.rad2deg(nc_area.clon.values))) and
        (np.array_equal(np.rad2deg(nc.clat.values), np.rad2deg(nc_area.clat.values)))) is True:
        print ('Coordinates is the same')
    else:
        sys.exit('Problem with grid cell lat or lon values!')
    # -- Add cell area values to dataset:
    nc['area'] = nc_area
    # -- Convert units:
    if var == 'assimi_gross_assimilation_box':
        # μmolC m-2 s-1 -> molC m-2 s-1 -> gC m-2 s-1 --> PgC m-2 s-1 -> PgC s-1 -> PgC yr-1
        nc[var] = (
            nc[var] * micromol2mol * molc2gramm * gc2pgc * nc['area'] *
            sec_1day * nc[var].time.dt.days_in_month
        )
    elif var == 'veg_veg_pool_total_c_box':
        # molC m-2 --> gC m-2 -> PgC m-2 -> PgC
        nc[var] = nc[var] * molc2gramm * gc2pgc * nc['area']
    elif var == 'sb_emission_n2o_box':
        # μmol N2O m-2 s-1 -> μmol N m-2 s-1
        nc[var] = (nc[var] ) * 2
        # μmol N m-2 s-1 -> mol N m-2 s-1 -> gN m-2 s-1 -> Tg N m-2 s-1 -> TgN s-1 -> TgN yr-1
        nc[var] = (
            nc[var] * micromol2mol * moln2gramm * g2tg * nc['area'] *  
            sec_1day * nc[var].time.dt.days_in_month
        )
        nc[var] = (nc[var])
    elif  var == 'sb_het_respiration_box':
        # -- Get actual layer depths:
        soil_layers = nc['soil_layer_sb'].values
        hlayers = []
        for i in range(len(soil_layers)):
            if i == 0:
                lev_diff = 0 - soil_layers[i]
            else:
                lev_diff = soil_layers[i-1] - soil_layers[i]
            hlayers.append(abs(lev_diff))
        # -- Convert μmol C m-3 s-1 --> μmol C m-2 s-1
        for i in range(len(soil_layers)):
            nc[var][:,i,:] = nc[var][:,i,:] * hlayers[i]
        # Get total values over layers:
        nc[var] = nc[var].sum(dim = {'soil_layer_sb'})
        # μmol C m-2 s-1 -> mol C m-2 s-1 -> gC m-2 s-1 -> PgC m-2 s-1 -> PgC s-1 -> PgC yr-1
        nc[var] = (
            nc[var] * micromol2mol * molc2gramm * gc2pgc * nc['area'] * 
            sec_1day * nc[var].time.dt.days_in_month
        )
    else:
        ds_new = nc[var].resample(time = 'A').mean('time')
    # -- Get annual values:
    if var in ('assimi_gross_assimilation_box', 
               'sb_emission_n2o_box',
               'sb_het_respiration_box'):
        ds_new = nc[var].resample(time = 'A').sum('time')
    else:
        ds_new = nc[var].resample(time = 'A').mean('time')
    return ds_new


# ================   User settings (have to be adapted)  ===============
# -- Variables for analysis:
var_set4line = [
    'pheno_lai_box', 
    'assimi_gross_assimilation_box',
    'veg_veg_pool_total_c_box',
    'sb_het_respiration_box',
    'sb_emission_n2o_box',
]

fluxes = [
    'assimi_gross_assimilation_box',
    'sb_het_respiration_box',
]

# -- Select time range:
start_year = 1901
end_year = 1948
# -- User settings for time scale (x axis)  
tstep = '1M'
years = pd.date_range(f'{start_year}-01-01', f'{end_year+1}-01-01', freq = tstep)
years4plot = pd.date_range(f'{start_year}-01-01', f'{end_year+1}-01-01', freq = '1Y') 

#-- Input and output paths:
com_path = 'C:/Users/evchur'
main = f'{com_path}/Desktop/DATA/FORCING_QUINCY'
# Dataset paths:
lst4path = []
for var in var_set4line:
    lst4path.append(main + f'/DATA_SPINUP_CORR/1901-1948/lplot/{var}_{start_year}_{end_year}_map.nc')
# Input area path:
pin_area = main + '/DATA_SPINUP_CORR/1901-1948/lplot/cell_area.nc'
# Output:
fout = f'{com_path}/Python/scripts/github/icon_data_processing/RESULTS/check4spinup_corr'

#-- Plot settings:
#-- Settings for plot:
param = 'SPINUP_CRUJRA_CO2'
labels = [param]
colors = ['red']
styles = ['-']
rotat = 0.0

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

    # -- Get data (We can use them for 2D maps and linear plots)
    lst4data = []    
    for i in range(len(lst4path)):
        nc_crujra = get_data(
            lst4path[i],
            pin_area,
            f'{start_year}-01-01',
            f'{end_year+1}-01-01',
            tstep, 
            var_set4line[i],
        )    
        # -- Prep data for linear plots:
        if var_set4line[i] == 'pheno_lai_box':
            amean = nc_crujra.mean(dim = {'ncells'})
        else:
            amean = nc_crujra.sum(dim = {'ncells'})

        # -- Create linear plot:
        l4v.get_line_plot(
            'DataArray',
            set4line_plot.get(var_set4line[i]),
            data_xr = [amean],
            years = years4plot,
        )
