# -*- coding: utf-8 -*-
"""
Description: Module for visualization of ICON data

Authors: Evgenii Churiulin

Current Code Owner: MPI-BGC, Evgenii Churiulin
phone:  +49  170 261-5104
email:  evgenychur@bgc-jena.mpg.de

History:
Version    Date       Name
---------- ---------- ----
    1.1    07.03.2023 Evgenii Churiulin, MPI-BGC
           Initial release
"""

# =============================     Import modules     =======================
import time
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import colors
import cartopy.crs as ccrs
import cartopy
import cartopy.feature as cfeature
from typing import Optional

import warnings
warnings.filterwarnings("ignore")

# =============================   Personal functions   ======================
# Function --> tick_rotation_size
def xticks_settings(ax:plt.Axes, rotation:float, fsize:int):
    """Additional settings for x ticks labels"""
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(rotation)
        label.set_fontsize(fsize)


def yticks_settings(ax:plt.Axes, rotation:float, fsize:int):
    """Additional settings for y ticks labels"""
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(fsize)


def timer(func):
    """Time calculator"""
    def wrapper(*args, **kwargs):
        #-- retrieve start time
        t1 = time.time()
        res = func(*args, **kwargs)
        # -- retrieve stop time
        t2 = time.time()
        #-- get wallclock time
        print('Wallclock time:  %0.3f seconds\n' % (t2-t1))
        return res
    return wrapper


class Plot_settings:
    def __init__(self):
        # Set common parameters for all figures:
        # -- Settings for 1D plots:
        self.title = 'title'    # Common plot title
        self.clr   = 'black'    # Color of labels
        self.fsize = 14         # Size of labels
        self.pad   = 20         # Space betveen axis and label
        self.l_pos = 'upper left'  # Legend location
        self.gtype = 'major'    # Which axis do you want to use for grid (major or)
        self.gclr  = 'grey'     # Grid color
        self.gstyle= 'dashed'   # Grid line style
        self.galpha= 0.2        # Grid transparacy
        self.txaxis_format = '%Y'
        self.plt_format = 'png'
        self.plt_dpi = 300
        # -- Settings for 2D maps:
        self.mglw = 0.5         # Map grid line width
        self.mgcol = 'dimgray'  # Map grid line color
        self.mgalp = 0.4        # Map grid transparency
        self.mgzord = 2.0       # Map grid zoom order
        self.msave_dpi = 150.0  # DPI for map
        self.mbbox = 'tight'    #
        self.lw_coast = 0.5     # Size of coastline
        self.zord_coast = 2.0   # zoom order of coastline


    def plt_uset_maps(self, ax, uset):
        """ User settings for 2D plot"""
        # -- Add plot title to 2D map:
        if 'title' in uset and len(uset.get('title')) > 0:
            plt.title(uset.get('title'))
        # -- Add coastlines to 2D map:
        if 'lcoastline' in uset and uset.get('lcoastline'):
            ax.coastlines(linewidth = self.lw_coast, zorder = self.zord_coast)
        # -- Add grid for 2D maps:
        if 'lgrid_map' in uset and uset.get('lgrid_map'):
            ax.gridlines(
                draw_labels = uset.get('lgrid_map'),
                linewidth = self.mglw,
                color = self.mgcol,
                alpha = self.mgalp,
                zorder = self.mgzord,
            )

        # -- Save figure:
        if 'pout_map' in uset and len(uset.get('pout_map')) > 0:
            if 'prefix' in uset and len(uset.get('prefix')) > 0:
                plt.savefig(
                    f"{uset.get('pout_map')}_{uset.get('prefix')}.{self.plt_format}",
                    bbox_inches = self.mbbox,
                    dpi = self.msave_dpi,
                )
            else:
                plt.savefig(
                    f"{uset.get('pout_map')}.{self.plt_format}",
                    bbox_inches = self.mbbox,
                    dpi = self.msave_dpi,
                )
        else:
            plt.show()


    def plt_uset_line(self, ax, uset):
        """ User settings for 1D plot"""
        # -- Set plot title:
        if 'title' in uset and len(uset.get('title')) > 0:
            ax.set_title(
                uset.get('title'),
                color = self.clr,
                fontsize = self.fsize,
                pad = self.pad,
            )
        # -- Set x axis label:
        if 'xlabel' in uset:
            ax.set_xlabel(
                uset.get('xlabel'),
                color = self.clr,
                fontsize = self.fsize,
                labelpad = self.pad,
            )
        # -- Set y axis label:
        if 'ylabel' in uset:
            ax.set_ylabel(
                uset.get('ylabel'),
                color = self.clr,
                fontsize = self.fsize,
                labelpad = self.pad,
            )
        # -- Set X axis ticks paramters for numbers:
        if 'xlim_num' in uset and len(uset.get('xlim_num')) > 0:
            ax.set_xticks(np.arange(uset.get('xlim_num')[0],
                                    uset.get('xlim_num')[1],
                                    uset.get('xlim_num')[2]))
                # -- Set X axis ticks parameters for time axis:
        if 'xlim_time' in uset and len(uset.get('xlim_time')) > 0:
            ax.set_xlim(
                pd.to_datetime(uset.get('xlim_time')[0], format='%d.%m.%Y'),
                pd.to_datetime(uset.get('xlim_time')[1], format='%d.%m.%Y'),
            )
            xftm = mdates.DateFormatter(self.txaxis_format)
            ax.xaxis.set_major_formatter(xftm)
            ax.xaxis.set_minor_locator(days)
        #-- Extra parameters for ticks: (ax, rotation, size)
        if 'x_rotation' in uset:
            xticks_settings(ax, uset.get('x_rotation'), self.fsize)
        # -- Set Y axis ticks parameters:
        if 'ylim_num' in uset and len(uset.get('ylim_num')) > 0:
            ax.set_yticks(
                np.arange(
                    uset.get('ylim_num')[0],
                    uset.get('ylim_num')[1],
                    uset.get('ylim_num')[2],
                )
            )
        #-- Extra parameters for ticks: (ax, rotation, size)
        if 'y_rotation' in uset:
            yticks_settings(ax, uset.get('y_rotation'), self.fsize)
        # -- Add legend:
        if 'llegend' in uset and uset.get('llegend'):
            ax.legend(loc = self.l_pos)
        # -- Add grid settings:
        if 'lgrid' in uset and uset.get('lgrid'):
            ax.grid(
                uset.get('lgrid'),
                which = self.gtype,
                color = self.gclr,
                linestyle = self.gstyle,
                alpha = self.galpha,
            )
        # -- Set output parameters:
        if 'output' in uset and len(uset.get('output')) > 0:
            #-- Plot save
            plt.savefig(
                f"{uset.get('output')}.{self.plt_format}",
                format = self.plt_format,
                dpi = self.plt_dpi,
            )
        else:
            plt.show()


@timer
def plot_mask(
    # Input parameters:
    data : xr.DataArray,                                  # ICON (land/sea) data for visualization
    clon : np.array,                                      # longitude
    clat : np.array,                                      # latitude
    set4plot: dict,                                       # user settings
    **kwargs,                                             # other parameters (optional)
    # Output parameters:
    ):                                                    # Create 2D map in the output folder
    """Visualization of land sea mask"""
    # -- Local variables:
    mwidth = 10
    mlength = 10
    ncols = 2                                             # number of columns for legend
    maps_settings = Plot_settings()                       # user settings class
    projection = ccrs.PlateCarree()                       # type of projection
    sea_color = set4plot.get('sea_color')                 # pixel colors for water
    land_color = set4plot.get('land_color')               # pixel colors for land
    cmap = colors.ListedColormap([sea_color, land_color]) # colormap based on input colors

    #-- Create figure and axes instances; we need subplots for plot and colorbar
    fig, ax = plt.subplots(
        figsize = (mwidth, mlength),
        subplot_kw = dict(projection = projection),
    )
    # -- Make the map global rather than have it zoom in to the extents of any plotted data
    ax.set_global()
    #-- Contour plot:
    cnf = ax.tricontourf(
        clon,
        clat,
        data,
        vmin = set4plot.get('vmin'),
        vmax = set4plot.get('vmax'),
        cmap = cmap,
    )

    #-- Add legend:
    leg_sea  = mpatches.Rectangle((0, 0), 1, 1, facecolor = sea_color)
    leg_land = mpatches.Rectangle((0, 0), 1, 1, facecolor = land_color)
    plt.legend(
        [leg_sea, leg_land],
        set4plot.get('labels'),
        loc = 'lower center',
        fancybox = True,
        ncol = ncols,
        bbox_to_anchor = (0.5, -0.2),
    )
    if 'prefix' in kwargs and len(kwargs['prefix']) > 0:
        set4plot['prefix'] = kwargs['prefix']
    # -- Set other user settings parameters:
    maps_settings.plt_uset_maps(ax, set4plot)


@timer
def icon_data(
    # Input parameters:
    data : xr.DataArray,                                  # ICON (land/sea) data for visualization,
    clon : np.array,                                      # longitude
    clat : np.array,                                      # latitude
    set4plot: dict,                                       # user settings
    **kwargs,                                             # other parameters (optional)
    # Output parameters:
    ):                                                    # Create 2D map in the output folder
    """ Visialization of the research ICON parameter """
    # -- Local variables:
    mwidth = 10
    mlength = 10
    nanvals = -9999
    cmap_extend = 'neither'
    maps_settings = Plot_settings()                       # user settings class
    projection = ccrs.PlateCarree()                       # type of projection
    varMin = set4plot.get('varMin')                       # min values
    varMax = set4plot.get('varMax')                       # max values
    varInt = set4plot.get('varInt')                       # step between values
    units = set4plot.get('units')                         # units for labels
    #-- Replace NaN values
    data4plot = np.nan_to_num(data, nan = nanvals)
    # -- Set contour levels, labels:
    levels = np.arange(varMin, varMax+varInt, varInt)
    nlevs  = levels.size
    labels = ['{:.2f}'.format(x) for x in levels]
    # -- Set colormap for nlevs:
    cmap = plt.get_cmap(set4plot.get('cmap'), nlevs)
    #-- print information to stdout
    print(kwargs['var'])
    print('')
    print('Cells:            %6d ' % clon.size)
    print('Variable min/max: %6.2f ' % np.nanmin(data)+'/'+' %.2f' % np.nanmax(data))
    print('Contour  min/max: %6.2f ' % varMin+'/'+' %.2f' % varMax)
    print('')
    #-- Create figure and axes instances; we need subplots for plot and colorbar:
    fig, ax = plt.subplots(
        figsize=(mwidth, mlength),
        subplot_kw=dict(projection=projection),
    )
    ax.set_global()
    # -- Contour plot
    cnf = ax.tricontourf(
        clon,
        clat,
        data4plot,
        vmin = varMin,
        vmax  = varMax,
        levels = levels,
        cmap = cmap,
        extend = cmap_extend,
        zorder = 0,
    )
    #-- Add a color bar      x,    y,    w,    h
    cbar_ax = fig.add_axes([0.2, 0.25, 0.6, 0.015], autoscalex_on = True) 
    cbar = fig.colorbar(cnf, cax=cbar_ax, orientation = 'horizontal')
    plt.setp(cbar.ax.get_xticklabels()[::2], visible = False)
    cbar.set_label(f'[{units}]')
    # Add prefix to figure:
    if 'prefix' in kwargs and len(kwargs['prefix']) > 0:
        set4plot['prefix'] = kwargs['prefix']
    # -- Set other user settings parameters:
    maps_settings.plt_uset_maps(ax, set4plot)



def get_line_plot(
    # Input parameters:
    mode : str,                                          # Type of input data for visualization
    set4plot : dict,                                     # User settings for plot
    data_xr : Optional[list[xr.DataArray]] = None,       # Input data in xarray format
    data_df : Optional[list[pd.DataFrame]] = None,       # Input data in pd.DataFrame format
    years : Optional[np.array] = None,                   # Actual years when xarray data
    var : Optional[list[int]] = None,                    # Actual parameter when pd.Series
    # Output parameters:
    ):                                                   # Create and save output figure
    """Create line plot for research parameter"""
    # -- Local variables:
    maps_settings = Plot_settings()                      # user settings class

    if data_xr != None:
        niter = len(data_xr)
    elif data_df != None:
        niter = len(data_df)

    #-- Create plot:
    fig = plt.figure(figsize = (12,7))
    ax  = fig.add_subplot(111)
    for i in range(niter):
        # -- Define correct index and data for visualization:
        index = years      if mode == 'DataArray' else data_df[i].index
        data  = data_xr[i] if mode == 'DataArray' else data_df[i][var[i]]
        # -- Add new line to the plot:
        ax.plot(
            index,
            data,
            label = set4plot.get('legends')[i],
            color = set4plot.get('colors')[i] ,
            linestyle = set4plot.get('styles')[i],
         )
    # -- Apply user settings:
    maps_settings.plt_uset_line(ax, set4plot)
    #-- Clean memory
    plt.close(fig)
    plt.gcf().clear()
