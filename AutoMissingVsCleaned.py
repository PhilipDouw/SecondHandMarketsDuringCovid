# =============================================================================
# Programm to put multiple Cleaned Datasets together in order, regardless of index continuity
# =============================================================================


# Used Libraries

import os
import glob
import pandas as pd


# Selecting Path

path = 'C:/Users/phili/OneDrive/Documents/CarThesisNew/Data/CleanedAuto'

os.chdir(path) # set working directory

del path


# Importing Datasets

WithMissing = pd.read_csv('Cleaned_combined_Auto_All.csv')

Missing = pd.read_csv('Cleaned_Cleaned_combined_Chunks.csv')

MissingChunks = pd.read_csv('Cleaned_Auto2021_ChunksToClean.csv')

del WithMissing['Unnamed: 0'], Missing['Unnamed: 0'], MissingChunks['Unnamed: 0']


# Values needed for later use to define the smallest and largest index available
# in the datasets

FirstIndex = WithMissing.nsmallest(1, ['ID']).iloc[0,0]

LastIndex = Missing.nlargest(1, ['ID']).iloc[0,0]

# Uncomment to check which is the largest and smaller index available

# WithMissing.nsmallest(1, ['ID'])
# Missing.nsmallest(1, ['ID'])
# MissingChunks.nsmallest(1, ['ID'])
# WithMissing.nlargest(1, ['ID'])
# Missing.nlargest(1, ['ID'])
# MissingChunks.nlargest(1, ['ID'])


# Setting the ID of vehicle as index and deleting any duplicate rows

WithMissing = WithMissing.drop_duplicates(subset='ID').set_index('ID')

Missing = Missing.drop_duplicates(subset='ID').set_index('ID')

MissingChunks = MissingChunks.drop_duplicates(subset='ID').set_index('ID')


# Creating an empty dataframe with range of index from smallest index largest 
# index available

columns = WithMissing.columns.to_list()

index = list(range(FirstIndex, LastIndex + 1))

Finaldf = pd.DataFrame(index = index, columns=columns)


# Looping through the first dataset and replacing data in final dataframe

index = WithMissing.index

for i in index:
    
    if (i-24000000)%10000 == 0:
        print((i - 24000000)/(27192495 - 24000000))
    
    Finaldf.loc[i] = WithMissing.loc[i]
    
# Doing a backup in case of problems
    
backup = Finaldf


# Looping through the second dataset and replacing data in final dataframe
    
index = Missing.index
    
for i in index:
    
    if str(i)[-2:] == '00':
        print(i)
    
    Finaldf.loc[i] = Missing.loc[i]
    
backup = Finaldf


# Looping through the last dataset and replacing data in final dataframe

index = MissingChunks.index

for i in index:
    
    if str(i)[-2:] == '00':
        print(i)
    
    Finaldf.loc[i] = MissingChunks.loc[i]


# Saving final dataframe with consolidated data

Finaldf.to_csv('Complete_Cleaned_Auto_24m_27075k.csv')


# Not used but maybe helpfull

# Finaldf.update(WithMissing.set_index('ID'))
# Finaldf.update(WithMissing)
# Finaldf = Finaldf.update(Missing)
# Finaldf = Finaldf.update(MissingChunks)
