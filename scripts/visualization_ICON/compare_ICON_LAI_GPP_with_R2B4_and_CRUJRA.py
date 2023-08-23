# -*- coding: utf-8 -*-
"""
Description: Compare LAI and GPP parameters calculated in ICON based on R2B4
             and CRUJRA forcing data

Authors: Evgenii Churiulin
                                                   
Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----                                                   
    1.1    12.04.2023 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    23.08.2023 Evgenii Churiulin, MPI-BGC
           Script was fully updated 
"""

# =============================     Import modules     =================
# 1.1: Standard modules
import numpy as np
import pandas as pd
import xarray as xr
import warnings
warnings.filterwarnings("ignore")
# 1.2 Personal module
import lib4sys_support as l4s
import lib4visualization as l4v
import lib4processing as l4p
# =============================   Personal functions   =================
def icon_vars(
    # Input variables:
    uset:dict,                           # User settings for plot
    **kwargs,                            # Other parameters 
    # Output variables:
    ) -> tuple[
        np.array,                        # Research parameter
        np.array,                        # longitudes
        np.array,                        # Latittudes
    ]:
    """Get ICON data for research parameter and create 2D map for it"""
    # -- Get data:
    ds, lon, lat = l4p.get_ICON_data(
        kwargs['pin'], kwargs['param'], kwargs['dims'])
    # -- Create plot:
    l4v.icon_data(ds, lon, lat, uset, var = kwargs['param'],
        prefix = f"{kwargs['param']}_{kwargs['plt_name']}" )
    return ds, lon, lat


def create_icon_map(
        # Input variables:
        path1:str,                       # Input path for the first dataset  
        path2:str,                       # Input path for the second dataset
        parameters:list[str],            # Research parameters
        set4plot:dict,                   # User settings for plots
        # Output variables: 
    ) -> list[np.array]:                 # DIFF (ds1 - ds2) for parameters
    """Create 2D maps for ICON research parameters"""
    global dims
    #-- Local parameters:
    plt_name1 = 'CRUJRA_R2B4'
    plt_name2 = 'GSWP3_R2B4'
    
    lst4data = []
    #-- Get ICON data
    for param in parameters:
        # Get parameters for datasets:
        # Dataset 1:
        ds4param1, clon1, clat1 = icon_vars(
            set4plot.get(param),
            pin = path1,
            param = param,
            dims = dims,
            plt_name = plt_name1)
        # Dataset 2:
        ds4param2, clon2, clat2 = icon_vars(
            set4plot.get(param),
            pin = path2,
            param = param,
            dims = dims,
            plt_name = plt_name2)        
        # Find difference between das1 and ds2
        ds4param3 = ds4param1 - ds4param2
        lst4data.append(ds4param3)

        # -- Create 2D map with difference:
        if param == 'assimi_gross_assimilation_box':
            l4v.icon_data(
                ds4param3, clon2, clat2,
                set4plot.get('gpp_diff'),
                var = 'gpp_diff',
                prefix = 'gpp_diff_DIFF_CRUJRA-GSWP3',
            )
        else:
            l4v.icon_data(
                ds4param3, clon2, clat2, 
                set4plot.get('lai_diff'),
                var = 'lai_diff',
                prefix = 'pheno_lai_diff_DIFF_CRUJRA-GSWP3',
            )
            
    return(lst4data)

#================   User settings (have to be adapted)  =======================

#-- Input paths:
com_path = 'C:/Users/evchur' 
main = f'{com_path}/Desktop/DATA/FORCING_QUINCY'

# ICON monmean values:
pin1      = main + '/DATA/jsbalone_R2B4_lnd_basic_ml_1979_1986_1p_mon_crujra.nc'
pin2      = main + '/DATA/jsbalone_R2B4_lnd_basic_ml_1979_1986_1p_mon_GSWP3.nc'
# ICON YEARMEAN values
pin_mean1 = main + '/DATA/jsbalone_R2B4_lnd_basic_ml_1985_annual_mean_crujra.nc'
pin_mean2 = main + '/DATA/jsbalone_R2B4_lnd_basic_ml_1985_annual_mean_gswp3.nc'
# ICON YEARMAX values
pin_max1  = main + '/DATA/jsbalone_R2B4_lnd_basic_ml_1985_annual_max_crujra.nc'
pin_max2  = main + '/DATA/jsbalone_R2B4_lnd_basic_ml_1985_annual_max_gswp3.nc'

#-- Output paths:
main_out = f'{com_path}/Python/scripts/github/icon_data_processing/RESULTS'
fout = f'{main_out}/check4lai_gpp'
fout_max = f'{main_out}/check4lai_gpp/MAX'
fout_mean = f'{main_out}/check4lai_gpp/MEAN'

#-- Parameters for comparison:
parameters = ['assimi_gross_assimilation_box', 'pheno_lai_box']
dims = 20

# -- Time limits:
tstart = '1979-01-01'
tstop  = '1986-02-01'
tstep  = '1M'

# -- Settings for linear plots (common):
ln_title  = 'Comparison of ICON results based on CRUJRA_R2B4 and GSWP3_R2B4 forcing data by'
ln_xlabel = 'Years' 
labels = ['CRUJRA_R2B4', 'GSWP3_R2B4']
colors = ['red', 'blue']
styles = ['-','-']
rotation = 0.0

# -- Settings for linear plots (uniq):
set4line_plot = {
    'assimi_gross_assimilation_box'  : {
        'legends' : labels,
        'colors' : colors,
        'styles' : styles,        
        'title'  : f'{ln_title} GPP',
        'xlabel' : ln_xlabel,
        'ylabel' : 'Gross photosynthesis on tile area, mol(CO2)/m^2 (tile area) / s',
        'x_rotation': rotation,
        'ylim_num': [4e-07, 1.61e-06, 2e-07],
        'llegend' : True,
        'lgrid' : True,
        'output' : f'{fout}/GPP',
    },
    'pheno_lai_box' : {
        'legends' : labels,
        'colors' : colors,
        'styles' : styles,  
        'title' : f'{ln_title} LAI',
        'xlabel' : ln_xlabel,
        'ylabel' : 'leaf area index, m2 / m2',
        'x_rotation': rotation,        
        'ylim_num': [0.0, 1.0, 0.1],
        'llegend' : True,
        'lgrid' : True,
        'output' : f'{fout}/LAI',
    },
}      
 
# -- Settings for 2D map with YEARMEAN values:
set4plot_mean = {
    # Settings for GPP:
    'assimi_gross_assimilation_box' : {
        'title'  : 'ICON plot for yearmean GPP values. Year - 1985',
        'cmap'   : 'gist_earth_r',
        'varMin' : 0,
        'varMax' : 0.000015,
        'varInt' : 0.0000005,
        'units'  : 'mol(CO2)/m^2 (tile area) / s',
        'lcoastline' : True,
        'lgrid_map' : True,
        'pout_map' : f'{fout_mean}/ICON_mean',
    },
    # Settings for GPP diff (CRUJRA_R2B4 - GSWP3_R2B4):
    'gpp_diff' : {
        'title'  : 'ICON plot for DIFF (CRUJRA_R2B4 - GSWP3_R2B4) yearmean GPP values. Year - 1985',
        'cmap'   : 'RdBu', #'Greens',
        'varMin' : -0.00001,
        'varMax' :  0.00001,
        'varInt' :  0.0000005,
        'units'  : 'mol(CO2)/m^2 (tile area) / s',
        'lcoastline' : True,
        'lgrid_map' : True,
        'pout_map' : f'{fout_mean}/ICON_mean',
    },
    # Settings for LAI:
    'pheno_lai_box' : {
        'title'  : 'ICON plot for yearmean LAI values. Year - 1985',
        'cmap'   :  'Greens',
        'varMin' :  0.0,
        'varMax' :  7.0,
        'varInt' :  0.25,
        'units'  : 'm2 m-2',
        'lcoastline' : True,
        'lgrid_map' : True,
        'pout_map' : f'{fout_mean}/ICON_mean',
    },
    # Settings for LAI diff (CRUJRA_R2B4 - GSWP3_R2B4):
    'lai_diff' : {
        'title'  : 'ICON plot for DIFF (CRUJRA_R2B4 - GSWP3_R2B4) yearmean LAI values. Year - 1985',
        'cmap'   : 'RdGy', #'Greens',
        'varMin' : -4.0,
        'varMax' :  4.0,
        'varInt' :  0.25,
        'units'  : 'm2 / m2',
        'lcoastline' : True,
        'lgrid_map' : True,
        'pout_map' : f'{fout_mean}/ICON_mean',
    },
}    

#-- Settings for 2D map with YEARMAX values: 
set4plot_max = {
    # Settings for GPP:
    'assimi_gross_assimilation_box' : {
        'title' : 'ICON plot for yearmax GPP values. Year - 1985',
        'cmap' : 'gist_earth_r',
        'varMin' : 0,
        'varMax' : 0.00002,
        'varInt' : 0.0000005,
        'units' : 'mol(CO2)/m^2 (tile area) / s',
        'lcoastline' : True,
        'lgrid_map' : True,
        'pout_map' : f'{fout_max}/ICON_max',
    },
    # Settings for GPP diff (CRUJRA_R2B4 - GSWP3_R2B4):
    'gpp_diff' : {
        'title'  : 'ICON plot for DIFF (CRUJRA_R2B4 - GSWP3_R2B4) yearmax GPP values. Year - 1985',
        'cmap'   : 'RdBu', #'Greens',
        'varMin' : -0.00002,
        'varMax' :  0.00002,
        'varInt' :  0.0000005,
        'units'  : 'mol(CO2)/m^2 (tile area) / s',
        'lcoastline' : True,
        'lgrid_map' : True,
        'pout_map' : f'{fout_max}/ICON_max',
    },
    # Settings for LAI:
    'pheno_lai_box' : {
        'title'  : 'ICON plot for yearmax LAI values. Year - 1985',
        'cmap'   :  'Greens',
        'varMin' :  0.0,
        'varMax' :  7.0,
        'varInt' :  0.5,
        'units'  : 'm2 m-2',
        'lcoastline' : True,
        'lgrid_map' : True,
        'pout_map' : f'{fout_max}/ICON_max',
    },
    # Settings for LAI diff (CRUJRA_R2B4 - GSWP3_R2B4):
    'lai_diff' : {
        'title'  : 'ICON plot for DIFF (CRUJRA_R2B4 - GSWP3_R2B4) yearmax LAI values. Year - 1985',
        'cmap'   : 'RdGy', #'Greens',
        'varMin' : -4.5,
        'varMax' :  4.5,
        'varInt' :  0.25,
        'units'  : 'm2 / m2',
        'lcoastline' : True,
        'lgrid_map' : True,
        'pout_map' : f'{fout_max}/ICON_max',
    },
}
   
# =============================    Main program   ======================
if __name__ == '__main__':
    #-- Create output folders:
    output_folder = l4s.makefolder(fout)
    max_out  = l4s.makefolder(fout_max)
    mean_out = l4s.makefolder(fout_mean)
    
    # -- 1. Get data and create linear plots:
    years = pd.date_range(tstart, tstop, freq = tstep)
    #-- Create line plots
    for param in parameters:
        #-- Read data
        nc_crujra = xr.open_dataset(pin1)
        nc_gswp3  = xr.open_dataset(pin2)
        tr = nc_crujra[param][:,0,0]   
        #-- Get data list with data (T63 --> R2B4). 
        # Check legend, should be the same order.
        lst4ds = [nc_crujra[param][:,0,0], nc_gswp3[param][:,0,0]]
        #-- Create line plots:
        l4v.get_line_plot(
            'DataArray', 
            set4line_plot.get(param), 
            data_xr = lst4ds, 
            years = years,
        )
    
    # -- 2. Create 2D maps:
    data_max  = create_icon_map(pin_max1 , pin_max2 , parameters, set4plot_max )
    data_mean = create_icon_map(pin_mean1, pin_mean2, parameters, set4plot_mean)

# =============================    End of program   ====================
