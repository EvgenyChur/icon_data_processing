# Table of components:

1. create_land_sea_R2B4_mask.sh --> create land/sea mask based on R2B4 dataset (1 - land, 0 - sea). The main problem is no float data near coarse line, due to on next the create_land_sea_ICON_R2B4_mask.sh script has to be activated;

2. create_land_sea_ICON_R2B4_mask.sh --> create land/sea mask based on R2B4 and ICON datasets. The main benifit is float values close to coarse line. This mask option is more accurate then original R2B4;

3. create_T63_R2B4_annual_data.sh  --> script for processing of annual T63 and R2B4 data and visualization of them;

4. visualization_ICON --> folder with python scripts for data processing:

   - ***lib4processing.py*** --> processing of ICON data in NetCDF format. Module has functions:
      * get_ICON_data --> Get ICON data;
      * get_ICON_bnds --> Get ICON bnds values for longitude and latitude;
      * check_param --> Quality control of the research data.

   - ***lib4sys_support*** --> Module with functions for work with file system:
      * dep_clean --> Cleaning previous results;
      * makefolder --> Check and create folder;
      * get_info --> Get common information about datasets.

   - ***lib4visualization*** --> Module for visualization of ICON data:
      * plot_mask --> Visualization of land sea mask;
      * icon_data  --> Visialization of the research ICON parameter;
      * get_line_plot --> Create line plot for ICON research parameter;
      * tick_rotation_size --> Setting for x and y axis of linear plots.

   - ***bc_control*** --> Create 2D maps for controling values of ICON data in ICON bc_land_frac before updates and after;

   - ***check_forcing*** --> Comparison of annual CRUJRA data (longwave, wspeed, shortwave, tmin, tmax, qair, precip) presented on ICON_R2B4 land/sea mask with CRUJRA data presented on T63 land/sea mask. This script can be automatically run from create_T63_R2B4_annual_data.sh;

   - ***check_ICON_R2B4*** --> Creating figures with land/sea and sea/land masks based on ICON data. This script can be automatically run from create_land_sea_ICON_R2B4_mask.sh;

   - ***check_lsm*** --> Comparison of land/sea masks of CRUJRA datasets with tmin and tswrf (fd). This script can be automatically run from create_land_sea_R2B4_mask.sh


## How to use this scripts:

1. Create data on R2B4 grid based on CRUJRA forcing:
   a. gunzip_climate_data_CRUJRA.bash;
   b. remap_CRUJRA.bash;

2. We have to create land/sea mask based on R2B4. However, we have to be sure that
   CRUJRA_tmin and CRUJRA_tswrf (CRUJRA_fd) maps have simular land/sea pixels.
   For this purpose, we have to use create_land_sea_R2B4_mask.sh and check_lsm.py
   scripts;

3. We have to change R2B4 land/sea mask based on ICON coarse values. Otherwise,
   there is a big change to get problems with output data. For this purpose, we
   have to use - create_land_sea_ICON_R2B4_mask.sh and check_ICON_R2B4.py scripts;

3. Replace original fields (notsea and sea) in ICON file (bc_land_frac.nc) to a
   new one. For this purpose, we have to use - replace_land_sea_mask.sh script;

4. Run quality control test - run script bc_control.py;

5. We have to calculate the new forcing data based on updated ICON boundary
   conditions file (bc_land_frac_res.nc). For this purpose, we have to use -
   calculate_ICON_land_forcing_CRUJRA.bash script;

6. The last step is comparison of new CRUJRA forcing data with (R2B4_ICON land/sea mask)
   with CRUJRA forcing data with (T63 land/sea mask). For that, run
   create_T63_R2B4_annual_data.sh and check_forcing.py scripts. Look at the figures.
