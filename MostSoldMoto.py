# =============================================================================
# Selecting the most sold models of cars which have at least 500 entries and
# create a dataframe for each one
# =============================================================================

# Used Libraries

import pandas as pd
import os


# Select path

path = 'C:/Users/phili/OneDrive/Documents/CarThesisNew/Moto'

os.chdir(path) # set working directory

del path


# Import data

df = pd.read_csv('Cleaned_combined_Moto_600000-1223999.csv')


# Count the number of occurences of each brand

mostSoldBrands = df['Brand'].value_counts()

# Select all brands that have at least 2000 entries

mostSoldBrands = mostSoldBrands[mostSoldBrands >= 2000]

mostSoldBrands = mostSoldBrands.index.to_list()


# Select all models for each brand which has at least 500 entries

mostSoldModels = []

for brand in mostSoldBrands:
    
    tempModels = df[df['Brand'] == brand]['Model'].value_counts()
    
    tempModels = tempModels[tempModels >= 1000]
    
    mostSoldModels.append(tempModels.index.to_list())
    
mostSoldModels = mostSoldModels[0:13]

# converting special charachters
    
for i in range(len(mostSoldModels)):
    
    d = {ord(x):"_" for x in "/"}
    
    mostSoldModels[i] = [x.translate(d) for x in mostSoldModels[i]]
    
    
# Select new path to save the new dataframes
    

path = 'C:/Users/phili/OneDrive/Documents/CarThesisNew/Moto/NewMostSold'

os.chdir(path) # set working directory

del path

for i in range(len(mostSoldBrands)):
    
    for model in mostSoldModels[i]:
        
        moto = df[(df['Brand'] == mostSoldBrands[i]) & (df['Model'] == model)]
        
        del moto['Unnamed: 0']
        
        FileName = mostSoldBrands[i] + '_' + model
        
        moto.to_csv('{}.csv'.format(FileName))
        
        print(FileName)
    









