# -*- coding: utf-8 -*-
"""
Description: Create 2D maps for ICON spinup variables (land_model: QUINCY):

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

# ================   User settings (have to be adapted)  ===============
# -- Type of output figures (don't change):
umode = '2dmap'

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
tstart = 1938
tstop = 1948
start_year = f'{tstart}-01-01'
end_year = f'{tstop+1}-01-01'
tstep = '1M'

# -- Dataset input paths:
lst4path = []
for var in var_set4line:
    lst4path.append(
        l4s.input_path() +
        f'/DATA_SPINUP_CORR/1901-1948/maps/{var}_{tstart}_{tstop}_map.nc')
# Output path:
fout = f'{l4s.output_path()}/check4spinup_corr'

# -- User settings for maps:
set4plot_2dmap = {
    # Settings for GPP:
    'assimi_gross_assimilation_box' : {
        'title'  : f'Average GPP values over {tstart} - {tstop} yr.',
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
        'title'  : f'Average LAI values over {tstart} - {tstop} yr.',
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
        'title'  : f'Average cVeg values over {tstart} - {tstop} yr.',
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
        'title'  : f'Average het_respiration values over {tstart} - {tstop} yr.',
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
        'title'  : f'Average emission_n2o values over {tstart} - {tstop} yr.',
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
    # -- Activate class for work with ICON - QUINCy data:
    gid = l4p.Get_ICON_QUINCY_data()
    # -- Get data (We can use them for 2D maps):
    for i in range(len(lst4path)):
        ds = gid.get_annual_ICON_data(
            umode,                              # type plot (2D map)
            fluxes,                             # Research parameters presented as flux variable
            var_set4line[i],                    # Research variable
            dpath = lst4path[i],                # Input dataset path
            t1 = start_year,                    # First year of the research period
            t2 = end_year,                      # Last year of the research period
            tstep = tstep,                      # Time frequency
        )
        # -- Get mean data over time axis (nc_crujra has annual values):
        ave_data = ds.mean(dim = {'time'})
        # -- Create 2d plot:
        l4v.icon_data(
            ave_data.values,
            np.rad2deg(ave_data.clon.values),
            np.rad2deg(ave_data.clat.values),
            set4plot_2dmap.get(var_set4line[i]),
            var = var_set4line[i],
            prefix = f'{var_set4line[i]}_{start_year}_{end_year}',
        )
