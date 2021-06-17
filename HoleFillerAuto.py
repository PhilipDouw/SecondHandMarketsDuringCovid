# =============================================================================
# Code very similar to retrieveing Auto but which can take a list of IDs to
# retrieve the data of
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
    
    # print(f'beginning ID {IDs[n]}') # for manual check
    
    # information that will be sent to the client server
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'From': 'youremail@domain.com'  # This is another valid field
    }
    
    # a list of fictive IP adresses that will be sent to the client server
    
    ProxyListhttps = [    
    '85.26.146.169:80',
    '137.59.155.14:80',
    '93.170.123.200:9999',
    '177.220.226.122:50151',
    '213.230.127.140:3128',
    '223.244.137.124:3256',
    '85.216.127.185:8080',
    '36.92.5.194:8089',
    '45.79.39.147:3128',
    '195.53.49.11:3128',
    '37.235.96.200:3128',
    '193.200.151.69:48241',
    '167.172.109.12:36271',
    '222.186.190.62:31081',
    '117.24.80.93:3256',
    '45.84.58.230:80',
    '180.211.248.222:8080',
    '117.197.102.193:80',
    '221.1.205.74:8060',
    '110.50.84.231:42851',
    '139.162.78.109:3128',
    '58.176.147.14:80',
    '37.235.97.13:3128',
    '92.172.165.187:8080',
    '193.106.130.249:8080']
    
    # selecting a random IP adress from the above list
    
    https = 'http://'
    
    ProxyList = [https + sub for sub in ProxyListhttps]
    
    x = random.randint(0,len(ProxyListhttps))
    
    Proxy = ProxyList[x]
    
    # wait some time to lower the chances of overloading the client server
    time.sleep(random.uniform(0.1, 0.2))
    
    # retrieve the html code using the FuturesSession library
    Result[n] = session.get(str(url) + str(IDs[n]),headers=headers, proxies={'http': Proxy}) # 0.02s
    
    # Save the HTML code in a list with all others htmls
    response[n] = Result[n].result() # 0.5s
    
    # save the "content" of the HTML code in a list
    vhcSource[n] = response[n].content # 0.01s
    
    # Convert the content into a soup to make it easier to use
    soups[n] = BeautifulSoup(vhcSource[n], 'lxml') # 0.3s
    
    # print(f'Done with ID {IDs[n]}')
  
    
# function that takes the above created soup and only keeps usefull data

def GetVhcInfo(soup):


    ### Fetching variable values from our source file ###

    ### Adding "title" value to our lsit. We want to do this first since we
    ### want the title in the first position of our list (position 0).
    ## Creates values list with vehicule title as first element by separating
    ## words with a space
    valueList = [(' '.join(soup.title))]
    
    valueList.append(soup.findAll('meta', {'class': 'swiftype'}, {'name': 'body'}))
        

    ### Adding Kilometrage, Première mise en circulation and Code postal
    ## Look for any <div> where class=row show-for-xsmall-only columns
    for i in soup.findAll('div', {'class': 'row show-for-xsmall-only columns'}):
        vLTemp = [(''.join(i.findAll(text=True)))]
        vLTemp = [l.split() for l in vLTemp]
        valueList.append(vLTemp)
        
        try:
            ## Append Kilometrage to values list
            valueList.append(vLTemp[0][-2])
            ## Append Première mise en circulation to values list
            valueList.append(vLTemp[0][-3])
        except:
            valueList.append('error')
            valueList.append('error')
        # ## Append Code postal to values list
        # valueList.append(vLTemp[0][0])
        # # ValueList.extend(vLTemp)
        # valueList.append(vLTemp)


    ### Adding Date de mise en ligne
    
    for i in soup.findAll('div', {'class': 'row xsmall-12 columns'}):
        vLTemp = [(''.join(i.findAll(text=True)))]
        vLTemp = [l.split() for l in vLTemp]
        valueList.append(vLTemp[0][-1])
        valueList.append(vLTemp)
        

    ### Adding all values which amount changes for every vehicule ID
    ## Search for every dd and only output what's in between the <dd> ... <\dd>
    # Only works for active posts
    for k in soup.findAll('dd'):
        vLTemp = [(''.join(k.findAll(text=True)))]
        valueList.extend(vLTemp)

    ### Fetching variable names from our source file ###

    ### Initializing names list
    ## We already input column names that are invariant regarless of which ID
    namesList = ['Titre', 'Description', 'Description2', 'Km', 'PmeC', 'DateAnnonce', 'InfoDateAnnonce']
    
    ### Adding column names that are different for every vehicule ID
    ## Search for every dt and only output what's in between the <dt> ... <\dt>
    for i in soup.findAll('dt'):
        namesList.append(''.join(i.findAll(text=True)))


    ## Creates a dictionary with our two lists as input
    vhcDictionary = dict(zip(namesList, valueList))

    # return the created dictionary    
    return vhcDictionary


# initialise the session to retrieve multiple htmls at once
session = FuturesSession()

# Select the base url
url = "https://www.comparis.ch/carfinder/marktplatz/details/show/"

# Select the number of IDs that will be performed togheter
NbIDs = 2500

# we can either select a list of IDs or simply input a range of IDs

# list of missing IDs
# MissingIds = open("Data/Auto/MissingAuto10052021.txt", "r")
# Missing = MissingIds.readlines()

# Missing = [line[:-1] for line in Missing]

# Range of missing IDs
Missing = list(range(22400000, 23285000)) # number of chunks: 354

# Separate the ID's into chunks of 2500 IDs

chunks = [Missing[x:x+NbIDs] for x in range(0, len(Missing), NbIDs)] # 286 chunks


# Select how many chunks of ID to do
for i in range(0,99):

    # initialise the timer    
    ts = time.perf_counter()
    
    # Create empty lists to be filled with the above functions
    IDs = chunks[i]
    Result = [None] * NbIDs
    response = [None] * NbIDs
    vhcSource = [None] * NbIDs
    soups = [None] * NbIDs
    Nbfutures = list(range(NbIDs))
    DicList = []
    
    # Perform the "get_url" function for each chunk in the selected range

    with concurrent.futures.ThreadPoolExecutor() as executor:
      
        executor.map(get_url, Nbfutures)
        
    # get the finishing time and output it to the user
    tf = time.perf_counter()
    
    print(f'Finished with Chunk {i} of Chunk{len(chunks)} in {round(tf - ts, 2)} second(s)')    
    
    ts2 = time.perf_counter()
    
    # Perform the second function for the whole chunk
    
    for j in range(len(soups)):
        
        DicList.append(GetVhcInfo(soups[j]))
        
    # Create a dataframe using the created dictionnary

    df = pd.DataFrame(DicList)
    
    IDList = chunks[i]
    
    df.index = IDList
    
    ## Input for filename
    IDForFileName = ('Chunk' + str(i))
    
    fileNameEnd = ''.join(IDForFileName)
    
    
    # Save the dataframe of each chunk as a csv file
    
    df.to_csv('Data/2017S2/Auto2017_{}.csv'.format(fileNameEnd))
    
    # overall time    
    tf2 = time.perf_counter()
    
    
    # Print the name of the chunk that is finished, and output the overall time

    print(f'Finished developping data in {round(tf2 - ts2, 2)} second(s)')
    
    print(f'Whole process for Chunk {i} of Chunk{len(chunks)} took {round(tf2 - ts, 2)} second(s)')

    del DicList, IDForFileName, IDList, IDs, Nbfutures, Result, df, executor, fileNameEnd, i, j, response, soups, tf, tf2, ts, ts2, vhcSource
    
print('Everything is finished, wow')