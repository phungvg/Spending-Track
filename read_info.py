import numpy as np 
import pandas as pd
from datetime import datetime
import random

# ---------------------------------------------------------------------------------------------------------------------------------------
"""Data Reading"""
# ---------------------------------------------------------------------------------------------------------------------------------------
# df = pd.read_csv('/Users/panda/Documents/Work/Work_Main/spending_track/demo_project/dataset/before_merge/credit_card_transactions.csv')
# df = pd.read_csv('/Users/panda/Documents/Work/Work_Main/spending_track/demo_project/dataset/before_merge/Daily Household Transactions.csv')
# df = pd.read_csv('/Users/panda/Documents/Work/Work_Main/spending_track/demo_project/dataset/after_merge/merged_transactions.csv')
df = pd.read_csv('/Users/panda/Documents/Work/Work_Main/spending_track/demo_project/dataset/after_merge/merged_transactions.csv')

##Check the dataset info
print("(1) -- General view 0:\n",df.head())
print("(2) -- Shape of the dataset:",df.shape)
print("(3) -- Info of the dataset:",df.info())
print("(4) -- Info of the dataset:",df.describe())
print("(5) -- Columns of the dataset:",df.columns)

#Check missing values
print("(6) -- Missing values of the dataset:",df.isnull().sum())
print("(7) -- Missing values of the dataset:",df.isna().sum())

#Check duplicated values
print("(8) -- Duplicated values of the dataset: ",df.duplicated().sum())

#Check unique values
print("(9) -- Unique values of the dataset:",df.nunique())

#List all categories (Total 14) 
print("(10) -- List all categories:\n",df.category.unique())

#Check data types
print("(11) -- Data types of the dataset:",df.dtypes)

