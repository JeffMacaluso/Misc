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


# Hourly Temperature Normals
# Formats the column names including a prefix for the weather type
station_columns = ['Station', 'Month', 'Day']
tmp_columns = (['Tmp'+str(x) for x in range(1, 25)])
tmp_columns = station_columns+tmp_columns

# Temperature normals
dfTmp = pd.read_csv(hourlyPath+'hly-temp-normal.txt', 
                     header=None, delim_whitespace=True,
                     names = tmp_columns)

# Sets missing values to NaN
dfTmp.replace('-9999', np.NaN, inplace=True)

# Extracting to avoid calculations
tmp_order = dfTmp[['Station', 'Month', 'Day']]

# Removing flags and converting to the proper format
formatted_tmp = dfTmp.replace('[\D]', '', regex=True).astype(float) / 10
formatted_tmp = formatted_tmp.drop(['Station', 'Month', 'Day'], axis=1)

dfTmp = pd.merge(tmp_order, formatted_tmp, left_index=True, right_index=True)


# Hourly Dewpoint Normals
# Formats the column names including a prefix for the weather type
station_columns = ['Station', 'Month', 'Day']
dew_columns = (['Dew'+str(x) for x in range(1, 25)])
dew_columns = station_columns+dew_columns
dfDewp = pd.read_csv(hourlyPath+'hly-dewp-normal.txt', 
                     header=None, delim_whitespace=True,
                     names = dew_columns)

# Sets missing values to NaN
dfDewp.replace('-9999', np.NaN, inplace=True)

# Extracting to avoid calculations
dewp_order = dfDewp[['Station', 'Month', 'Day']]

# Removing flags and converting to the proper format
formatted_dewp = dfDewp.replace('[\D]', '', regex=True).astype(float) / 10
formatted_dewp = formatted_dewp.drop(['Station', 'Month', 'Day'], axis=1)

dfDewp = pd.merge(dewp_order, formatted_dewp, left_index=True, right_index=True)


# Hourly Cloud Coverage
# Formats the column names including a prefix for the weather type
station_columns = ['Station', 'Month', 'Day']
cloud_columns = (['Cloud'+str(x) for x in range(1, 25)])
cloud_columns = station_columns+cloud_columns

dfCloud = pd.read_csv(hourlyPath+'hly-cldh-normal.txt', 
                     header=None, delim_whitespace=True,
                     names = cloud_columns)

# Sets missing values to NaN
dfCloud.replace('-9999', np.NaN, inplace=True)

# Extracting to avoid calculations
cloud_order = dfCloud[['Station', 'Month', 'Day']]

# Removing flags and converting to the proper format
formatted_cloud = dfCloud.replace('[\D]', '', regex=True).astype(float) / 10
formatted_cloud = formatted_cloud.drop(['Station', 'Month', 'Day'], axis=1)

dfCloud = pd.merge(cloud_order, formatted_cloud, left_index=True, right_index=True)


# Combining data frames together
dfWeather = pd.merge(dfStation, dfTemp).merge(dfDewp).merge(dfCloud)
