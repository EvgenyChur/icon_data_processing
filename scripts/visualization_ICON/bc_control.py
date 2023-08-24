# -*- coding: utf-8 -*-
"""
Description: Control of boundary conditions

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    07.03.2023 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    23.08.2023 Evgenii Churiulin, MPI-BGC
           Updated script according to the lib4visualization.py changes 
"""
# =============================     Import modules     =======================
import lib4visualization as vis
import lib4processing as l4p
import lib4sys_support as l4s
# =============================   Personal functions   =======================

def get_param(
    # Intup variables:
    set4plot:dict,              # User settings for plots
    **kwargs,                   # other parameters (pin, var, dims)
    # Output variables:
    ):
    """Get data"""
    ds, clon, clat = l4p.get_ICON_data(
        kwargs['pin'], kwargs['var'], kwargs['dims'])
    vis.plot_mask(
        ds, clon, clat, set4plot, prefix = kwargs['prefix'])

# ================   User settings (have to be adapted)  ===============
# -- Parameters in NetCDF file:
lst4param = [
    'fract_glac' , 'fract_lake' , 'fract_land' , 'fract_pft01', 'fract_pft02',
    'fract_pft03', 'fract_pft04', 'fract_pft05', 'fract_pft06', 'fract_pft07',
    'fract_pft08', 'fract_pft09', 'fract_pft10', 'fract_pft11', 'fract_veg'  ,
    'glac'       , 'lake'       , 'land'       ]

# -- Paths settings:
pin1 = f'{l4s.input_path()}/bc_land_frac.nc'
pin2 = f'{l4s.input_path()}/bc_land_frac_res.nc'
pout = f'{l4s.output_path()}/res4bc_control'

# -- Dimensions of data in NetCDF:
dim4mask = 1
dim4param = 1

# -- Parameters in NetCDF responsible for land and sea:
var1 = 'notsea'
var2 = 'sea'

# -- Settings for ICON land/sea mask:
set4mask_plots_ls = {
    'title' : 'ICON land/sea mask',
    'sea_color' : 'aqua',
    'land_color': 'peru',
    'labels' : ['Water cover', 'Land cover'],
    'vmin' : 0,
    'vmax' : 1,
    'pout_map' : f'{pout}/ICON_mask',
    'lcoastline': True,
    'lgrid_map' : True,
}

# -- Settings for ICON sea/land mask:
set4mask_plots_sl = {
    'title' : 'ICON sea/land mask',
    'sea_color' : 'aqua',
    'land_color': 'peru',
    'labels' : ['Land cover', 'Water cover'],
    'vmin' : 0,
    'vmax' : 1,
    'pout_map' : f'{pout}/ICON_mask',
    'lcoastline': True,
    'lgrid_map': True,
}

#-- Settings for other parameters in NetCDF (all data has values in range 0 - 1)
set4plot = {
    'title'  : 'ICON tricontourf plot',
    'cmap'   : 'afmhot_r',
    'varMin' : 0.0,
    'varMax' : 1.0,
    'varInt' : 0.2,
    'units'  : '--',
    'pout_map' : f'{pout}/plot_ICON',
    'lcoastline': True,
    'lgrid_map' : True,
}

# =============================    Main program   ======================
if __name__ == '__main__':
    # -- Create output folder:
    pout = l4s.makefolder(pout)

    # -- 1. Create land/sea and sea/land masks based on original and updated 
    #       ICON boundary condition files:
    # Get ICON data (for Land / Sea)
    get_param(
        set4mask_plots_ls, pin = pin1, var = var1, dims = dim4mask, prefix = f'{var1}_orig')
    get_param(
        set4mask_plots_ls, pin = pin2, var = var1, dims = dim4mask, prefix = f'{var1}_new')
    # Get ICON data (for Sea / Land)
    get_param(
        set4mask_plots_sl, pin = pin1, var = var2, dims = dim4mask, prefix = f'{var2}_orig')
    get_param(
        set4mask_plots_sl, pin = pin2, var = var2, dims = dim4mask, prefix = f'{var2}_new')

    # -- 2. Quality control and visualization of other data from NetCDF:
    for var in lst4param:
        print('Working with ', var)
        ds4param1, clon1, clat1 = l4p.get_ICON_data(pin1, var, dim4param)
        ds4param2, clon2, clat2 = l4p.get_ICON_data(pin2, var, dim4param)
        # -- Compare clat and clon values. We can do it only one time, because
        #    parameters are common for all dataset variables:
        if var == lst4param[0]:
            # -- Check latitude values:
            check_lat = l4p.check_param(clat1, clat2, 'clat')
            # -- Check longitude values:
            check_lon = l4p.check_param(clon1, clon2, 'clon')
        # -- Check main variables:
        check_var = l4p.check_param(ds4param1, ds4param2, var)
        # -- Visualization of other data from NetCDF:
        vis.icon_data(
            ds4param1, clon1, clat1, set4plot, var = var, prefix = f'{var}_orig')
        vis.icon_data(
            ds4param2, clon2, clat2, set4plot, var = var, prefix = f'{var}_new')
# ============================    End of program   =====================
