# =============================================================================
# Code that takes multiple csv files and merges them together
# =============================================================================

# Used libraries

import os
import glob
import pandas as pd

# Selecting path

path = 'C:/Users/phili/OneDrive/Documents/CarThesisNew/Data/2017S2'

os.chdir(path) # set working directory

del path

# Selecting all files that are of type extension (.csv in our case)

extension = 'csv'
all_filenames = [i for i in glob.glob('Auto2017_Chunk*.{}'.format(extension))]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

#export to csv
combined_csv.to_csv( "combined_2017s1.csv", index=False, encoding='utf-8-sig')

