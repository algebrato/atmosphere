#!/usr/bin/python3
import os
import glob
import matplotlib.pylab as plt
from astropy.io import fits
from argparse import ArgumentParser, RawTextHelpFormatter
from distribution_merra2 import *
from distribution_era5 import *
from seasonal_maps import *

if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter, description="TOAST weather file generator")
    parser.add_argument("site", type=str, help="Site name")
    parser.add_argument('-p', '--path', default=".", type=str, help="Data Directory")
    parser.add_argument('-o', '--out_file', default="weather.fits", type=str, help="Output File")
    parser.add_argument('-ps', '--pix_size', type=float, default=0.35, help='Select the pixel size of your reanalysis')
    parser.add_argument('-npix', '--num_pix', default=1, type=int, help="Number of pixel")
    parser.add_argument('-m', '--seasonal_maps', action='store_true', help="Return the seasonal maps ")
    parser.add_argument('-var', '--variable', default="TQV", type=str, help="Atmospheric Variable")
    parser.add_argument('-ra', '--reanalysis', default='merra2', type=str, help='Select the reanalysis type of your data')


    args = parser.parse_args()

    print("Site Name   : {}".format(args.site))
    print("Out File    : {}".format(args.out_file))
    print("Working Path: {}".format(args.path))
    print("Seas. Maps  : {}".format(args.seasonal_maps))
    print("Spatial AVG : {}".format(args.num_pix))
    if args.seasonal_maps:
        print("Atm. Var    : {}".format(args.variable))

    if args.reanalysis == "merra2":

        try:
            file_list = sorted(glob.glob(args.path+"m*"))
            print("Num of files:\t", len(file_list))
        except FileNotFoundError as FnF:
            print("Error Number {0}; {1}".format(FnF.errno, FnF.strerror))

        if args.seasonal_maps:

            make_maps_merra2(args.site, args.path, file_list, args.out_file, args.num_pix, args.variable)

        else:

            distr = cumulative_distribution_merra2(args.site, args.path, file_list, args.out_file, args.num_pix)

            for i in range(0, 24):
                plt.plot(distr[i])
            plt.show()

    if args.reanalysis == "era5":

        try:
            file_list = sorted(glob.glob(args.path+"*.nc"))
            print("Num of files:\t", len(file_list))
        except FileNotFoundError as FnF:
            print("Error Number {0}; {1}".format(FnF.errno, FnF.strerror))

        if args.seasonal_maps:
            make_maps_era5(args.site, args.path, file_list, args.out_file, args.num_pix, args.variable)

        else:

            cumulative_distribution_era5(args.site, args.path, file_list, args.out_file, args.num_pix, args.pix_size)
