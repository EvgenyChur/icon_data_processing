# -*- coding: utf-8 -*-
"""
Description: Module with processing functions for working with ICON data

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    07.03.2022 Evgenii Churiulin, MPI-BGC
           Initial release
"""
# =============================     Import modules     ======================
import sys
import numpy as np
import pandas as pd
import xarray as xr
import warnings
warnings.filterwarnings("ignore")

# =============================   Personal functions   =================
class UnitConverter:
    def __init__(self):
        self.micromol2mol = 1e-6    # micro-mol in mole
        self.molc2gramm   = 12.0107 # mole C in gC
        self.moln2o_gramm = 44.0128 # mole N2O in gN2O
        self.moln2gramm   = 14.0067 # mole N to gN
        self.sec_1day     = 86400   # seconds in 1 day
        self.gc2kgc       = 1000    # gC in kgC
        self.gc2pgc       = 1e-15   # gC in PgC
        self.g2tg         = 1e-12   # g in Tg (teragram)
        self.kg2pg        = 1e-12   # kg in PgC
        self.area = 'area'


    def gpp_converter(self, ds:xr.DataArray,var:str, mode:str):
        """Convert GPP units from:
            1. Linear plot: μmolC m-2 s-1 --> PgC yr-1;
            2. 2D Map: μmolC m-2 s-1 -> gC m-2 yr-1"""
        # -- 1. Units for linear plot:
        if mode == 'lplot':
            # μmolC m-2 s-1 -> molC m-2 s-1 -> gC m-2 s-1 ->
            # -> PgC m-2 s-1 -> PgC s-1 -> PgC yr-1
            ds[var] = (
                ds[var] * self.micromol2mol * self.molc2gramm * self.sec_1day *
                ds[var].time.dt.days_in_month * self.gc2pgc * ds[self.area])
        # -- 2. Units for 2D maps:
        if mode == '2dmap':
            # μmolC m-2 s-1 -> molC m-2 s-1 -> gC m-2 yr-1
            ds[var] = (
                ds[var] * self.micromol2mol * self.molc2gramm * self.sec_1day *
                ds[var].time.dt.days_in_month)
        return ds


    def cveg_converter(self, ds:xr.DataArray,var:str, mode:str):
        """Convert cVeg units from:
            1. Linear plot: molC m-2 -> PgC
            2. 2D Map: molC s-1 --> kgC"""
        # -- 1. Units for linear plot:
        if mode == 'lplot':
            # molC m-2 --> gC m-2 -> PgC m-2 -> PgC
            ds[var] = ds[var] * self.molc2gramm * self.gc2pgc * ds[self.area]
        # -- 2. Units for 2D maps:
        if mode == '2dmap':
            # mol C s-1 --> kgC
            ds[var] = ds[var] * self.molc2gramm / self.gc2kgc
        return ds


    def n2o_converter(self, ds:xr.DataArray,var:str, mode:str):
        """Convert N2O units from:
            1. Linear plot: μmol N2O m-2 s-1 to TgN yr-1
            2. 2D Map: μmol N2O m-2 s-1 -> gN m-2 yr-1"""

        # Step 1: μmol N2O m-2 s-1 -> μmol N m-2 s-1
        ds[var] = (ds[var] ) * 2
        # -- 1. Units for linear plot:
        if mode == 'lplot':
            # μmol N m-2 s-1 -> mol N m-2 s-1 -> gN m-2 s-1 -> Tg N m-2 s-1 -> TgN s-1 -> TgN yr-1
            ds[var] = (
                ds[var] * self.micromol2mol * self.moln2gramm * self.sec_1day *
                ds[var].time.dt.days_in_month * self.g2tg * ds[self.area])
        # -- 2. Units for 2D maps:
        if mode == '2dmap':
            # μmol N m-2 s-1 -> mol N m-2 s-1 -> gN m-2 s-1
            ds[var] = (
                ds[var] * self.micromol2mol * self.moln2gramm * self.sec_1day *
                ds[var].time.dt.days_in_month)
        return ds


    def het_resp_converter(self, ds:xr.DataArray,var:str, mode:str):
        """Converter heterotrophic respiration from:
            1. Linear plot: μmol C m-3 s-1 to PgC yr-1
            2. 2D Map: μmol C m-3 s-1 to gC m-2 yr-1"""
        # -- Step 1: Get actual layer depths:
        soil_layers = ds['soil_layer_sb'].values
        hlayers = []
        for i in range(len(soil_layers)):
            if i == 0:
                lev_diff = 0 - soil_layers[i]
            else:
                lev_diff = soil_layers[i-1] - soil_layers[i]
            hlayers.append(abs(lev_diff))
        # -- Step 2: Convert μmol C m-3 s-1 --> μmol C m-2 s-1
        for i in range(len(soil_layers)):
            ds[var][:,i,:] = ds[var][:,i,:] * hlayers[i]
        # Get total values over layers:
        ds[var] = ds[var].sum(dim = {'soil_layer_sb'})
        # -- 1. Units for linear plot:
        if mode == 'lplot':
            # -- Step 3: Convert
            # μmol C m-2 s-1 -> mol C m-2 s-1 -> gC m-2 s-1 -> PgC m-2 s-1 -> PgC s-1 -> PgC yr-1
            ds[var] = (
                ds[var] * self.micromol2mol * self.molc2gramm * self.sec_1day *
                ds[var].time.dt.days_in_month * self.gc2pgc * ds[self.area])
        # -- 2. Units for 2D maps:
        if mode == '2dmap':
            # Convert:
            # μmol m-2 s-1 --> mol C m-2 s-1 --> gC m-2 s-1 --> gC m-2 yr-1
            ds[var] = (
                ds[var] * self.micromol2mol * self.molc2gramm * self.sec_1day *
                ds[var].time.dt.days_in_month)
        return ds
