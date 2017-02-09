# Libraries for reading the files
import os
import csv

# Libraries for manipulating and writing the final file
import numpy as np
import pandas as pd

# Initializing the list to be filled
combinedFile = []

# Root directory
root = 'E:/SSURGO Data'

# Loop to read through files within subdirectories
for path, subdirs, files in os.walk(root):
    for name in files:
        
        # Checks if the file has the correct name
        if name != 'mapunit.txt':
            pass
        else:
            
            # Opens the file, and appends it to the initalized list in csv form
            with open(os.path.join(path, name), "r") as file:
                csvfile = csv.reader(file, delimiter='|', quotechar='"')
                for row in csvfile:
                    combinedFile.append([x.replace('"', '') for x in row])

# Reads the list into a data frame for easier processing
dfSoil = pd.DataFrame(combinedFile)

# Removes duplicates and properly appends null values
dfSoil.replace('', np.NaN, inplace=True)
dfSoil.drop_duplicates(inplace=True)

# Uncomment if wishing to view the data frame
# dfSoil

# Writing the data frame to a csv within the same directory as this notebook
dfSoil.to_csv('soilDescriptions.csv', index=False)
