# -*- coding: utf-8 -*-
"""
Task : Module with functions for work with file system

Autors of project: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    2022-11-11 Evgenii Churiulin, MPI-BGC
           Initial release
    1.2    2023-03-03 Evgenii Churiulin, MPI-BGC
           Add new function 3.
"""

# =============================     Import modules     ======================
import os

#=============================   Personal functions   =======================
# 1. Function --> dep_clean
def dep_clean(path:str):
    '''
    Task : Cleaning previous results

    Parameters
    ----------
    path : Path to the folder with results.
    '''
    for file in os.listdir(path):
        os.remove(path + file)

# 2. Function --> makefolder
def makefolder(path:str) -> tuple[str]:
    '''
    Task: Check and create folder

    Parameters
    ----------
    path : Path to the folder.

    Returns
    -------
    path_OUT : New path for output data
    '''
    # Create folder for output data
    try:
        # There is no folder in our output place. Create a new one
        os.makedirs(path)
    except FileExistsError:
        # Folder already exist in our output place.
        pass
    return path + '/'

# 3. Function --> get_info
def get_info(df, df_name):
    '''
    Task: Get common information about datasets

    df : Dataframe,
        The dataset with data for the project
    df_name : Objects
        The name of the dataset for information

    Returns
    -------
    None.
    '''
    print(f'Common information about - {df_name}')
    df.info()
    print(df.columns, '\n')
    print(f'Numbers of NaN values in the dataset - {df_name}', '\n')
    print(df.isnull().sum())
    print(f'Numbers of duplicates (explicit)in the dataset - {df_name}', '\n')