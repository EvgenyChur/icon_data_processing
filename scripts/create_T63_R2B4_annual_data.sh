#!/bin/bash

#-------------------------------------------------------------------------------
# Task: Creating annual values of T63 and ICON_R2B4 datasets in one point and
#       comparing them to each other
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
#module load nco
#========================= Settings ============================================
proc_T63=1             # Do you want to calculate annual values in 1 point for T63 dataset?
proc_ICON_R2B4=1       # Do you want to calculate annual values in 1 point for ICON_R2B4 dataset?
comp_T63_ICON_R2B4=1   # Do you want to compare T63 and ICON_R2B4 dataset?

#========================= Paths ===============================================

# -- Input paths:
data_T63_in='/pool/data/JSBACH/jsbalone_forcing/T63/CRUJRA/data/crujra_v2.3'
data_ICON_R2B4_in='/scratch/b/b381275/FORCING/cal_forc'
pyt_script='/work/mj0143/b381275/CRUJRA2022/scripts/visualization_ICON_R2B4_data'

# -- Output paths
pout_temp='/work/mj0143/b381275/CRUJRA2022/DATA/TEMP'
pout='/work/mj0143/b381275/CRUJRA2022/DATA'

t63_outname='climate_crujra_v2.3_T63_1901-2021_zone_1p_annual.nc'
icon_r2b4_outname='climate_crujra_v2.3_R2B4_1901-2021_zone_1p_annual.nc'
#========================= Generation operations ===============================

# -- Get T63 data for analysis:
if [ $proc_T63 == 1 ]; then
    cdo -mergetime ${data_T63_in}/Climate_crujra_v2.3_T63_*.nc ${pout_temp}/temp.nc
    cdo -sellonlatbox,-180,180,90,-60 ${pout_temp}/temp.nc ${pout_temp}/temp_zone.nc
    cdo -fldmean ${pout_temp}/temp_zone.nc ${pout_temp}/temp_zone_1p.nc
    cdo -yearmean ${pout_temp}/temp_zone_1p.nc ${pout}/${t63_outname}
    # Delete temporal NetCDF:
    rm {pout_temp}/*.nc
fi

# -- Get ICON_R2B4 data for analysis:
if [ $proc_ICON_R2B4 == 1 ]; then
    cdo -mergetime ${data_ICON_R2B4_in}/Climate_crujra_v2.3_R2B4_*.nc ${pout_temp}/temp.nc
    cdo -sellonlatbox,-180,180,90,-60 ${pout_temp}/temp.nc ${pout_temp}/temp_zone.nc
    cdo -fldmean ${pout_temp}/temp_zone.nc ${pout_temp}/temp_zone_1p.nc
    cdo -yearmean ${pout_temp}/temp_zone_1p.nc ${pout}/${icon_r2b4_outname}
    # Delete temporal NetCDF:
    rm {pout_temp}/*.nc
fi

# -- Run script for comparison:
if [ $comp_T63_ICON_R2B4 == 1 ]; then
    python3 ${pyt_script}/check_forcing.py
fi
