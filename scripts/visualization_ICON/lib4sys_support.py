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

# =============================     Import modules     ==================
import os
import pandas as pd
# =============================   Personal functions   ==================
def dep_clean(path:str):
    """ Cleaning previous results """
    for file in os.listdir(path):
        os.remove(path + file)


def makefolder(path:str) -> tuple[str]:
    """ Check and create folder """
    try:
        # There is no folder in our output place. Create a new one
        os.makedirs(path)
    except FileExistsError:
        # Folder already exist in our output place.
        pass
    return path + '/'


def get_info(
    df : pd.DataFrame,      # Dataset with data for the project
    df_name : str,          # Name of the dataset for information
    ):
    """ Get common information about datasets """
    print(f'Common information about - {df_name}')
    df.info()
    print(df.columns, '\n')
    print(f'Numbers of NaN values in the dataset - {df_name}', '\n')
    print(df.isnull().sum())
    print(f'Numbers of duplicates (explicit)in the dataset - {df_name}', '\n')
