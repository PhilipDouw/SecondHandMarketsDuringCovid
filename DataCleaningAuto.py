
# =============================================================================
# Programm taking the retrieved row data and cleaning it in defined columns
# =============================================================================

# Used Libraries

import pandas as pd
import time
import os


# Function that takes a Dataset as input and cleans it into defined columns

def DataCleaning(DataFile):
    
    # Holding count of number of errors
    
    Errors = 0
    
    
    # Creating an empty dataframe to input the cleaned data
    
    Labels = {'ID':[], 'Brand':[], 'Model':[], 'Price':[], 'Km':[], 'Engine':[],  'Age':[], 'Color':[], 'NIP':[], 'Date':[]}

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
                    TempModel = TempTitle[:j-4]
                    
                    # The Value before 'Anfrage' no Price is available
                    
                    if TempTitle[j-1] == 'Anfrage':
                        
                        CleanData.loc[i, 'Price'] = None
                    
                    # else, the price is in position keyword-2, we directly
                    # clean the Price of any unwanted symbols
                        
                    else:
                        
                        CleanData.loc[i, 'Price'] = int(TempTitle[j-2].replace("'", "").replace(".", "").replace("-", ""))
        
        # if an error was raised, set the price to None to avoid an error
        
        except: 
            
            CleanData.loc[i, 'Price'] = None
            
            
        # Next we join the brand and model of the vehicule together
            
        try:
            
            CleanData.loc[i, 'Brand'] = TempModel[0]
            
            CleanData.loc[i, 'Model'] = '_'.join(TempModel[1:])
            
        # again accounting for missing data
            
        except:
            
            CleanData.loc[i, 'Brand'] = None
            
            CleanData.loc[i, 'Model'] = None
        
        
        # The Km usually comes retrieved at a specific place and can be taken
        # as is
        
        try:
            
            CleanData.loc[i, 'Km'] = DataFile.iloc[i, 4].replace("'", "")
            
        except:
            
            CleanData.loc[i, 'Km'] = None
            
            
        # fetching the date of publication while accounting for a possible shift
        # in columns depending the the amount of values that we managed to retrieve
            
        try:
            
            if DataFile.iloc[i,6] != 'error':
                
                CleanData.loc[i, 'Date'] = DataFile.iloc[i,6]
                
            else:
                
                if len(DataFile.iloc[i,7]) == 10:
                    
                    CleanData.loc[i, 'Date'] = DataFile.iloc[i,7]
                    
        # again accounting for missing data
        
        except:
            
            CleanData.loc[i, 'Date'] = None
            
        
        # Fetching the initial entry into service date, same as above
            
        try:
            
            if len(DataFile.iloc[i,5]) == 7:
                
                CleanData.loc[i, 'Age'] = DataFile.iloc[i,5]
                
            else:
                
                CleanData.loc[i, 'Age'] = CleanData.loc[i, 'Date'][3:]
                
        except:
            
            CleanData.loc[i, 'Age'] = None
            

        # Other usefull data such as the color and the engine specifics
        
        try:
            
            # taking the description and dividing it into words
            
            TempDescr = DataFile.iloc[i,2]
            
            TempDescr = TempDescr.split('<meta')
            
            TempDescrEngine = TempDescr[2].split(' ')
            
            # looping through the "sentence" and looking for keywords and like
            # above it becomes a game of finding the correct offset for the
            # correct value
            
            for k in range(len(TempDescrEngine)):
                
                if TempDescrEngine[k][0:7] == 'content':
                    
                    first = k
                    
                else:
                    
                    pass
                
                if TempDescrEngine[k] == CleanData.loc[i, 'Age']:
                    
                    second = k
                    
                else:
                    
                    pass
                    
                # the color is after the word 'km'
                
                if TempDescrEngine[k] == 'km':
                    
                    CleanData.loc[i, 'Color'] = TempDescrEngine[k+1]
                    
                else:
                    
                    pass
                
            # The enging type or more precisly the model's specifics are
            # always between the two words 'content' and the date of first 
            # entry into service date
                    
            engineType = TempDescrEngine[first+len(TempModel)+1:second]
            
            # it can be that we take a bit too much, therefore we might need
            # to get rid of a word if it is present in our model's specifics
            
            CleanData.loc[i, 'Engine'] = ' '.join(engineType)  
            
            for x in range(len(engineType)):
                
                if engineType[x] == 'fuer':
                    
                    fuer = x
                    
                    CleanData.loc[i, 'Engine'] = ' '.join(engineType[:fuer-1])
                    
                else:
                    
                    pass
                
        
        # As usual, an excepetion in case of an error and also saving the amount
        # of error's occurences
    
        except:
            
            Errors += 1
            
            pass
        
    # Showing the user the progress in the console as well as the number of 
    # errors encountered
    
    print(f'Total errors is {Errors} of {len(DataFile)}, or {round((Errors/len(DataFile))*100,2)} percent')
    
    
    # the only element that is of use is the final dataframe containing all our data
    
    return CleanData
        

# selecting path

path = 'C:/Users/phili/OneDrive/Documents/CarThesisNew/Data/Auto/FinalHoleFiller'

os.chdir(path) # set working directory

del path
    

# Loading raw data and deleting the first column as it is the index from the
# old dataframe

DataFile = 'combined_Chunks_Final.csv'

rawData = pd.read_csv(DataFile)

# del rawData['Unnamed: 0']


# We will divide the dataset in a number of chunks (like sharing a cake) to limit
# the amount of RAM used for the process. We also initialize lists to store the
# different chunks of the dataset

ChunkSize = 5000

ListDfs = [None] * int((len(rawData)/ChunkSize))

ListCleanDfs = [None] * int((len(rawData)/ChunkSize))

# we can now divide our data into the different chunk lists we created

for i in range(int(len(rawData)/ChunkSize)):
    
    ListDfs[i] = rawData.loc[i * ChunkSize : (i * ChunkSize) + ChunkSize - 1]

    
# Holding track of the overall time

ts = time.perf_counter()


# looping through each chunk

for k in range(len(ListDfs)):
    
    # Holding track of the time per chunk and sending progress info to the console
    
    t1 = time.perf_counter()
    
    print(f'Start Cleaning set {k+1} of {len(ListDfs)}: \n')
    
    
    # Each chunk of 5000 vehicules goes through the above mentioned function
    # and will come out as a dataframe of cleaned data that we save in the 
    # created list
    
    ListCleanDfs[k] = DataCleaning(ListDfs[k])
    
    
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