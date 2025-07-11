import numpy as np
import pandas as pd

#
# Load the Ames Housing dataset
#
def load_data(): 
    df = pd.read_csv('AmesHousing.csv')
    return df

#
# Describe the dataset
#
def describe(df):
    print(df.head())
    print(df.shape)
    df.info()
    df.describe().T[['mean', 'std', 'min', 'max']]
    
    

df = load_data()
describe(df)