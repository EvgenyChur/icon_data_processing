#!/bin/bash

#-------------------------------------------------------------------------------
# Task: Replace field in the original ICON boundary condition file:
#
# Current code owner: MPI-BGC
#
# Authors: Evgenii Churiulin
#
#   MPI-BGC, 2023
#   Evgenii Churiulin
#   phone:  +49 170-261-51-04
#   email:  evchur@bgc-jena.mpg.de
#-------------------------------------------------------------------------------

# ========================= Paths ============================================
main='/work/mj0143/b381275/CRUJRA2022/mask'

# ICON original boundary conditions file:
icon_bc_orig=${main}/'bc_land_frac.nc'
# ICON new boundary conditions file:
icon_bc_new=${main}/'bc_land_frac_res.nc'

# R2B4 land/sea mask
r2b4_lsm=${main}/'lsm_ICON_R2B4.nc'
# R2B4 sea/land mask
r2b4_slm=${main}/'slm_ICON_R2B4.nc'

cdo -replace ${icon_bc_orig} ${r2b4_lsm} ${icon_bc_new}.tmp
cdo -replace ${icon_bc_new}.tmp ${r2b4_slm} ${icon_bc_new}
rm ${icon_bc_new}.tmp
