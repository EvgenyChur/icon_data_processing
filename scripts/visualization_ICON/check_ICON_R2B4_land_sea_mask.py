# -*- coding: utf-8 -*-
"""
Description: Creating figures with land/sea and sea/land masks based on ICON data

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    20.03.23 Evgenii Churiulin, MPI-BGC
           Initial release
"""

# =============================     Import modules     =======================
import lib4processing as l4p
import lib4sys_support as l4s
import lib4visualization as l4v

# ================   User settings (have to be adapted)  =====================
# -- Path settings:
com_path = 'C:/Users/evchur'
main = f'{com_path}/Desktop/DATA/FORCING_QUINCY'
# sea/land mask
pin_slm = main + '/slm_ICON_R2B4.nc'
# land/sea mask
pin_lsm = main + '/lsm_ICON_R2B4.nc'
# output path
pout = f'{com_path}/Python/scripts/github/icon_data_processing/RESULTS/res4_icon_masks'

#-- Settings for ICON sea/land or land/sea mask
set4mask_plots1 = {
    'title'     : 'ICON sea/land mask',
    'sea_color' : 'aqua',
    'land_color': 'peru',
    'labels'    : ['Land cover', 'Water cover'],
    'vmin'      : 0,
    'vmax'      : 1,
    'pout_map'  : f'{pout}/ICON_mask_sea',
    'lcoastline': True,
    'lgrid_map' : True,
}

set4mask_plots2 = {
    'title'     : 'ICON land/sea mask',
    'sea_color' : 'aqua',
    'land_color': 'peru',
    'labels'    : ['Water cover', 'Land cover'],
    'vmin'      : 0,
    'vmax'      : 1,
    'pout_map'  : f'{pout}/ICON_mask_notsea',
    'lcoastline': True,
    'lgrid_map' : True,
}

# =============================    Main program   =====================
if __name__ == '__main__':
    # -- Create output folder:
    pout = l4s.makefolder(pout)

    # -- 1. Get data for sea/land mask and create 2D map:
    ds4param1, clon1, clat1 = l4p.get_ICON_data(pin_slm, 'sea', dim = 1)
    l4v.plot_mask(ds4param1, clon1, clat1, set4mask_plots1, var = 'sea')

    # -- 2. Get data for land/sea mask and create 2D map:
    ds4param2, clon1, clat1 = l4p.get_ICON_data(pin_lsm, 'notsea', dim = 1)
    l4v.plot_mask(ds4param2, clon1, clat1, set4mask_plots2, var = 'notsea')
# ============================    End of program   ====================
