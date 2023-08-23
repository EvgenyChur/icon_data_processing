# -*- coding: utf-8 -*-
"""
Description: Create 2D maps forICON spinup variables:

Authors: Evgenii Churiulin
                                                   
Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----                                                   
    1.1    18.04.2023 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    23.08.2023 Evgenii Churiulin, MPI-BGC
           Script was updated 
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
def agg(ds, method):
    if method == 'sum':
        return ds.sum(dim = {'ncells'}).groupby('time.year').sum()
    else:
        return ds.sum(dim = {'ncells'}).groupby('time.year').mean()
    
    
def get_data(ds_path, yr1, yr2, tstep, var):
        
    # -- local variables
    micromol2mol = 1e-6   # micro-mol in mole
    molc2gramm = 12.0107  # mole C in gC
    moln2o_gramm = 44.0128 # mole N2O in gN2O
    moln2gramm = 14.0067   # mole N to gN
    sec_1day = 86400      # seconds in 1 day
    gc2pgc  = 1e-15       # gC in PgC 
    gc2kgc = 1000         # gC in kgC
    #-- Read data
    nc = (xr.open_dataset(ds_path, decode_times = False)
            .assign_coords({'time': pd.date_range(yr1, yr2, freq = tstep )}))
        
    # Convert units:
    if var == 'assimi_gross_assimilation_box':
        # micro-mol C m-2 s-1 --> gC m-2 yr-1 --> PgC m-2 yr-1
        nc[var] = (nc[var] * micromol2mol * molc2gramm * sec_1day *
                   nc[var].time.dt.days_in_month)
    elif var == 'veg_veg_pool_total_c_box':
        # mol C s-1 --> kgC
        nc[var] = nc[var] * molc2gramm / gc2kgc
    elif var == 'sb_emission_n2o_box':
        # μmol N2O m-2 s-1 -> mol N2O m-2 s-1 -> gN2O m-2 s-1 -> gN2O m-2 yr-1
        #nc[var] = (nc[var] * micromol2mol * moln2o_gramm * sec_1day *
        #           nc[var].time.dt.days_in_month)

        # μmol N2O m-2 s-1 -> μmol N m-2 s-1
        nc[var] = (nc[var] ) * 2
        #nc[var] = (nc[var] / moln2o_gramm) * 28
        nc[var] = (nc[var] * micromol2mol * moln2gramm * sec_1day *
                   nc[var].time.dt.days_in_month)
    elif  var == 'sb_het_respiration_box':
        # Convert micro-mol m-3 s-1 --> micro-mol m-2 s-1
        # -- Get actual layer depths:
        soil_layers = nc['soil_layer_sb'].values
        hlayers = []
        for i in range(len(soil_layers)):
            if i == 0:
                lev_diff = 0 - soil_layers[i]
            else:
                lev_diff = soil_layers[i-1] - soil_layers[i]   
            hlayers.append(abs(lev_diff))
        # Convert micro-mol m-3 s-1 --> micro-mol m-2 s-1
        for i in range(len(soil_layers)):
            nc[var][:,i,:] = nc[var][:,i,:] * hlayers[i]
        # Get total values over layers:
        nc[var] = nc[var].sum(dim = {'soil_layer_sb'})
        # Convert micro-mol m-2 s-1 --> mol C m-2 s-1 --> gC m-2 s-1 --> gC m-2 yr-1
        nc[var] = (nc[var] * micromol2mol * molc2gramm * sec_1day *
                   nc[var].time.dt.days_in_month)
    else:
        ds_new = nc[var].resample(time = 'A').mean('time')     
        
    # Get annual values:
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

# -- Select time range:
start_year = 1938
end_year = 1948
# -- User settings for time scale (x axis)  
tstep = '1M'
years = pd.date_range(f'{start_year}-01-01', f'{end_year+1}-01-01', freq = tstep)

#-- Input and output paths:
com_path = 'C:/Users/evchur'
main = f'{com_path}/Desktop/DATA/FORCING_QUINCY'

lst4path = []
for var in var_set4line:
    lst4path.append(main + f'/DATA_SPINUP_CORR/1901-1948/maps/{var}_{start_year}_{end_year}_map.nc')
fout = f'{com_path}/Python/scripts/github/icon_data_processing/RESULTS/check4spinup_corr'

# -- User settings for maps:
set4plot_2dmap = {
    # Settings for GPP:
    'assimi_gross_assimilation_box' : {
        'title'  : f'Average GPP values over {start_year} - {end_year} yr.',
        'cmap'   : 'gist_earth_r',
        'varMin' :    0.0,
        'varMax' : 4000.1,
        'varInt' :  100.0,
        'units'  : 'gC m-2 yr-1',
        'lcoastline' : True,
        'lgrid_map' : True,
        'pout_map' : f'{fout}/',
    },
    # Settings for LAI:
    'pheno_lai_box' : {
        'title'  : f'Average LAI values over {start_year} - {end_year} yr.',
        'cmap'   :  'Greens',
        'varMin' :  0.0,
        'varMax' :  9.0,
        'varInt' :  0.5,
        'units'  : 'm2 m-2',
        'lcoastline' : True,
        'lgrid_map' : True,
        'pout_map' : f'{fout}/',
    },
    # Settings for cVEG:
    'veg_veg_pool_total_c_box' : {
        'title'  : f'Average cVeg values over {start_year} - {end_year} yr.',
        'cmap'   :  'gist_earth_r',
        'varMin' :   0.0,
        'varMax' :  12.0,
        'varInt' :   0.5,
        'units'  : 'kgC m-2',
        'lcoastline' : True,
        'lgrid_map' : True,
        'pout_map' : f'{fout}/',
    },
    # Settings for heterotropics respiration:
    'sb_het_respiration_box' : {
        'title'  : f'Average het_respiration values over {start_year} - {end_year} yr.',
        'cmap'   :  'gist_earth_r',
        'varMin' :    0.0,
        'varMax' :  900.0,
        'varInt' :   25.0,
        'units'  : 'gC m-2 yr-1',
        'lcoastline' : True,
        'lgrid_map' : True,
        'pout_map' : f'{fout}/',
    },
    # Settings for sb_emission_n2o_box:
    'sb_emission_n2o_box' : {
        'title'  : f'Average emission_n2o values over {start_year} - {end_year} yr.',
        'cmap'   :  'PuBuGn',
        'varMin' :   0.0,
        'varMax' :  30.01,
        'varInt' :   1.0,
        'units'  : 'gN m-2 yr-1',
        'lcoastline' : True,
        'lgrid_map' : True,
        'pout_map' : f'{fout}/',
    },
}

# =============================    Main program   ========================   
if __name__ == '__main__':
    # -- Create output folders:
    output_folder = l4s.makefolder(fout)
    

    # Call 
    def create_2dplot(ds, plot2d_settings, var, nout):
        l4v.icon_data(
           ds.values, 
           np.rad2deg(ds.clon.values), 
           np.rad2deg(ds.clat.values), 
           plot2d_settings.get(var),
           var = var,  
           prefix = nout,
        ) 
    
    # -- Get data (We can use them for 2D maps and linear plots)
    lst4data = []
    lst4aver = []
    for i in range(len(lst4path)):
        nc_crujra = get_data(
            lst4path[i],
            f'{start_year}-01-01',
            f'{end_year+1}-01-01',
            tstep, 
            var_set4line[i],
        )
        lst4data.append(nc_crujra)
        ave_data = nc_crujra.mean(dim = {'time'})
        lst4aver.append(ave_data)
        # -- Create 2d plot:
        create_2dplot(ave_data, set4plot_2dmap, var_set4line[i], f'{var_set4line[i]}_{start_year}_{end_year}')
