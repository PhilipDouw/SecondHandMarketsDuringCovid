# =============================================================================
# Code to retrieve motorcycle data from a webpage
# =============================================================================

# Used libraries

import time
import random
import numpy as np
import pandas as pd
import concurrent.futures
import requests
from requests_futures.sessions import FuturesSession
from bs4 import BeautifulSoup
import os


# Selecting path
path = 'C:/Users/phili/OneDrive/Documents/CarThesisNew'

os.chdir(path) # set working directory

del path

# =============================================================================
# Functions
# =============================================================================

# Function that takes an ID as input, retrieves the html code and converts
# it to a "soup" using the BeautifulSoup library

def get_url(n):
    
    
    print(f'beginning ID {IDs[n]}')
    
    # wait some time to lower the chances of overloading the client server
    time.sleep(random.uniform(0.05, 0.1))
    
    # retrieve the html code using the FuturesSession library
    Result[n] = session.get(str(url) + str(IDs[n])) # 0.02s
    
    # Save the HTML code in a list with all others htmls
    response[n] = Result[n].result() # 0.5s
    
    # save the "content" of the HTML code in a list
    vhcSource[n] = response[n].content # 0.01s
    
    # Convert the content into a soup to make it easier to use
    soups[n] = BeautifulSoup(vhcSource[n], 'lxml') # 0.3s
    
    print(f'Done with ID {IDs[n]}')

def GetVhcInfo(soup):

    try:
        ### Fetching variable values from our source file ###
    
        ### Adding "title" value to our lsit. We want to do this first since we
        ### want the title in the first position of our list (position 0).
        ## Creates values list with vehicule title as first element by separating
        ## words with a space
        valueList = [(' '.join(soup.title))]
        
        # ### Preparing title to fetch infos from it (these infos are always available)
        # ## Put title in a temporary list ## need to check if faster with numpy arrays pr not
        # infoTemp = np.array([' '.join(soup.title)])
        # ## Splits title into a list of words ## Creates list inside list...
        # infoTemp = [i.split() for i in infoTemp]
        # ## For the first element in infoTemp, 5th list starting at the end of
        # ## the list, everything except the last three characters into values list
    
        ### Adding Kilometrage, Première mise en circulation and Code postal
        ## Look for any <div> where class=row show-for-xsmall-only columns
        for i in soup.findAll('div', {'class': 'row show-for-xsmall-only columns'}):
            vLTemp = [(''.join(i.findAll(text=True)))]
            vLTemp = [l.split() for l in vLTemp]

            ## Append Kilometrage to values list
            valueList.append(vLTemp[0][-1])
            ## Append Première mise en circulation to values list
            valueList.append(vLTemp[0][-2])
            ## Append Code postal to values list
            valueList.append(vLTemp[0][0])
            # ValueList.extend(vLTemp)
            valueList.append(vLTemp)
    
        ### Adding Date de mise en ligne
        for i in soup.findAll('div', {'class': 'row xsmall-12 columns'}):
            vLTemp = [(''.join(i.findAll(text=True)))]
            vLTemp = [l.split() for l in vLTemp]
            valueList.append(vLTemp[0][-1])
            valueList.append(vLTemp)
            
        ### Adding Description
        # ()for i in soup.findAll('div', {'class': 'column'})
    
        ### Adding all values which amount changes for every vehicule ID
        ## Search for every dd and only output what's in between the <dd> ... <\dd>
        for k in soup.findAll('dd'):
            vLTemp = [(''.join(k.findAll(text=True)))]
            valueList.extend(vLTemp)
    
    
        ### Fetching variable names from our source file ###
    
        ### Initializing names list
        ## We already input column names that are invariant regarless of which ID
        namesList = ['Titre', 'Km', 'PmeC', 'CP', 'Info', 'DateAnnonce', 'InfoDateAnnonce']
        
        ### Adding column names that are different for every vehicule ID
        ## Search for every dt and only output what's in between the <dt> ... <\dt>
        for i in soup.findAll('dt'):
            namesList.append(''.join(i.findAll(text=True)))
    
    
        ### Converting our lists into a dictionary###
    
        ## Creates a dictionary with our two lists as input
        vhcDictionary = dict(zip(namesList, valueList))
    
        ## Function will return a dictionary
    except:
        
        namesList = ['Titre', 'Prix', 'Marque', 'Modele', 'Cylindree', 'Couleure', 'Kilometrage', 'Premiere mise en circulation', 'Code Postal', 'Parution']
        valueList = ['None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None']
        
        vhcDictionary = dict(zip(namesList, valueList))
        
    return vhcDictionary


# initialise the session to retrieve multiple htmls at once
session = FuturesSession()

# Select base URL
url = "https://www.comparis.ch/motorrad/marktplatz/details/show/"

# Select file size (number of IDs per file), first ID and last ID
NbIDs = 1000
IDsStart = 1200000
IDsEnd = 1223614

# Create a list which divides the range of IDs into chunks of the same size
IDsStartsList = np.arange(IDsStart, IDsEnd, NbIDs).tolist()

# Select how many chunks of ID to do
for i in range(len(IDsStartsList)):
    
    # initialise the timer 
    ts = time.perf_counter()
    
    # Create empty lists to be filled with the above functions
    IDs = np.arange(IDsStartsList[i], IDsStartsList[i] + NbIDs, 1).tolist()
    Result = [None] * NbIDs
    response = [None] * NbIDs
    vhcSource = [None] * NbIDs
    soups = [None] * NbIDs
    Nbfutures = list(range(NbIDs))
    DicList = []
    
    # Perform the "get_url" function for each chunk in the selected range
    with concurrent.futures.ThreadPoolExecutor() as executor:
      
        # [executor.submit(get_url, Nbfutures[n]) for n in Nbfutures]
        executor.map(get_url, Nbfutures)

    # get the finishing time and output it to the user
    tf = time.perf_counter()
    
    print(f'Finished with IDs {IDsStartsList[i]} - {IDsStartsList[i] + NbIDs} in {round(tf - ts, 2)} second(s)')    
    
    ts2 = time.perf_counter()
    
    # Perform the second function for the whole chunk    
    for j in range(len(soups)):
        DicList.append(GetVhcInfo(soups[j]))
        
    # Create a dataframe using the created dictionnary
    df = pd.DataFrame(DicList)
    
    IDList = np.arange(IDsStartsList[i], IDsStartsList[i] + NbIDs, 1)
    
    df.index = IDList
    
    ## Input for filename
    IDForFileName = (str(IDsStartsList[i]) + '-' + str(IDsStartsList[i] + NbIDs - 1))
    fileNameEnd = ''.join(IDForFileName)
    
    df.to_csv('Data/Moto2020_{}.csv'.format(fileNameEnd))
    
    # overall time 
    tf2 = time.perf_counter()
    
    
    # Print the name of the chunk that is finished, and output the overall time

    print(f'Finished developping data in {round(tf2 - ts2, 2)} second(s)')
    
    print(f'Whole process for {IDsStartsList[i]} - {IDsStartsList[i] + NbIDs} took {round(tf2 - ts, 2)} second(s)')

    del DicList, IDForFileName, IDList, IDs, Nbfutures, Result, df, executor, fileNameEnd, i, j, response, soups, tf, tf2, ts, ts2, vhcSource
print('Everything is finished, wow')