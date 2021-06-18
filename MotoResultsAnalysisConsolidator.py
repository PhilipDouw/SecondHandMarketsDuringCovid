# =============================================================================
# Takes all selected vehicles results and consolidates them into a single file
# =============================================================================

# Used Libraries

import os
import glob
import pandas as pd

# Selecting Path

path = 'C:/Users/phili/OneDrive/Documents/CarThesisNew/Moto/NewMostSold/AnalysisIncl2017'

os.chdir(path) # set working directory

del path

# Creating list of selected file names

extension = 'csv'

FileNames = glob.glob('*.{}'.format(extension))

FileNames = [x[:-12] for x in FileNames]

# Creating list for column labeling

columnsList = ['OLSRSquarred', \
               'ChowTest2020Coef', 'ChowTest2020Reject', 'ChowTest2020S2Coef', 'ChowTest2020S2Reject', 'ChowTest2020S1S2Coef', 'ChowTest2020S1S2Reject', 'ChowTestBaseCoef', 'ChowTestBaseReject', \
                   '2019S1Coef', '2019S1Reject', '2019S2Coef', '2019S2Reject', '2020S1Coef', '2020S1Reject', '2020S2Coef', '2020S2Reject', \
                      'Before2020Coef', 'Before2020Reject', 'After2020Coef', 'After2020Reject', \
                          'Est2017MinusReal2018', 'Est2018MinusReal2019', 'Est2019MinusReal2020', 'Est2019MinusReal2020S1', 'Est2019MinusReal2020S2', \
                              'Average2017', 'Average2018', 'Average2019', 'Average2020', 'Average2017S1', 'Average2018S1', 'Average2019S1', 'Average2020S1', 'Average2017S2', 'Average2018S2', 'Average2019S2', 'Average2020S2', \
                                  'Average2017Q1', 'Average2018Q1', 'Average2019Q1', 'Average2020Q1', 'Average2017Q2', 'Average2018Q2', 'Average2019Q2', 'Average2020Q2', 'Average2017Q3', 'Average2018Q3', 'Average2019Q3', 'Average2020Q3',\
                                      'Average2017Q4', 'Average2018Q4', 'Average2019Q4', 'Average2020Q4' ,\
                                                          'BaseIntercept', 'BaseKm', 'BaseVhcAge', 'BaseQ1', 'BaseQ2', 'BaseQ3', 'BaseQ4', \
                                                              'before2020Intercept', 'before2020Km', 'before2020VhcAge', 'before2020Q1', 'before2020Q2', 'before2020Q3', 'before2020Q4', \
                                                                  '2019Intercept', '2019Km', '2019VhcAge', '2019Q1', '2019Q2', '2019Q3', '2019Q4']
    
# Creating pandas dataframe for consolidated results

comparison = pd.DataFrame(index = FileNames, columns = columnsList)


# Looping trough all vehicles resultst files and adding the results
# to the consolidated results dataframe

for vhc in FileNames:
    
    
    ## Importing vehicule data for 
    
    df = pd.read_csv('{}Analysis.csv'.format(vhc)).set_index('Unnamed: 0')
    
    
    ## R squarred
    
    comparison.loc[vhc, 'OLSRSquarred'] = df.loc['BaseIntercept', 'R_Squarred']
    

    ## Chow Test Coefs & Rejects
    
    # 2020
    
    comparison.loc[vhc, 'ChowTest2020Coef'] = df.loc['chowTest2020(1)', 'Test/Coef']
    
    comparison.loc[vhc, 'ChowTest2020Reject'] = df.loc['chowTest2020(1)', 'RejectEquality']
    
    # 2020S2
    
    comparison.loc[vhc, 'ChowTest2020S2Coef'] = df.loc['chowTest20S2(2)', 'Test/Coef']
    
    comparison.loc[vhc, 'ChowTest2020S2Reject'] = df.loc['chowTest20S2(2)', 'RejectEquality']
    
    # 2020S1S2
    
    comparison.loc[vhc, 'ChowTest2020S1S2Coef'] = df.loc['chowTest2020S1S2(3)', 'Test/Coef']
    
    comparison.loc[vhc, 'ChowTest2020S1S2Reject'] = df.loc['chowTest2020S1S2(3)', 'RejectEquality']
    
    # Base
    
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
    
    
    ## Averages (averages have the same name in the consolidated and individual
    ## files, so we can simply loop through the names)
    
    AverageList = ['Average2017', 'Average2018', 'Average2019', 'Average2020', 'Average2017S1', 'Average2018S1', 'Average2019S1', 'Average2020S1', 'Average2017S2', 'Average2018S2', 'Average2019S2', 'Average2020S2', \
                                  'Average2017Q1', 'Average2018Q1', 'Average2019Q1', 'Average2020Q1', 'Average2017Q2', 'Average2018Q2', 'Average2019Q2', 'Average2020Q2', 'Average2017Q3', 'Average2018Q3', 'Average2019Q3', 'Average2020Q3',\
                                      'Average2017Q4', 'Average2018Q4', 'Average2019Q4', 'Average2020Q4']
    
    for Average in AverageList:
        
        comparison.loc[vhc, Average] = df.loc[Average, 'Test/Coef']
        
    
    CoefficientsList = ['BaseIntercept', 'BaseKm', 'BaseVhcAge', 'BaseQ1', 'BaseQ2', 'BaseQ3', 'BaseQ4', 'before2020Intercept', 'before2020Km', 'before2020VhcAge', 'before2020Q1', 'before2020Q2', 'before2020Q3', 'before2020Q4', '2019Intercept', '2019Km', '2019VhcAge', '2019Q1', '2019Q2', '2019Q3', '2019Q4']
  
    for Coef in CoefficientsList:
        
        comparison.loc[vhc, Coef] = df.loc[Coef, 'Test/Coef']
    

# Selecting path of where to save the consolidated file

path = 'C:/Users/phili/OneDrive/Documents/CarThesisNew/Moto'

os.chdir(path) # set working directory

del path

# Saving the consolidated dataframe as a csv file
        
comparison.to_csv('MotosResultsConsolidatedWithCoefs.csv')
