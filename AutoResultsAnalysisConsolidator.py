# =============================================================================
# take all analysis results csv files and consolidate the results in one signle file
# =============================================================================


# Used libraries

import os
import glob
import pandas as pd

# Select the path with the analysis results files

path = 'C:/Users/phili/OneDrive/Documents/CarThesisNew/Data/CleanedAuto/NewMostSoldincl2017/AnalysisChowTestResults/WithDeletedEngines'

os.chdir(path) # set working directory

del path

# Create a list with all file names

extension = 'csv'

FileNames = glob.glob('*.{}'.format(extension))

FileNames = [x[:-12] for x in FileNames]

# Create a list with all final column names

columnsList = ['OLSRSquarredBefore', 'OLSRSquarredAfter', 'EntriesBefore', 'EntriesAfter', \
               'ChowTest2020Coef', 'ChowTest2020Reject', 'ChowTest2020S2Coef', 'ChowTest2020S2Reject', 'ChowTest2020S1Coef', 'ChowTest2020S1Reject', 'ChowTestBaseCoef', 'ChowTestBaseReject', \
                   '2019S1Coef', '2019S1Reject', '2019S2Coef', '2019S2Reject', '2020S1Coef', '2020S1Reject', '2020S2Coef', '2020S2Reject', \
                      'Before2020Coef', 'Before2020Reject', 'After2020Coef', 'After2020Reject', \
                          'Est2017MinusReal2018', 'Est2018MinusReal2019', 'Est2019MinusReal2020', 'Est2019MinusReal2020S1', 'Est2019MinusReal2020S2', \
                              'Average2017', 'Average2018', 'Average2019', 'Average2020', 'Average2017S1', 'Average2018S1', 'Average2019S1', 'Average2020S1', 'Average2017S2', 'Average2018S2', 'Average2019S2', 'Average2020S2', \
                                  'Average2017Q1', 'Average2018Q1', 'Average2019Q1', 'Average2020Q1', 'Average2017Q2', 'Average2018Q2', 'Average2019Q2', 'Average2020Q2', 'Average2017Q3', 'Average2018Q3', 'Average2019Q3', 'Average2020Q3',\
                                      'Average2017Q4', 'Average2018Q4', 'Average2019Q4', 'Average2020Q4']
    
# Create a new ampty dataframe to be filled with the analysis results

comparison = pd.DataFrame(index = FileNames, columns = columnsList)


# importing number of entries amount

path = 'C:/Users/phili/OneDrive/Documents/CarThesisNew/Data/CleanedAuto/NewMostSoldincl2017/AnalysisChowTestResults'

os.chdir(path) # set working directory

del path

dfNbEntries = pd.read_csv('NumberOfEntries.csv').set_index('Unnamed: 0')


# For each vehicle results file, find the right value and add it in the right place
# in the final comparison dataframe:
for vhc in FileNames:
    
    path = 'C:/Users/phili/OneDrive/Documents/CarThesisNew/Data/CleanedAuto/NewMostSoldincl2017/AnalysisChowTestResults'

    os.chdir(path) # set working directory

    del path
    
    ## Importing vehicule data for 
    
    df = pd.read_csv('WithDeletedEngines/{}Analysis.csv'.format(vhc)).set_index('Unnamed: 0')
    
    ## Importing vehicule data OLSRSquarredBefore # was needed to check if the deletion of 
    ## not significant engine types inproved the R squarred, it did
    
    # dfBefore = pd.read_csv('WithEngineBetas/{}Analysis.csv'.format(vhc)).set_index('Unnamed: 0')
    
    
    ## R squarred
    
    comparison.loc[vhc, 'OLSRSquarredAfter'] = df.loc['BaseIntercept', 'R_Squarred']
    
    # comparison.loc[vhc, 'OLSRSquarredBefore'] = dfBefore.loc['BaseIntercept', 'R_Squarred']
    
    
    ## Number of entries (difference between before analysis.py and after)
    
    comparison.loc[vhc, 'EntriesBefore'] = dfNbEntries.loc[vhc, 'StartAmount']
    
    comparison.loc[vhc, 'EntriesAfter'] = dfNbEntries.loc[vhc, 'EndAmount']


    ## Chow Test Coefs & Rejects
    
    # 1:
    
    comparison.loc[vhc, 'ChowTest2020Coef'] = df.loc['chowTest2020(1)', 'Test/Coef']
    
    comparison.loc[vhc, 'ChowTest2020Reject'] = df.loc['chowTest2020(1)', 'RejectEquality']
    
    # 2:
    
    comparison.loc[vhc, 'ChowTest2020S2Coef'] = df.loc['chowTest20S2(2)', 'Test/Coef']
    
    comparison.loc[vhc, 'ChowTest2020S2Reject'] = df.loc['chowTest20S2(2)', 'RejectEquality']
    
    # 3:
    
    comparison.loc[vhc, 'ChowTest2020S1Coef'] = df.loc['chowTest2020S1S2(3)', 'Test/Coef']
    
    comparison.loc[vhc, 'ChowTest2020S1Reject'] = df.loc['chowTest2020S1S2(3)', 'RejectEquality']
    
    # 4:
    
    comparison.loc[vhc, 'ChowTestBaseCoef'] = df.loc['chowTestBase(4)', 'Test/Coef']
    
    comparison.loc[vhc, 'ChowTestBaseReject'] = df.loc['chowTestBase(4)', 'RejectEquality']
    
    
    ## Regression coefficients Semestrial
    
    # 2019S1
    
    comparison.loc[vhc, '2019S1Coef'] = df.loc['SS12019', 'Test/Coef']
    
    comparison.loc[vhc, '2019S1Reject'] = df.loc['SS12019', 'RejectEquality']
    
    # 2019S2
    
    comparison.loc[vhc, '2019S2Coef'] = df.loc['SS22019', 'Test/Coef']
    
    comparison.loc[vhc, '2019S2Reject'] = df.loc['SS22019', 'RejectEquality']
    
    # 2020S1
    
    comparison.loc[vhc, '2020S1Coef'] = df.loc['SS12020', 'Test/Coef']
    
    comparison.loc[vhc, '2020S1Reject'] = df.loc['SS12020', 'RejectEquality']
    
    # 2020S2
    
    comparison.loc[vhc, '2020S2Coef'] = df.loc['SS22020', 'Test/Coef']
    
    comparison.loc[vhc, '2020S2Reject'] = df.loc['SS22020', 'RejectEquality']
    
    
    ## Regression coefficients Annual
    
    # Before 2020
    
    comparison.loc[vhc, 'Before2020Coef'] = df.loc['Abefore2020', 'Test/Coef']
    
    comparison.loc[vhc, 'Before2020Reject'] = df.loc['Abefore2020', 'RejectEquality']
    
    # After 2020
    
    comparison.loc[vhc, 'After2020Coef'] = df.loc['Aafter2020', 'Test/Coef']
    
    comparison.loc[vhc, 'After2020Reject'] = df.loc['Aafter2020', 'RejectEquality']
    
    
    ## Estimates Minus Real Values
    
    # 2017 vs 2018
    
    comparison.loc[vhc, 'Est2017MinusReal2018'] = df.loc['Est2017_Minus_Real2018', 'Test/Coef']
    
    # 2018 vs 2019
    
    comparison.loc[vhc, 'Est2018MinusReal2019'] = df.loc['Est2018_Minus_Real2019', 'Test/Coef']
    
    # 2019 vs 2020
    
    comparison.loc[vhc, 'Est2019MinusReal2020'] = df.loc['Est2019_Minus_Real2020', 'Test/Coef']
    
    # 2019 vs 2020S1
    
    comparison.loc[vhc, 'Est2019MinusReal2020S1'] = df.loc['Est2019_Minus_Real2020S1', 'Test/Coef']
    
    # 2019 vs 2020S2
    
    comparison.loc[vhc, 'Est2019MinusReal2020S2'] = df.loc['Est2019_Minus_Real2020S2', 'Test/Coef']
    
    
    ## Averages
    
    AverageList = ['Average2017', 'Average2018', 'Average2019', 'Average2020', 'Average2017S1', 'Average2018S1', 'Average2019S1', 'Average2020S1', 'Average2017S2', 'Average2018S2', 'Average2019S2', 'Average2020S2', \
                     'Average2017Q1', 'Average2018Q1', 'Average2019Q1', 'Average2020Q1', 'Average2017Q2', 'Average2018Q2', 'Average2019Q2', 'Average2020Q2', 'Average2017Q3', 'Average2018Q3', 'Average2019Q3', 'Average2020Q3',\
                         'Average2017Q4', 'Average2018Q4', 'Average2019Q4', 'Average2020Q4']
        
    for Average in AverageList:
        
        comparison.loc[vhc, Average] = df.loc[Average, 'Test/Coef']
    
    
    
# Select the path to save the comparison table and save it as a new csv file

path = 'C:/Users/phili/OneDrive/Documents/CarThesisNew/Data/CleanedAuto/NewMostSoldincl2017/AnalysisChowTestResults'

os.chdir(path) # set working directory

del path
        
comparison.to_csv('vhcsResultsConsolidated.csv')
