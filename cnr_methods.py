import numpy as np 
import pandas as pd 

def get_preprocessed_data():
    x_train = pd.read_csv('X_train.csv')
    x_test = pd.read_csv('X_test.csv')

    x_train['Set'] = 'Train'
    x_test['Set'] = 'Test'
    full_data = pd.concat([x_train,x_test])

    U_100m = []
    V_100m = []
    U_10m = []
    V_10m = []
    T = []
    CLCT = []

    for column in full_data.columns:
        if (column.__contains__('U')) and (column.__contains__('NWP1') or column.__contains__('NWP2') or column.__contains__('NWP3')):
            U_100m.append(column)
        elif (column.__contains__('V')) and (column.__contains__('NWP1') or column.__contains__('NWP2') or column.__contains__('NWP3')):
            V_100m.append(column)
        elif (column.__contains__('U')) and (column.__contains__('NWP4')):
            U_10m.append(column)
        elif (column.__contains__('V')) and (column.__contains__('NWP4')):
            V_10m.append(column)
        elif (column.__contains__('_T')):
            T.append(column)
        elif (column.__contains__('CLCT')):
            CLCT.append(column)

    full_data['U_100m'] = full_data[U_100m].mean(axis=1)
    full_data['V_100m'] = full_data[V_100m].mean(axis=1)
    full_data['U_10m'] = full_data[U_10m].mean(axis=1)
    full_data['V_10m'] = full_data[V_10m].mean(axis=1)
    full_data['T'] = full_data[T].mean(axis=1)
    full_data['CLCT'] = full_data[CLCT].mean(axis=1)

    full_data['CLCT'] = full_data['CLCT'].apply(lambda x: 0 if x < 0 else x)

    return full_data

def get_simplified_data():
    simple_data = get_preprocessed_data()
    simple_data = simple_data[['ID','Time','WF','U_100m','V_100m','U_10m','V_10m','T','CLCT','Set']]
    return simple_data

def transform_data(df,shift_n):
    for column in df.columns:
        df[column] = np.log(df[column]) - np.log(df[column].shift(shift_n)) #Stabilize the Mean and Variance
    return df

def revert_data(y_train,y_test):
    reverted_data = y_train[-1] * np.exp(y_test.cumsum())
    return reverted_data

def metric_cnr(dataframe_y_pred,dataframe_y_true):
     cape_cnr = 100*np.sum(np.abs(dataframe_y_pred-dataframe_y_true))/np.sum(dataframe_y_true)
     return cape_cnr