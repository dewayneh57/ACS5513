import numpy as np
import pandas as pd

#
# Load the Ames Housing dataset
#
def load_data(): 
    df = pd.read_csv('AmesHousing.csv')
    return df

#
# Print the head.
#
def describe(df):
    print(df.head())
    print(df.shape)
    df.info()
    df.describe().T[['mean', 'std', 'min', 'max']].round(2).sort_values('mean')
    
    

df = load_data()
describe(df)