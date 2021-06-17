# =============================================================================
# Code that checks the data for missing values and outputs a list of missing
# =============================================================================


# Used libraries

import os
import glob
import pandas as pd


# Selecting path

path = 'C:/Users/phili/OneDrive/Documents/CarThesisNew/Data/Auto'

os.chdir(path) # set working directory

del path

# Selecting the files to be checked (divided by datasets of 1 million vehicles
# to lower the load of the RAM)

extension = 'csv'

FileNames = glob.glob('combined_Auto*.{}'.format(extension))

FileNames = [x[:-4] for x in FileNames]


# Create an empty list for the missing IDs

missing = []


# Read the first file, go trough it using a loop and append the vehicle
# ID of all vehicles that have missing values

df = pd.read_csv('{}.csv'.format(FileNames[0]))
    
print('24k')
        
for i in range(len(df)):
    
    if i%100000 == 0:
        print(i)
        
    if df.iloc[i,1] == 'None':
        missing.append(df.iloc[i,0])
    
# Does the same as above with the next file

df = pd.read_csv('{}.csv'.format(FileNames[1]))

print('25k')
    

for i in range(len(df)):

    if i%100000 == 0:
        print(i)
        
    if df.iloc[i,1] == 'None':
        missing.append(df.iloc[i,0])
        
# Does the same as above with the next file
        
df = pd.read_csv('{}.csv'.format(FileNames[2]))
    
print('26k')
    
for i in range(len(df)):

    if i%100000 == 0:
        print(i)
        
    if df.iloc[i,1] == 'None':
        missing.append(df.iloc[i,0])
  
        
# create a list with the initial range of IDs and compare it to the ID of 
# vehicles in our list. This is to catch the ID of vehicles that are completly
# missing (i.e. no entry at all)
        
listOf26 = list(range(26000000,27000000))

listOfExisting26 = df['Unnamed: 0'].tolist()
    
for i in listOf26:
    if i in listOfExisting26:
        print(i)
        listOf26.remove(i)
        
missing.extend(listOf26)
        
    
df = pd.read_csv('{}.csv'.format(FileNames[3]))

print('27k')
    
for i in range(len(df)):

    if i%100000 == 0:
        print(i)
        
    if df.iloc[i,1] == 'None':
        missing.append(df.iloc[i,0])
        
listOf27 = list(range(27000000,28000000))

listOfExisting27 = df['Unnamed: 0'].tolist()
    
for i in listOf27:
    if i in listOfExisting27:
        print(i)
        listOf27.remove(i)
        
missing.extend(listOf27)


# Convert the ID's to strings (they are currently integers)

string_ints = [str(int) for int in missing]


# Save the list to a text file where every ID is on an individual line

textfile = open("MissingAuto10052021.txt", "w")
for element in string_ints:
    textfile.write(element + "\n")
textfile.close()
    

    



