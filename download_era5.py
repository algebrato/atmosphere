import cdsapi
from netCDF4 import Dataset
from argparse import ArgumentParser, RawTextHelpFormatter

if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter, description="ERA-5 reanalysis download data")

    #parser.add_argument('-d','--day', default="01", type=str, help="Day")
    parser.add_argument('-m','--month', default="01", type=str, help="Month")
    #parser.add_argument('-y','--year', default="1980", type=str, help="Year")
    parser.add_argument('-mlon', '--min_lon', default="", type=str, help="Min Long")
    parser.add_argument('-mlat', '--min_lat', default="", type=str, help="Min Lat")
    parser.add_argument('-mxlon', '--max_lon', default="", type=str, help="Max Long")
    parser.add_argument('-mxlat', '--max_lat', default="", type=str, help="Max Lat")

    args = parser.parse_args()
    #day = args.day
    month = args.month
    #year = args.year
    out_file_name = month + ".nc"

    try:
        c = cdsapi.Client()
        c.retrieve('reanalysis-era5-single-levels', {
                'product_type': 'reanalysis',
                'format': 'netcdf',
                'variable': 'total_column_water_vapour',
                "expver": "0",
                'year': ['1981', '1982', '1983',
                         '1984', '1985', '1986',
                         '1987', '1988', '1989',
                         '1990', '1991', '1992',
                         '1993', '1994', '1995',
                         '1996', '1997', '1998',
                         '1999', '2000', '2001',
                         '2002', '2003', '2004',
                         '2005', '2006', '2007',
                         '2008', '2009', '2010',
                         '2011', '2012', '2013',
                         '2014', '2015', '2016',
                         '2017', '2018', '2019',
                         ],
                'month': [month],
                'day': [
                        '01', '02', '03',
                        '04', '05', '06',
                        '07', '08', '09',
                        '10', '11', '12',
                        '13', '14', '15',
                        '16', '17', '18',
                        '19', '20', '21',
                        '22', '23', '24',
                        '25', '26', '27',
                        '28', '29', '30',
                        '31',
                        ],
                'time': [
                    '00:00', '01:00', '02:00',
                    '03:00', '04:00', '05:00',
                    '06:00', '07:00', '08:00',
                    '09:00', '10:00', '11:00',
                    '12:00', '13:00', '14:00',
                    '15:00', '16:00', '17:00',
                    '18:00', '19:00', '20:00',
                    '21:00', '22:00', '23:00',
                    ],
                'area': [args.max_lat+"/"+args.min_lon+"/"+args.min_lat+"/"+args.max_lon],
                },
                out_file_name)
    except IOError as io:
        c.info("Something has gone wrong")
