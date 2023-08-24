# -*- coding: utf-8 -*-
"""
Description: Script for analysis of CO2 and C13 and C14 isotopes:

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    15.04.2023 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    23.08.2023 Evgenii Churiulin, MPI-BGC
           Updated according to the lib4visualization changes 
"""

# =============================     Import modules     ================
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import lib4visualization as l4v
import lib4sys_support as l4s
# =============================   Personal functions   ================
def get_co2(path):
    """Get CO2 data from database file"""
    # read data
    df = pd.read_csv(path, header = None, sep = '\s+')
    return (df.set_index((df[0] - 0.5)
              .astype('int64'), drop = True)
              .drop([0], axis = 1))

# ================   User settings (have to be adapted)  ==============
# -- Input and output paths:
path_c02y_dc13 = f'{l4s.input_path()}/DATA_CO2/delta13C_in_air_input4MIPs_GM_1850-2021_extrapolated.txt'
path_c02y_dc14 = f'{l4s.input_path()}/DATA_CO2/Delta14C_in_air_input4MIPs_SHTRNH_1850-2021_extrapolated.txt'
fout = f'{l4s.output_path()}/check4delta'

# -- Plot settings:
set4plot_dc13 = {
    'legends' : ['CO2Y_DC13'],
    'colors' : ['blue'],
    'styles' : ['-'],
    'title' : ('Check CO2 values in '
               'delta13C_in_air_input4MIPs_GM_1850-2021_extrapolated file'),
    'xlabel' : 'Date, yr',
    'ylabel' : 'CO2, per-mill',
    'x_rotation' : 0,
    'ylim_num' : [-6.5, -9.1, -0.25],
    'llegend' : True,
    'lgrid' : True,
    'output' : f'{fout}/delta13',
}

set4plot_dc14 = {
    'legends' : ['CO2Y_DC14_var1', 'CO2Y_DC14_var2', 'CO2Y_DC14_var3'],
    'colors' : ['red', 'blue', 'green'],
    'styles' : ['-', '-.', '--'],
    'title' : ('Check CO2 values in '
               'Delta14C_in_air_input4MIPs_SHTRNH_1850-2021_extrapolated file'),
    'xlabel' : 'Date, yr',
    'ylabel' : 'CO2, per-mill',
    'x_rotation' : 0,
    'ylim_num' : [-50.0, 850.1, 50.0],
    'llegend' : True,
    'lgrid' : True,
    'output' : f'{fout}/delta14',
}

# -- Columns for visualization:
var_dc13 = [1]
var_dc14 = [1,2,3]

# =============================    Main program   =====================
if __name__ == '__main__':
    # Create output folder:
    output_folder = l4s.makefolder(fout)
    # Get CO2 data + C13 and C14 isotopes:
    df_dc13 = get_co2(path_c02y_dc13)
    df_dc14 = get_co2(path_c02y_dc14)
    # Visualization of CO2 data (c13 and c14 isotopes):
    l4v.get_line_plot(
        'DataFrame', set4plot_dc13, data_df = [df_dc13], var = var_dc13)
    l4v.get_line_plot(
        'DataFrame', set4plot_dc14, data_df = [df_dc14, df_dc14, df_dc14], var = var_dc14)
# =============================    End of program   =================== 
