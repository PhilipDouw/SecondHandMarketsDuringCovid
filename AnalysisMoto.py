# =============================================================================
# Analysis code: takes a vehicles entries and
# - Cleans it further
# - performs several tests
# - Saves it as a new file
# =============================================================================


# Used libraries

import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn import linear_model
import sys
import math
from chow_test import chowtest
import numpy as np

## functions

# OLS base regression

def OLS(df):

    # create the regression equation
    f_rev = 'LogPrice~Km+VhcAge+Q1+Q2+Q3+Q4'
    
    # use the statmodels library to perform the ols regression as save the 
    # result as a variable
    model_rev = smf.ols(formula=f_rev, data=df).fit()
    
    # save the output as a variable that can be called using the commented
    # function at the end of the function
    print_model = model_rev.summary()
    
    # save the parameters as a variable that can be called using the commented
    # function at the end of the function
    print_param = model_rev.params
    
    # Save the r squared as a variable (finally used a separate function to 
    # save the time rewriting a large part of the script)
    r_squared = model_rev.rsquared
    r = pd.Series(r_squared, index = ['r_squared'])
    # print(print_model) to get summary of the regression
    # print(print_param)
    
    # Return the variable that includes the whole regression
    return model_rev

# OLS regression with two aditional dummy variables
# for comments, see the function above

def OLSwith2020separation(df):
    
    f_rev = 'LogPrice~Km+VhcAge+Q1+Q2+Q3+Q4+before2020+after2020'
    model_rev = smf.ols(formula=f_rev, data=df).fit()
    print_model = model_rev.summary()
    print_param = model_rev.params
    r_squared = model_rev.rsquared
    r = pd.Series(r_squared, index = ['r_squared'])
    # print(print_model)
    
    return model_rev

# OLS Regression with four addtionional dummy variables

def OLSwith2020S1S2separation(df):
    
    df['S12019'] = 0
    df['S22019'] = 0
    
    for i in range(len(df)):
        if (df.loc[i, 'CurrentYear'] == 2019) & (df.loc[i, 'S1'] == 1):
            df.loc[i,'S12019'] = 1
        elif (df.loc[i, 'CurrentYear'] == 2019) & (df.loc[i, 'S2'] == 1):
            df.loc[i,'S22019'] = 1
    
    f_rev = 'LogPrice~Km+VhcAge+Q1+Q2+Q3+Q4+S12019+S22019+S12020+S22020'
    model_rev = smf.ols(formula=f_rev, data=df).fit()
    print_model = model_rev.summary()
    print_param = model_rev.params
    r_squared = model_rev.rsquared
    r = pd.Series(r_squared, index = ['r_squared'])
    # print(print_model)

    return model_rev

# OLS base Regression that only outputs the r squared
# could have done this in the upper mentioned functions, but it would have
# led to many changes later on, easier this way, however a better way exists to
# do this for example simply writing model_rev.rsquared in the analysis function

def OLSR(df):

    f_rev = 'LogPrice~Km+VhcAge+Q1+Q2+Q3+Q4'
    model_rev = smf.ols(formula=f_rev, data=df).fit()
    print_model = model_rev.summary()
    print_param = model_rev.params
    r_squared = model_rev.rsquared
    r = pd.Series(r_squared, index = ['r_squared'])
    # print(print_model)
    
    
    # output = pd.concat([r, print_param]).rename('OLS')
    # print(print_model)
    # print(print_param)
    return r

# OLS Regression with two addtionional dummy variables, R squarred

def OLSwith2020separationR(df):
    
    f_rev = 'LogPrice~Km+VhcAge+Q1+Q2+Q3+Q4+before2020+after2020'
    model_rev = smf.ols(formula=f_rev, data=df).fit()
    print_model = model_rev.summary()
    print_param = model_rev.params
    r_squared = model_rev.rsquared
    r = pd.Series(r_squared, index = ['r_squared'])
    # print(print_model)
    
    
    # output = pd.concat([r, print_param]).rename('OLS')
    # print(print_model)
    # print(print_param)
    return r

# OLS Regression with four addtionional dummy variables, R squarred

def OLSwith2020S1S2separationR(df):
    
    df['S12019'] = 0
    df['S22019'] = 0
    
    for i in range(len(df)):
        if (df.loc[i, 'CurrentYear'] == 2019) & (df.loc[i, 'S1'] == 1):
            df.loc[i,'S12019'] = 1
        elif (df.loc[i, 'CurrentYear'] == 2019) & (df.loc[i, 'S2'] == 1):
            df.loc[i,'S22019'] = 1
    
    f_rev = 'LogPrice~Km+VhcAge+Q1+Q2+Q3+Q4+S12019+S22019+S12020+S22020'
    model_rev = smf.ols(formula=f_rev, data=df).fit()
    print_model = model_rev.summary()
    print_param = model_rev.params
    r_squared = model_rev.rsquared
    r = pd.Series(r_squared, index = ['r_squared'])
    # print(print_model)
    
    
    # output = pd.concat([r, print_param]).rename('OLS')
    # print(print_model)
    # print(print_param)
    return r

# Chow tests using the chowTest library

def Chow(df):
    
    # use the logprice column as our "y/dependent" variable
    
    y = df[['LogPrice']].copy()
    
    # select the independent variables
    
    BaseVariables = ['Km', 'VhcAge', 'Q1', 'Q2', 'Q3', 'Q4'] 
    
    X = df[BaseVariables].copy()
    
    # Select a significance level (the function taken from the ChowTest library
    # needs this as input, however this is a bit obselet, since the test
    # will output the P-Value, which we can use to determine at which significance
    # level the test will reject the equality hypothesis)
    
    significance_level = 0.1
    
    # Create an empty list to store the chow test results
    
    ChowList = []

    # Perfrom four individual chow tests
    
    # 1.    separate the main datasets into two parts, the first with data until the 
    # end of 2019 and the second one with the data after 2020
    
    first_index_in_model_S12020 = df[df.CurrentYear == 2020].first_valid_index()
    
    last_index_in_model_2019 = first_index_in_model_S12020 -1
    
    ChowList.append(chowtest(X, y, last_index_in_model_2019, first_index_in_model_S12020, significance_level))
    
    # 2.    data until the end of the first semester of 2020 and data within the second semester of 2020
    
    first_index_in_model_S22020 = df[(df.CurrentYear == 2020) & (df.CurrentMonth == 6)].first_valid_index()
    
    last_index_in_model_2020S1 = first_index_in_model_S22020 -1
    
    ChowList.append(chowtest(X, y, last_index_in_model_2020S1, first_index_in_model_S22020, significance_level))
    
    # 3.	We will only take data within 2020 and separate it between the first and second semester
    
    df20192020S1 = df[df['S22020'] == 0]
    
    first_index_in_model_20192020S1 = df20192020S1[(df20192020S1.CurrentYear == 2020)].first_valid_index()
    
    last_index_in_model_20192020S1 = first_index_in_model_20192020S1 -1
    
    y3 = df20192020S1[['LogPrice']].copy()
    
    BaseVariables3 = ['Km', 'VhcAge', 'Q1', 'Q2', 'Q3', 'Q4'] 
    
    X3 = df20192020S1[BaseVariables3].copy()
    
    ChowList.append(chowtest(X3, y3, last_index_in_model_20192020S1, first_index_in_model_20192020S1, significance_level))
    
    # 4.	We will only take data until the end of 2019 and separate the datasets between the years 2018 and 2019
    
    df1819 = df[df['CurrentYear'] <= 2019]
    
    first_index_in_model_2019 = df1819[(df1819.CurrentYear == 2019)].first_valid_index()
    
    last_index_in_model_2018 = first_index_in_model_2019 -1
    
    y4 = df1819[['LogPrice']].copy()
    
    BaseVariables4 = ['Km', 'VhcAge', 'Q1', 'Q2', 'Q3', 'Q4'] 
    
    X4 = df1819[BaseVariables4].copy()
    
    ChowList.append(chowtest(X4, y4, last_index_in_model_2018, first_index_in_model_2019, significance_level))
    
    # Return our chowtest results list
  
    return ChowList


# Estimates the price a vehicle would have had in 2017 using the data of 2018

def LogPriceEstimatorEstimatedFrom2017MinusReal2018(df):
    
    # Generate the parameters of the year we want to estimate the prices of 
    params2017 = OLS(df[df['CurrentYear'] == 2017]).params
    
    # Select the entries that are of the next year
    df2018 = df[df['CurrentYear'] == 2018]
    
    # reset the index to make sure we do not have holes in the dataset
    df2018.reset_index(inplace=True)
    del df2018['index']
    
    # Create empty list to store the estimated prices
    estimatedLogPrice = [None] * len(df2018)
    
    # for each entry, estimate the price the vehicule would have had in 2017
    # using the parameters of 2017 and the data of 2018
    for i in range(len(df2018)):
    
        estimatedLogPrice[i] = params2017.Intercept + params2017.Km * df2018.loc[i, 'Km'] + \
            params2017.VhcAge * df2018.loc[i, 'VhcAge'] + \
                params2017.Q1 * df2018.loc[i, 'Q1'] + \
                    params2017.Q2 * df2018.loc[i, 'Q2'] + \
                        params2017.Q3 * df2018.loc[i, 'Q3'] + \
                            params2017.Q4 * df2018.loc[i, 'Q4']
    
    # Create a list of the actual prices of 2018
    RealLogPrice = [None] * len(df2018)
                            
    for i in range(len(df2018)):
        
        RealLogPrice[i] = df2018.loc[i, 'LogPrice']
        
    # calculate the difference between estimated and real prices
    differences = [None] * len(df2018)
    
    for i in range(len(differences)):
        
        differences[i] = estimatedLogPrice[i] - RealLogPrice[i]
        
    # Sum the differences and save it as a variable to return
        
    EstimatedFrom2017MinusReal2018 = sum(differences)
    
    return EstimatedFrom2017MinusReal2018 
    # if positive -> same vehicule in 2017 would on average have been more expensive (what we would expect)
    # if Negative -> same vehicule in 2017 would on average have been cheaper (not what we would expect)
    
    
# Estimates the price a vehicle would have had in 2019 using the data of 2020
# For comments see the function above
   
def LogPriceEstimatorEstimatedFrom2019MinusReal2020(df):
    
    params2019 = OLS(df[df['CurrentYear'] == 2019]).params
    
    df2020 = df[df['CurrentYear'] == 2020]
    
    df2020.reset_index(inplace=True)
    del df2020['index']
    
    VarIndex2020 = df2020.columns
    
    estimatedLogPrice = [None] * len(df2020)
    
    for i in range(len(df2020)):
        
    
        estimatedLogPrice[i] = params2019.Intercept + params2019.Km * df2020.loc[i, 'Km'] + \
            params2019.VhcAge * df2020.loc[i, 'VhcAge'] + \
                params2019.Q1 * df2020.loc[i, 'Q1'] + \
                    params2019.Q2 * df2020.loc[i, 'Q2'] + \
                        params2019.Q3 * df2020.loc[i, 'Q3'] + \
                            params2019.Q4 * df2020.loc[i, 'Q4']
                                
    RealLogPrice = [None] * len(df2020)
                            
    for i in range(len(df2020)):
        
        RealLogPrice[i] = df2020.loc[i, 'LogPrice']
        
    differences = [None] * len(df2020)
    
    for i in range(len(differences)):
        
        differences[i] = estimatedLogPrice[i] - RealLogPrice[i]
        
    EstimatedFrom2019MinusReal2020 = sum(differences)
    
    return EstimatedFrom2019MinusReal2020 
    # if positive -> same vehicule in 2019 would on average have been more expensive (what we would expect)
    # if Negative -> same vehicule in 2019 would on average have been cheaper (not what we would expect)
    
# Estimates the price a vehicle would have had in 2018 using the data of 2019
# For comments see the function above
    
def LogPriceEstimatorEstimatedFrom2018MinusReal2019(df):
    
    params2018 = OLS(df[df['CurrentYear'] == 2018]).params
    
    df2019 = df[df['CurrentYear'] == 2019]
    
    df2019.reset_index(inplace=True)
    del df2019['index']
    
    VarIndex2020 = df2019.columns
    
    estimatedLogPrice = [None] * len(df2019)
    
    for i in range(len(df2019)):
    
        estimatedLogPrice[i] = params2018.Intercept + params2018.Km * df2019.loc[i, 'Km'] + \
            params2018.VhcAge * df2019.loc[i, 'VhcAge'] + \
                params2018.Q1 * df2019.loc[i, 'Q1'] + \
                    params2018.Q2 * df2019.loc[i, 'Q2'] + \
                        params2018.Q3 * df2019.loc[i, 'Q3'] + \
                            params2018.Q4 * df2019.loc[i, 'Q4']
                                
    RealLogPrice = [None] * len(df2019)
                            
    for i in range(len(df2019)):
        
        RealLogPrice[i] = df2019.loc[i, 'LogPrice']
        
    differences = [None] * len(df2019)
    
    for i in range(len(differences)):
        
        differences[i] = estimatedLogPrice[i] - RealLogPrice[i]
        
    EstimatedFrom2018MinusReal2019 = sum(differences)
    
    return EstimatedFrom2018MinusReal2019 
    # if positive -> same vehicule in 2019 would on average have been more expensive (what we would expect)
    # if Negative -> same vehicule in 2019 would on average have been cheaper (not what we would expect)
    

# Estimates the price a vehicle would have had in 2019 using the data of S1 2020
# For comments see the function above
    
def LogPriceEstimatorEstimatedFrom2019MinusReal2020FirstSemester(df):
    
    params2019 = OLS(df[df['CurrentYear'] == 2019]).params
    
    mask = (df['S12020'] == 1)
    
    df2020S1 = df.loc[mask]
    
    df2020S1.reset_index(inplace=True)
    del df2020S1['index']
    
    VarIndex2020 = df2020S1.columns
    
    estimatedLogPrice = [None] * len(df2020S1)
    
    for i in range(len(df2020S1)):

        estimatedLogPrice[i] = params2019.Intercept + params2019.Km * df2020S1.loc[i, 'Km'] + \
            params2019.VhcAge * df2020S1.loc[i, 'VhcAge'] + \
                params2019.Q1 * df2020S1.loc[i, 'Q1'] + \
                    params2019.Q2 * df2020S1.loc[i, 'Q2'] + \
                        params2019.Q3 * df2020S1.loc[i, 'Q3'] + \
                            params2019.Q4 * df2020S1.loc[i, 'Q4']
                                
    RealLogPrice = [None] * len(df2020S1)
                            
    for i in range(len(df2020S1)):
        
        RealLogPrice[i] = df2020S1.loc[i, 'LogPrice']
        
    differences = [None] * len(df2020S1)
    
    for i in range(len(differences)):
        
        differences[i] = estimatedLogPrice[i] - RealLogPrice[i]
        
    EstimatedFrom2019MinusReal2020 = sum(differences)
    
    return EstimatedFrom2019MinusReal2020 
    # if positive -> same vehicule in 2019 would on average have been more expensive (what we would expect)
    # if Negative -> same vehicule in 2019 would on average have been cheaper (not what we would expect)
    
    
# Estimates the price a vehicle would have had in 2019 using the data of S2 2020
# For comments see the function above

def LogPriceEstimatorEstimatedFrom2019MinusReal2020SecondSemester(df):
    
    params2019 = OLS(df[df['CurrentYear'] == 2019]).params
    
    mask = (df['S22020'] == 1)
    
    df2020S2 = df.loc[mask]
    
    df2020S2.reset_index(inplace=True)
    del df2020S2['index']
    
    VarIndex2020 = df2020S2.columns
    
    estimatedLogPrice = [None] * len(df2020S2)
    
    for i in range(len(df2020S2)):

        estimatedLogPrice[i] = params2019.Intercept + params2019.Km * df2020S2.loc[i, 'Km'] + \
            params2019.VhcAge * df2020S2.loc[i, 'VhcAge'] + \
                params2019.Q1 * df2020S2.loc[i, 'Q1'] + \
                    params2019.Q2 * df2020S2.loc[i, 'Q2'] + \
                        params2019.Q3 * df2020S2.loc[i, 'Q3'] + \
                            params2019.Q4 * df2020S2.loc[i, 'Q4']
                                
    RealLogPrice = [None] * len(df2020S2)
                            
    for i in range(len(df2020S2)):
        
        RealLogPrice[i] = df2020S2.loc[i, 'LogPrice']
        
    differences = [None] * len(df2020S2)
    
    for i in range(len(differences)):
        
        differences[i] = estimatedLogPrice[i] - RealLogPrice[i]
        
    EstimatedFrom2019MinusReal2020 = sum(differences)
    
    return EstimatedFrom2019MinusReal2020 
    # if positive -> same vehicule in 2019 would on average have been more expensive (what we would expect)
    # if Negative -> same vehicule in 2019 would on average have been cheaper (not what we would expect)
    
    
# Function that modifies the data so that it can be used with the different tests:
    # Gets rid of outliers
    # modifies type of data (for example from strings to integers or floats)
    # outputs a "clean" and usable dataframe

def ModelSummary(vhc):
    
    # print the selected vehicle's name    
    print(vhc)

    # Importing dataframe and creating new dataframe with only usefull columns
    # (note when converting a saved csv file back into a dataframe, it will
    # usually create a new first column which we need to get rid of)

    df = pd.read_csv('{}.csv'.format(vhc))
    
    del df['Unnamed: 0'], df['Unnamed: 0.1']
    
    ## Cleaning
    
    # replace all Nan or "error" cells with a "0" and delete entries that now 
    # have this value
    
    df = df.fillna(0)
    
    df = df.drop(df[df.Age == 'k.A.'].index)
    
    df = df.drop(df[df.Color == 0].index)
    
    df = df.drop(df[df.Price == 0].index)
    
    df = df.drop(df[df.Age == 0].index)
    
    df = df.drop(df[df.Km == 0].index)
    
    df = df.drop(df[df.Km == 'error'].index)
    
    # delete all entries that have text as the km value (usually new vehicles)
    
    df['Km'] = df['Km'].astype(str)
    
    df = df.drop(df[df.Km.str.contains(r'[a-zA-Z]')].index)
    
    # do the same for the vehicle's age column
    
    df['Age'] = df['Age'].astype(str)
    
    df['ConstrYear'] = df['Age'].str.split('.').str[-1]
    
    df = df.drop(df[df.ConstrYear.str.contains(r'[a-zA-Z]')].index)
    
    # also delete entries that have a longer value that 5 for the vehicle's
    # construction year
    
    df['name_length'] = df.ConstrYear.str.len()
    
    df = df[df.name_length < 5]
    
    del df['name_length']    
    
    # Keep only the wanted variable columns
    
    df = df[['Price', 'Km', 'ConstrYear', 'Color', 'Date']].copy()
    
    ## Outliers
    
    # Only keep vehicles that have a certain price range and km range
    # note, we do not keep new vehicles, i.e. vehicles with less than 200km
    
    df.Price = df.Price.astype(int)
    
    df = df.drop(df[df.Price >= 300000].index)
    
    df = df.drop(df[df.Price <= 1000].index)
    
    df.Km = df.Km.astype(float)
    
    df.Km = df.Km.astype(int)
    
    df = df.drop(df[df.Km >= 100000].index)
    
    df = df.drop(df[df.Km <= 200].index)
    
    # convert the construction year to numeric and clean the value
    # for example if the year was 2010, it sometimes outputs it as 201, which
    # we need to change
    
    df['ConstrYear'] = pd.to_numeric(df['ConstrYear'])
    
    # Specifics manipulations for specific models
    df.reset_index(inplace=True)
    del df['index']
    
    for i in range(len(df['ConstrYear'])):
        
        if df.iloc[i,2] == 201:
            
            df.iloc[i,2] = 2010
            
        elif df.iloc[i,2] == 202:
            
            df.iloc[i,2] == 2020
            
        elif len(str(df.iloc[i,2])) > 4:
            
            df.iloc[i,2] = int(str(df.iloc[i,2])[0:4])
            
        else:
            
            pass
        
    # Delete all vehicles that were built before 1950 or after 2020
    
    df = df.drop(df[df.ConstrYear < 1950].index)
    
    df = df.drop(df[df.ConstrYear > 2020].index)
        
    # Need to transform age to lower values (1 year = 1 year old), by substracting
    # the year of the upload with the year of construction
    
    df['CurrentYear'] = df['Date'].str.split('.').str[-1]
    
    df['CurrentYear'] = pd.to_numeric(df['CurrentYear'])
    
    df['CurrentMonth'] = df['Date'].str.split('.').str[-2]
    
    df['CurrentMonth'] = pd.to_numeric(df['CurrentMonth'])
    
    # delete all vehicles that were "constructed after being sold"
    
    df = df.drop(df[df.ConstrYear > df.CurrentYear].index)
    
    df = df.drop(df[df.CurrentYear > 2020].index)
    
    df['VhcAge'] = df['CurrentYear'] - df['ConstrYear']
    
    ## Seasonality
    
    # Create dummy variables for each quarter and semester
    
    df.reset_index(inplace=True)
    del df['index']
    
    Q1 = [1,2,3]
    Q2 = [4,5,6]
    Q3 = [7,8,9]
    Q4 = [10,11,12]
    
    df['Q1'] = 0
    df['Q2'] = 0
    df['Q3'] = 0
    df['Q4'] = 0
    
    for i in range(len(df)):
        if df.iloc[i, 6] in Q1:
            df.iloc[i, 8] = 1
        elif df.iloc[i, 6] in Q2:
            df.iloc[i, 9] = 1
        elif df.iloc[i, 6] in Q3:
            df.iloc[i, 10] = 1
        elif df.iloc[i, 6] in Q4:
            df.iloc[i, 11] = 1
            
    S1 = [1,2,3,4,5,6]
    S2 = [7,8,9,10,11,12]
    
    df['S1'] = 0
    df['S2'] = 0
    
    for i in range(len(df)):
        if df.iloc[i, 6] in S1:
            df.iloc[i, 12] = 1
        elif df.iloc[i, 6] in S2:
            df.iloc[i, 13] = 1
            
    
    # Reset the index since we deleted some entries and the index keeps its
    # original value
    
    df.reset_index(inplace=True)
    del df['index']
    
    # Create dummy variables for whether the vehicle was uploaded before
    # or after 2020
    
    df.loc[:,'before2020'] = 0
    df.loc[:,'after2020'] = 0
    
    for i in range(len(df)):
        if df.loc[i,'CurrentYear'] >= 2020:
            df.loc[i, 'after2020'] = 1
        elif df.loc[i,'CurrentYear'] < 2020:
            df.loc[i,'before2020'] = 1
            
    # Create dummy variable for whether the vehicle was uploaded during
    # the first or second semester of 2020
            
    df['S12020'] = 0
    df['S22020'] = 0
    
    for i in range(len(df)):
        if (df.loc[i, 'CurrentYear'] == 2020) & (df.loc[i, 'S1'] == 1):
            df.loc[i,'S12020'] = 1
        elif (df.loc[i, 'CurrentYear'] == 2020) & (df.loc[i, 'S2'] == 1):
            df.loc[i,'S22020'] = 1
            
    # Create a new column which shows the Log(Price)            
    df['LogPrice'] = np.log(df['Price'])
    
    
    # Return the modified dataframe
    return df

'''

## Might still be usefull for later use

# simpler function to estimate the price but which needs the parameters of the
# regression as input

def PriceEstimator(params, Km, VhcAge, Q1, Q2, Q3, Q4):

    estimatedPrice = params[0] + Km*params[1] + VhcAge*params[2] + Q1*params[3] + Q2*params[4] + Q3*params[4] + Q4*params[5]''''''
    
    return estimatedPrice

# Funtion that calculates the Theil inequality coefficient

def TheilInequalityCoeff(params, df): #file:///C:/Users/phili/Downloads/4Hypothesistestinginthemultipleregressionmodel%20(2).pdf
    
    estimates = []
    
    observations = []
    
    differences = []
    
    differencesSquared = []
    
    denom1 = []
    
    denom2 = []

    for n in range(len(df)):
        
        data = df.iloc[n]
        
        Km = data.loc['Km']
        VhcAge = data.loc['VhcAge']
        Q1 = data.loc['Q1']
        Q2 = data.loc['Q2']
        Q3 = data.loc['Q3']
        Q4 = data.loc['Q4']
        
        estimate = PriceEstimator(params, Km, VhcAge, Q1, Q2, Q3, Q4)
        
        estimates.append(estimate)
    
        realValue = data['Price']
        
        observations.append(realValue)
        
        differences.append(abs(estimate - realValue))
        
        differencesSquared.append((estimate - realValue) ** 2)
        
        denom1.append(estimate ** 2)
        
        denom2.append(abs(float(realValue ** 2)))
    
        
    nominator = math.sqrt(sum(differencesSquared))/len(df)
    
    denominator = math.sqrt(sum(denom1)/len(df)) + math.sqrt(sum(denom2)/len(df))
    
    U = nominator/denominator
    
    return U
'''

# function that takes a vehicle name as input and calculates all the above
# created functions

def Analysis(vhc):

    
    # Cleaning the dataframe and getting rid of outliers
    df = ModelSummary(vhc)
    
    # Calculate the parameters of the OLS base regression using data of 2020
    params = OLS(df[df['after2020'] == 0]).params
    
    fit = OLS(df)
    
    OLSbase = list(zip(fit.params, fit.pvalues))
    
    r = OLSR(df)
    
    
    # same as above but with data before 2020
    
    fitbefore2020 = OLS(df[df['after2020'] == 0])
    
    OLSbefore2020 = list(zip(fitbefore2020.params, fitbefore2020.pvalues))
    
    rbefore2020 = OLSR(df[df['after2020'] == 0])
    
    
    # Same as above with data of 2019    
    
    fit2019 = OLS(df[df['CurrentYear'] == 2019])
    
    OLS2019 = list(zip(fit2019.params, fit2019.pvalues))
    
    r2019 = OLSR(df[df['CurrentYear'] == 2019])
    
    
    # Calculate the parameters of the second OLS regression
    
    fit1 = OLSwith2020S1S2separation(df)
    
    OLSsemesterSeparation = list(zip(fit1.params, fit1.pvalues))
    
    r1 = OLSwith2020S1S2separationR(df)
    
    
    # Calculate the parameters of the third OLS regression
    
    fit2 = OLSwith2020separation(df)
    
    OLSannualSeparation = list(zip(fit2.params, fit2.pvalues))
    
    r2 = OLSwith2020separationR(df)
    
    
    # perform the chow tests using data from 2017 to 2020
    
    mask = (df['CurrentYear'] >= 2017) & (df['CurrentYear'] < 2021)
    
    dfChow = df.loc[mask]
    
    ChowList18 = Chow(dfChow)
    
  
    # What if the vehicule was sold during a previous year
    
    IndexEstimatedFrom2019Minus = ['Est2017_Minus_Real2018', 'Est2018_Minus_Real2019', 'Est2019_Minus_Real2020', 'Est2019_Minus_Real2020S1', 'Est2019_Minus_Real2020S2']

    dfEstimates = pd.DataFrame(index = IndexEstimatedFrom2019Minus, columns = ['Test/Coef', 'P-Value', 'RejectEquality'])
    
    dfEstimates.loc['Est2017_Minus_Real2018', 'Test/Coef'] = LogPriceEstimatorEstimatedFrom2017MinusReal2018(df)   

    dfEstimates.loc['Est2018_Minus_Real2019', 'Test/Coef'] = LogPriceEstimatorEstimatedFrom2018MinusReal2019(df)

    dfEstimates.loc['Est2019_Minus_Real2020', 'Test/Coef'] = LogPriceEstimatorEstimatedFrom2019MinusReal2020(df)
    
    dfEstimates.loc['Est2019_Minus_Real2020S1', 'Test/Coef'] = LogPriceEstimatorEstimatedFrom2019MinusReal2020FirstSemester(df)
    
    dfEstimates.loc['Est2019_Minus_Real2020S2', 'Test/Coef'] = LogPriceEstimatorEstimatedFrom2019MinusReal2020SecondSemester(df)
    
    
    # Calculate the Average Prices yearly, semestrially and quarterly
    
    IndexAverages = ['Average2017', 'Average2018', 'Average2019', 'Average2020', 'Average2017S1', 'Average2018S1', 'Average2019S1', 'Average2020S1', 'Average2017S2', 'Average2018S2', 'Average2019S2', 'Average2020S2', \
                     'Average2017Q1', 'Average2018Q1', 'Average2019Q1', 'Average2020Q1', 'Average2017Q2', 'Average2018Q2', 'Average2019Q2', 'Average2020Q2', 'Average2017Q3', 'Average2018Q3', 'Average2019Q3', 'Average2020Q3',\
                         'Average2017Q4', 'Average2018Q4', 'Average2019Q4', 'Average2020Q4']
        
    dfAverages = pd.DataFrame(index = IndexAverages, columns = ['Test/Coef', 'P-Value', 'RejectEquality'])
    
    dfAverages.loc['Average2017', 'Test/Coef'] = df[df['CurrentYear'] == 2017]['Price'].mean()
    
    dfAverages.loc['Average2018', 'Test/Coef'] = df[df['CurrentYear'] == 2018]['Price'].mean()
    
    dfAverages.loc['Average2019', 'Test/Coef'] = df[df['CurrentYear'] == 2019]['Price'].mean()
    
    dfAverages.loc['Average2020', 'Test/Coef'] = df[df['CurrentYear'] == 2020]['Price'].mean()
    
    dfAverages.loc['Average2017S1', 'Test/Coef'] = df[(df['CurrentYear'] == 2017) & (df['S1'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2018S1', 'Test/Coef'] = df[(df['CurrentYear'] == 2018) & (df['S1'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2019S1', 'Test/Coef'] = df[(df['CurrentYear'] == 2019) & (df['S1'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2020S1', 'Test/Coef'] = df[df['S12020'] == 1]['Price'].mean()
    
    dfAverages.loc['Average2017S2', 'Test/Coef'] = df[(df['CurrentYear'] == 2017) & (df['S2'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2018S2', 'Test/Coef'] = df[(df['CurrentYear'] == 2018) & (df['S2'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2019S2', 'Test/Coef'] = df[(df['CurrentYear'] == 2019) & (df['S2'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2020S2', 'Test/Coef'] = df[df['S22020'] == 1]['Price'].mean()
    
    dfAverages.loc['Average2017Q1', 'Test/Coef'] = df[(df['CurrentYear'] == 2017) & (df['Q1'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2018Q1', 'Test/Coef'] = df[(df['CurrentYear'] == 2018) & (df['Q1'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2019Q1', 'Test/Coef'] = df[(df['CurrentYear'] == 2019) & (df['Q1'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2020Q1', 'Test/Coef'] = df[(df['CurrentYear'] == 2020) & (df['Q1'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2017Q2', 'Test/Coef'] = df[(df['CurrentYear'] == 2017) & (df['Q2'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2018Q2', 'Test/Coef'] = df[(df['CurrentYear'] == 2018) & (df['Q2'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2019Q2', 'Test/Coef'] = df[(df['CurrentYear'] == 2019) & (df['Q2'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2020Q2', 'Test/Coef'] = df[(df['CurrentYear'] == 2020) & (df['Q2'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2017Q3', 'Test/Coef'] = df[(df['CurrentYear'] == 2017) & (df['Q3'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2018Q3', 'Test/Coef'] = df[(df['CurrentYear'] == 2018) & (df['Q3'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2019Q3', 'Test/Coef'] = df[(df['CurrentYear'] == 2019) & (df['Q3'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2020Q3', 'Test/Coef'] = df[(df['CurrentYear'] == 2020) & (df['Q3'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2017Q4', 'Test/Coef'] = df[(df['CurrentYear'] == 2017) & (df['Q4'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2018Q4', 'Test/Coef'] = df[(df['CurrentYear'] == 2018) & (df['Q4'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2019Q4', 'Test/Coef'] = df[(df['CurrentYear'] == 2019) & (df['Q4'] == 1)]['Price'].mean()
    
    dfAverages.loc['Average2020Q4', 'Test/Coef'] = df[(df['CurrentYear'] == 2020) & (df['Q4'] == 1)]['Price'].mean()
    
    
    # consolidate all results so that we can output them in a single file
    
    ResultList = ChowList18 + OLSbase + OLSbefore2020 + OLS2019 + OLSsemesterSeparation + OLSannualSeparation
    
    # Generate the indexes for every test/value
    
    IndexChow = ['chowTest2020(1)', 'chowTest20S2(2)', 'chowTest2020S1S2(3)', 'chowTestBase(4)']
    
    IndexFit = fit.params.index.to_list()
    IndexFit = ["Base" + suit for suit in IndexFit]
    
    IndexFitbefore2020 = fitbefore2020.params.index.to_list()
    IndexFitbefore2020 = ["before2020" + suit for suit in IndexFitbefore2020]
    
    IndexFit2019 = fit2019.params.index.to_list()
    IndexFit2019 = ["2019" + suit for suit in IndexFit2019]
    
    IndexFit1 = fit1.params.index.to_list()
    IndexFit1 = ["S" + suit for suit in IndexFit1]
    
    IndexFit2 = fit2.params.index.to_list()
    IndexFit2 = ["A" + suit for suit in IndexFit2]
    
    Index = IndexChow + IndexFit + IndexFitbefore2020 + IndexFit2019 + IndexFit1 + IndexFit2
    
    # Create a new dataframe with the created results and index lists
    
    Results = pd.DataFrame(ResultList, columns=['Test/Coef', 'P-Value'], index = Index)
    
    
    # Add the rejection level for each test (where usefull)
    
    Results['RejectEquality'] = None
    
    for i in range(len(Results)):
        
        if Results.loc[Index[i], 'P-Value'] == None:
            Results.loc[Index[i], 'RejectEquality'] = None
        
        elif Results.loc[Index[i], 'P-Value'] <= 0.01:
            Results.loc[Index[i], 'RejectEquality'] = 'At 1%'
            
        elif Results.loc[Index[i], 'P-Value'] <= 0.05:
            Results.loc[Index[i], 'RejectEquality'] = 'At 5%'
            
        elif Results.loc[Index[i], 'P-Value'] <= 0.1:
            Results.loc[Index[i], 'RejectEquality'] = 'At 10%'
        
        else:
            Results.loc[Index[i], 'RejectEquality'] = 'Not Rejected'
            
    # add the estimates and averages to the final dataframe
            
    Results = pd.concat([Results, dfEstimates, dfAverages])
    
    # add the R squarred where usefull
    
    Results['R_Squarred'] = None
    
    Results.loc['BaseIntercept', 'R_Squarred'] = round(r[0],6)
    Results.loc['SIntercept', 'R_Squarred'] = round(r1[0],6)
    Results.loc['AIntercept', 'R_Squarred'] = round(r2[0],6)
    
    
    # Save the consolidated results for the current vehicle as a new csv file
            
    Results.to_csv('AnalysisIncl2017/{}_Analysis.csv'.format(vhc))


    # return Results # used for mannual validation
    

# Select the path with the vehicle's data csv files
        
path = 'C:/Users/phili/OneDrive/Documents/CarThesisNew/Moto/NewMostSold'

os.chdir(path) # set working directory

del path

# Create a list with all selected vehicle names

extension = 'csv'

FileNames = glob.glob('*.{}'.format(extension))

FileNames = [x[:-4] for x in FileNames]

# Create an empty list that will contain all vehicle names were an error
# occured during one of the different scripts
notGood = []

# For each vehicle in the list, perform the analysis function and either print
# "ok" if everything worked or append in to the notGood list if an error
# occured

for vhc in FileNames:
    
    try:
        
        Analysis(vhc)
        print('{} ok'.format(vhc))
        
    except:
        
        notGood.append(vhc)


    
    
    
    
    



    
    # df.to_csv('parameters_Full_Year_2017_2018_w_seasonality/Parameters_Quarters_{}.csv'.format(FileNames[vhc]))
