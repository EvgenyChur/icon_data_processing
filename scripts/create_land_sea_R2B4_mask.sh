#!/bin/bash

#-------------------------------------------------------------------------------
# Task: Create land / sea mask
#
# Current code owner:
#
#   MPI-BGC
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
#========================= Settings ============================================
tmin_file='crujra_v2.3_R2B4_tmin_2021.nc'

param1='tmin'
param2='tswrf'  # 'fd'
param3='ls_mask'
param4='sl_mask'

var='Minimum temperature at 2m'

#========================= Paths ===============================================
# Input path with python script
pyt_main='/work/mj0143/b381275/CRUJRA2022/scripts/visualization_ICON_R2B4_data'

main='/work/mj0143/b381275/CRUJRA2022'

pin_tmin=${main}"/DATA/"${tmin_file}
pout_mask1=${main}"/DATA/"${param3}.nc
pout_mask2=${main}"/DATA/"${param4}.nc
#========================= Generation operations ===============================

#-- We would to use tmin temperature data as an original file for creation land
#   sea mask. Moreover, we want to compare the values for land and sea between
#   tmin and tswrf variables due to the different type of initial data.
python3 ${pyt_main}/check_lsm.py ${param1} ${param2} ${param3}

#-- 1. Create (Land - Sea mask)
echo 'Create land sea mask'
#-- Replace none nan values to 1 (select land).
cdo setrtoc,0,1000,1 ${pin_tmin} temp.nc

#-- Replace NaN values to -9999 and then to 0
cdo setmisstoc,-9999. temp.nc temp2.nc
cdo setrtoc,-12000,-8000,0 temp2.nc temp3.nc

#-- Select only 1 moment of time
cdo seltimestep,1 temp3.nc temp4.nc

#-- Rename attribute name
#cdo chname,tmin,notsea temp4.nc ${pout_mask1}
cdo chname,tmin,lsmask temp4.nc ${pout_mask1}
ncatted -O -h -a long_name,lsmask,m,c,"Land_Sea_mask" ${pout_mask1}

#-- Delete temporal files
rm temp.nc temp2.nc temp3.nc temp4.nc
echo "Land Sea mask was created"

#-- 2. Create (Sea - Land mask)
echo 'Create sea land mask'
#-- Replace none nan values to 1 (select land).
cdo setrtoc,0,1000,0 ${pin_tmin} temp.nc

#-- Replace NaN values to -9999 and then to 0
cdo setmisstoc,-9999. temp.nc temp2.nc
cdo setrtoc,-12000,-8000,1 temp2.nc temp3.nc

#-- Select only 1 moment of time
cdo seltimestep,1 temp3.nc temp4.nc

#-- Rename attribute name
cdo chname,tmin,sea temp4.nc ${pout_mask2}
ncatted -O -h -a long_name,sea,m,c,"Sea_Land_mask" ${pout_mask2}

#-- Delete temporal files
rm temp.nc temp2.nc temp3.nc temp4.nc
echo "Sea land mask was created"