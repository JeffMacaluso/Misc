import numpy as np
import pandas as pd
import re  # regex

# Weather Station key & geocode
dfStation = pd.read_table('~/Data/stationary/allstations.txt', header=None)

# Removes trailing whitespaces and extracts the latitude/longitude
dfStation = dfStation[0].apply(lambda x: pd.Series(re.sub(' +', ' ', x).split()[:3]))
dfStation.columns = ['Station', 'Latitude', 'Longitude']

# Set path to directories to shorten code for reading data
hourlyPath = '~/Data/product/hourly/'
monthlyPrecipPath = '~/Data/products/precipitation/'
monthlyTempPath = '~/Data/products/temperature/'



def read_hourly(col_name, file_name, divisor):
    """Creates a formatted data frame from the hourly weather normals"""

    # Formats the column names including a prefix for the weather type
    station_columns = ['Station', 'Month', 'Day']
    column_names = ([col_name+str(x) for x in range(1, 25)])
    column_names = station_columns+column_names

    df_hourly = pd.read_csv(hourlyPath+file_name, 
                     header=None, delim_whitespace=True,
                     names = column_names)

    # Sets missing values to NaN
    df_hourly.replace('-9999', np.NaN, inplace=True)

    # Split - Extracting to avoid calculations
    column_order = df_hourly[['Station', 'Month', 'Day']]

    # Apply - Removing flags and converting to the proper format
    formatted_values = df_hourly.replace('[\D]', '', regex=True).astype(float) / divisor
    formatted_values = formatted_values.drop(['Station', 'Month', 'Day'], axis=1)

    # Combine
    df_hourly = pd.merge(column_order, formatted_values, left_index=True, right_index=True)

    return(df_hourly)


# Hourly Temperature
dfTmp = read_hourly('Tmp', 'hly-temp-normal.txt', 10)

# Hourly Dewpoint
dfDewp = read_hourly('Dew', 'hly-dewp-normal.txt', 10)

# Hourly Cloud Coverage - Specifically Overcast %
dfCloud = read_hourly('Cloud', 'hly-clod-pctovc.txt', 10)

# Hourly Cloud Coverage
dfHtIdx = read_hourly('HtIdx', 'hly-hidx-normal.txt', 10)

# Hourly Cloud Coverage
dfCoolHrs = read_hourly('CoolHr', 'hly-cldh-normal.txt', 10)

# Hourly Cloud Coverage
dfHtHrs = read_hourly('HtHr', 'hly-htdh-normal.txt', 10)


# Combining hourly data frames
dfHourlyWeather = pd.merge(dfStation, dfTmp).merge(dfDewp).merge(dfCloud).merge(dfHtIdx) \
              .merge(dfCoolHrs).merge(dfHtHrs)


def read_monthly(col_name, file_name, path, divisor):
    """Creates a formatted data frame from the monthly weather normals"""

    # Formats the column names including a prefix for the weather type
    station_columns = ['Station']
    column_names = ([col_name+str(x) for x in range(1, 13)])
    column_names = station_columns+column_names

    df_monthly = pd.read_csv(path+file_name, 
                     header=None, delim_whitespace=True,
                     names = column_names)

    # Sets missing values to NaN
    df_monthly.replace('-9999', np.NaN, inplace=True)

    # Split - Extracting to avoid calculations
    column_order = df_monthly[['Station']]

    # Apply - Removing flags and converting to the proper format
    formatted_values = df_monthly.replace('[\D]', '', regex=True).astype(float) / divisor
    formatted_values = formatted_values.drop(['Station'], axis=1)

    # Combine
    df_monthly = pd.merge(column_order, formatted_values, left_index=True, right_index=True)

    return(df_monthly)

# Monthly Precipitation
dfPrecip = read_monthly('Precip', 'mly-prcp-normal.txt', monthlyPrecipPath, 100)

# Monthly Minimum Temperature
dfMthlyTmpMin = read_monthly('MthlyTmpMin', 'mly-tmin-normal.txt', monthlyTempPath, 10)

# Monthly Maximum Temperature
dfMthlyTmpMax = read_monthly('MthlyTmpMax', 'mly-tmax-normal.txt', monthlyTempPath, 10)

# Monthly Average Temperature
dfMthlyTmpAvg = read_monthly('MthlyTmpAvg', 'mly-tavg-normal.txt', monthlyTempPath, 10)


# Combining monthly data frames
dfMonthlyWeather = pd.merge(dfStation, dfMthlyTmpMin).merge(dfMthlyTmpMax).merge(dfMthlyTmpAvg)
