import numpy as np
import pandas as pd
import re  # regex

# Weather Station key & geocode
dfStation = pd.read_table('~/Data/stationary/allstations.txt', header=None)

# Removes trailing whitespaces and extracts the latitude/longitude
dfStation = dfStation[0].apply(lambda x: pd.Series(re.sub(' +', ' ', x).split()[:3]))
dfStation.columns = ['Station', 'Latitude', 'Longitude']

# Set path to hourly directory to make reading hourly files easier
hourlyPath = '~/Data/product/hourly/'

# Set path to hourly directory to make reading hourly files easier
hourlyPath = 'E:/weather/normals/1981-2010/products/hourly/'

def read_hourly(col_name, file_name, divisor):
    """
    Creates a formatted data frame from the weather hourly normals
    """

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


# Combining data frames together
dfWeather = pd.merge(dfStation, dfTmp).merge(dfDewp).merge(dfCloud).merge(dfHtIdx) \
              .merge(dfCoolHrs).merge(dfHtHrs)
