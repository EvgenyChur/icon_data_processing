#!/bin/bash

#-------------------------------------------------------------------------------
# Task: Create land / sea mask
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

#module load cdo
module load nco

# ========================= Paths ===========================================
# Main intup paths
main='/work/mj0143/b381275/CRUJRA2022/mask'

# Input path with python script
pyt_main='/work/mj0143/b381275/CRUJRA2022/scripts/visualization_ICON_R2B4_data'

# Input data (ICON and R2B4 land sea mask)
pin1=${main}/icon_lsm.nc
pin2=${main}/ls_mask.nc

# Output data (land/sea and sea/land masks)
pout_lsm=${main}/lsm_ICON_R2B4.nc
pout_slm=${main}/slm_ICON_R2B4.nc
# ========================= Generation operations ===========================

# Select notsea ICON data from the original ICON boundary conditions file:
cdo -select,name=notsea ${main}/'bc_land_frac.nc' ${pin1}

# Creating a new file with differences in land/sea masks (diff = ICON - R2B4)
cdo -L -setname,diff -sub ${pin1} ${pin2} temp.nc

# Replace values to temporal constants:
#   a.  -1 --> 3333; ICON doesn't have land --> R2B4 has land (most of islands)
#                    change to ICON data
#
#   b.   0 --> 5555; ICON and R2B4 have land in pixel --> use R2B4 data
#
#   c.   1 --> 9999; ICON has land data, R2B4 doesn't have. ---> use R2B4 data
#
#   d. float values - should be saved without changes. R2B4 doesn't have fload
#                     values close to coarse line. In that case, we have to use
#                     ICON data
#
cdo setvals,-1,3333 temp.nc temp2.nc
cdo setvals,0,5555 temp2.nc temp3.nc
cdo setvals,1,9999 temp3.nc temp4.nc

# Replace constant values to ICON and R2B4 data
cdo ifthenelse -ltc,0 temp4.nc ${pin1} temp4.nc temp5.nc
cdo ifthenelse -eqc,9999 temp5.nc ${pin2} temp5.nc temp6.nc
cdo ifthenelse -eqc,5555 temp6.nc ${pin2} temp6.nc temp7.nc
cdo ifthenelse -eqc,3333 temp7.nc ${pin1} temp7.nc temp8.nc

# Rename attribute name and save new land/sea mask
cdo setname,notsea temp8.nc ${pout_lsm}

# Create sea/land mask
cdo -L -setname,slmask -subc,1 temp8.nc temp9.nc
cdo -L -mulc,-1 temp9.nc temp10.nc
cdo abs temp10.nc temp11.nc

# Rename attribute name and save new sea/land mask
cdo setname,sea temp11.nc ${pout_slm}

# Delete temporal files:
rm temp*.nc


#-- Run python script for fast visualization of lsm_ICON_R2B4.nc and
#   slm_ICON_R2B4.nc data
python3 ${pyt_main}/check_ICON_R2B4.py