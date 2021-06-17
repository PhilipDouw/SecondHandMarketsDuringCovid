
# =============================================================================
# Programm taking the retrieved row data and cleaning it in defined columns
# =============================================================================

# Used Libraries

import pandas as pd
import time
import os




def DataCleaning(DataFile, exceptions):
    
    # Creating an empty dataframe to input the cleaned data
    
    Labels = {'ID':[], 'Brand':[], 'Model':[], 'Price':[], 'Km':[], 'Cyl':[],  'Age':[], 'Color':[], 'NIP':[], 'Date':[]}

    CleanData = pd.DataFrame(data = Labels)
    
    
    # Holding track of time
            
    ts1 = time.perf_counter()
    
    
    # Looping for every vehicule

    for i in range(len(DataFile)):
        
        
        # Holding track of time
        
        ts2 = time.perf_counter()
        
        
        # Progress information printed on the console
        
        if i % int(ChunkSize/10) == 0 and i != 0:
            
            print(f'{i}: {round(i/len(DataFile)*100)}% in {round(ts2-ts1,2)} seconds')
            
        if i == len(DataFile)-1:
            
            print(f'{i + 1}: 100% in {round(ts2-ts1,3)} seconds \n')
        
        
        # Selecting the vehicule's id and sending it to the final Dataframe
        CleanData.loc[i, 'ID'] = str((DataFile.iloc[i, 0]))
        
        
        # Slicing the HTML title into separate words
        
        TempTitle = DataFile.iloc[i,1]
        
        TempTitle = TempTitle.split(' ')
        
        
        # try to fetch the price
        
        try:
            
            # Looking for keywords in the title
            
            for j in range(len(TempTitle)):
                
                # The keyword 'kaufen.' if our keyword. the model's name ended
                # 4 words prior.
                
                if TempTitle[j] == 'kaufen.':
                    
                    # For Model
                    TempModel = TempTitle[:j-2]
                    
                    # The Value before 'Anfrage' no Price is available
                    
                    if TempTitle[j-1] == 'Anfrage':
                        
                        CleanData.loc[i, 'Price'] = None
                        
                    # else, the price is in position keyword-2, we directly
                    # clean the Price of any unwanted symbols
                        
                    else:
                        
                        CleanData.loc[i, 'Price'] = int(TempTitle[j-1].replace("'", "").replace(".", "").replace("-", ""))
                        
            # fetching ccm & color which is always at the same position
            # regarding the key word "ccm"
            
                if TempTitle[j] =='ccm':
                    
                    CleanData.loc[i, 'Cyl'] = TempTitle[j-1]
                    
                    CleanData.loc[i, 'Color'] = TempTitle[j+1]
                     
            # using the exceptions at the bottom, separate the Brand & Model
            # depending of the length of the brand
            
            # Brand is 2 strings long
            
            if any(TempTitle[0] in s for s in exceptions[0]):
                
                CleanData.loc[i, 'Brand'] = TempTitle[0] + '_' + TempTitle[1]
                
                CleanData.loc[i, 'Model'] = '_'.join(TempModel[2:-3])
                
            # Brand is 3 strings long
            elif any(TempTitle[0] in s for s in exceptions[1]):
                
                CleanData.loc[i, 'Brand'] = TempTitle[0] + '_' + TempTitle[1] + '_' + TempTitle[2]
                
                CleanData.loc[i, 'Model'] = '_'.join(TempModel[3:-3])
                
            # Brand is 4 strings long
            elif any(TempTitle[0] in s for s in exceptions[2]):
                
                CleanData.loc[i, 'Brand'] = TempTitle[0] + '_' + TempTitle[1] + '_' + TempTitle[2] + '_' + TempTitle[3]
                
                CleanData.loc[i, 'Model'] = '_'.join(TempModel[4:-3])

            # Brand is 1 string long
            
            else:
                
                CleanData.loc[i, 'Brand'] = TempTitle[0]
                
                CleanData.loc[i, 'Model'] = '_'.join(TempModel[1:-3])
                
               
        # if an error was raised, set the price to None to avoid an error 
               
        except:
            
            CleanData.loc[i, 'Brand'] = 'nan'
            
            CleanData.loc[i, 'Model'] = 'nan'
            
            pass;
        
        
        # Some variables can be taken as is_

        # mileage
        
        CleanData.loc[i, 'Km'] = DataFile.iloc[i, 2]
        
        # Age
        
        CleanData.loc[i, 'Age'] = DataFile.iloc[i, 3]
        
        # NIP
        
        CleanData.loc[i, 'NIP'] = DataFile.iloc[i, 4]
        
        # Date
        
        CleanData.loc[i, 'Date'] = DataFile.iloc[i, 6]
        
        
    # the only element that is of use is the final dataframe containing all our data
        
    return CleanData
        
        
# selecting path

path = 'C:/Users/phili/OneDrive/Documents/CarThesisNew/AllMotoData'

os.chdir(path) # set working directory

del path
    

# Load the raw data

DataFile = 'combined_Moto_600000-1223999.csv'

rawData = pd.read_csv(DataFile)


# We will divide the dataset in a number of chunks (like sharing a cake) to limit
# the amount of RAM used for the process. We also initialize lists to store the
# different chunks of the dataset

ChunkSize = 1000

ListDfs = [None] * int((len(rawData)/ChunkSize))

ListCleanDfs = [None] * int((len(rawData)/ChunkSize))

# we can now divide our data into the different chunk lists we created

for i in range(int(len(rawData)/ChunkSize)):
    
    ListDfs[i] = rawData.loc[i * ChunkSize : (i * ChunkSize) + ChunkSize - 1]

# Exceptions list to know if the brand name is one, two or three strings long

exceptions = [['Arctic', 'Cf', 'Chang', 'City', 'E', 'Easy', 'Five', \
              'GAS', 'Ghezzi', 'Her', 'Moto', \
              'Motor', 'Mv' 'Mz', 'Smc', 'Spy', 'Valenti'],['Polaris'],['Generic']]
    

# Managing exceptions where Brand name is longer than 1 string

for k in range(len(exceptions)):
    
    for l in range(len(exceptions[k])):
        
        exceptions[k][l] = exceptions[k][l].split(' ')


# Holding track of the overall time
    
ts = time.perf_counter()


# looping through each chunk

for k in range(len(ListDfs)):
    
    # Holding track of the time per chunk and sending progress info to the console
    
    t1 = time.perf_counter()
    
    print(f'Start Cleaning set {k+1} of {len(ListDfs)}: \n')
    
    # Each chunk of 1000 vehicules goes through the above mentioned function
    # and will come out as a dataframe of cleaned data that we save in the 
    # created list
    
    ListCleanDfs[k] = DataCleaning(ListDfs[k], exceptions)
    
    # Holding track of the time per chunk and sending progress info to the console
    
    t2 = time.perf_counter()
    
    print(f'Finished in {round(t2-t1,3)} seconds')
    
    
# Once finished, we can merge/concacenate all the chunks of cleaned data together

MergedCleanData = pd.concat(ListCleanDfs)


# And finally save them as a new csv file before printing the overall timing
# results to the user

MergedCleanData.to_csv('Cleaned_{}.csv'.format(DataFile))

tf = time.perf_counter()

print(f'Finished cleaning of {len(rawData)} in {round(tf-ts,2)} seconds \n')
