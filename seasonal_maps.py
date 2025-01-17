# import os
import glob
import numpy as np
# import pandas as pd
import matplotlib.cm as cm
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
# from astropy.io import fits


def make_maps_merra2(site, path, month_list, out_file, npix, var):
    sites_dict = {'atacama': {'lllong': -72.0,
                              'lllat': -30.0,
                              'urlong': -65.0,
                              'urlat': -20.0},
                  'tenerife': {'lllong': -20.0,
                               'lllat': 26.0,
                               'urlong': -10.0,
                               'urlat': 31.0}, }

    lllong = sites_dict[site]['lllong']
    lllat = sites_dict[site]['lllat']
    urlong = sites_dict[site]['urlong']
    urlat = sites_dict[site]['urlat']

    id_month = 1
    for month in month_list:
        file_list = sorted(glob.glob(month+"/*"))
        array_of_days = np.zeros([24, 15, 17])
        k = 0
        for day in file_list:

            data = Dataset(day, mode='r')

            WV_l_tqv = data.variables[var][:, :, :]
            if np.shape(WV_l_tqv) == (24, 15, 17):
                if k == 0:
                    array_of_days = array_of_days + WV_l_tqv
                else:
                    array_of_days = np.append(array_of_days, WV_l_tqv, axis=0)
                k = k + 1

        month_median = np.median(array_of_days, axis=0)
        m = Basemap(llcrnrlon=lllong, llcrnrlat=lllat, urcrnrlon=urlong, urcrnrlat=urlat, projection='cyl', lon_0=0.0, lat_1=lllat, lat_2=urlat, resolution ='i')

        lons = data.variables['lon'][:]
        lats = data.variables['lat'][:]
        lon, lat = np.meshgrid(lons, lats)
        xi, yi = m(lon, lat)

        cs = m.pcolor(xi, yi, np.squeeze(month_median[:, :]), vmin=5.0, vmax=35.0, cmap=cm.jet)

        cs.set_edgecolor('face')
        m.drawparallels(np.arange(lllat, urlat, 1.), labels=[1, 0, 0, 0], fontsize=5)
        m.drawmeridians(np.arange(lllong, urlong, 1.), labels=[0, 0, 0, 1], fontsize=4)
        m.drawcoastlines()
        m.drawstates()
        m.drawcountries()

        cbar = m.colorbar(cs, location='bottom', pad="10%")
        cbar.set_label('')  # Insert the unit
        cbar.ax.tick_params(labelsize=10)
        plt.title('MERRA-2 ' + var + ' median value for : ' + str(id_month))
        figure = plt.figure(1)
        str_out = "month_" + str(id_month) + "_.png"

        try:
            figure.savefig(str_out, format='png', dpi=360)
            print("Month: {} done".format(id_month))
        except IOError as err:
            print("Error {}, number {}".format(err.strerror, err.errno))

        plt.clf()
        id_month = id_month + 1

    return 0


def make_maps_era5(site, path, month_list, out_file, npix, var):
    sites_dict = {'atacama': {'lllong': -72.0,
                              'lllat': -30.0,
                              'urlong': -65.0,
                              'urlat': -20.0},
                  'tenerife': {'lllong': -20.0,
                               'lllat': 26.0,
                               'urlong': -10.0,
                               'urlat': 31.0}, }

    lllong = sites_dict[site]['lllong']
    lllat = sites_dict[site]['lllat']
    urlong = sites_dict[site]['urlong']
    urlat = sites_dict[site]['urlat']

    id_month = 1
    for month in month_list:
        data = Dataset(month, mode='r')
        try:
            WV_l_tqv = data.variables[var][:, 0, :, :]
        except ValueError as verr:
            WV_l_tqv = data.variables[var][:, :, :]

        print(np.shape(WV_l_tqv))
        month_median = np.median(WV_l_tqv, axis=0)
        m = Basemap(llcrnrlon=lllong, llcrnrlat=lllat, urcrnrlon=urlong, urcrnrlat=urlat, projection='cyl', lon_0=0.0, lat_1=lllat, lat_2=urlat, resolution ='i')

        lons = data.variables['longitude'][:]
        lats = data.variables['latitude'][:]
        lon, lat = np.meshgrid(lons, lats)
        xi, yi = m(lon, lat)

        print(np.shape(xi), np.shape(yi), np.shape(month_median))

        cs = m.pcolor(xi, yi, np.squeeze(month_median[:, :]), vmin=5.0, vmax=35.0, cmap=cm.jet)

        cs.set_edgecolor('face')
        m.drawparallels(np.arange(lllat, urlat, 1.), labels=[1, 0, 0, 0], fontsize=5)
        m.drawmeridians(np.arange(lllong, urlong, 1.), labels=[0, 0, 0, 1], fontsize=4)
        m.drawcoastlines()
        m.drawstates()
        m.drawcountries()

        cbar = m.colorbar(cs, location='bottom', pad="10%")
        cbar.set_label('')  # Insert the unit
        cbar.ax.tick_params(labelsize=10)
        plt.title('ERA-5 ' + var + ' median value for : ' + str(id_month))
        figure = plt.figure(1)
        str_out = "month_" + str(id_month) + "ERA5_.png"

        try:
            figure.savefig(str_out, format='png', dpi=360)
            print("Month: {} done".format(id_month))
        except IOError as err:
            print("Error {}, number {}".format(err.strerror, err.errno))

        plt.clf()
        id_month = id_month + 1

    return 0
