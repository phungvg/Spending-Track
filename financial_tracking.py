"""
Project Title: Spending Tracking 
Dataset: Credit Card Transactions from Kaggle

** General info: 
- Dataset has 24 columns: Unnamed: 0', 'trans_date_trans_time', 'cc_num', 'merchant', 'category',
       'amt', 'first', 'last', 'gender', 'street', 'city', 'state', 'zip',
       'lat', 'long', 'city_pop', 'job', 'dob', 'trans_num', 'unix_time',
       'merch_lat', 'merch_long', 'is_fraud', 'merch_zipcode'],

Task 1: Clean up datasets, design subsets want to use, diversity of the dataset. 
Drop any duplicate, nans. Look at some model of OCR
"""

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import random

# ---------------------------------------------------------------------------------------------------------------------------------------
"""Data Preprocessing"""
# ---------------------------------------------------------------------------------------------------------------------------------------
# df = pd.read_csv('/Users/panda/Documents/Work/Work_Main/spending_track/demo_project/dataset/before_merge/credit_card_transactions.csv')
# df = pd.read_csv('/Users/panda/Documents/Work/Work_Main/spending_track/demo_project/dataset/before_merge/Daily Household Transactions.csv')
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

# ---------------------------------------------------------------------------------------------------------------------------------------
"""Feature Engineering"""
##Total spending per customer
# df['toal_spent'] = df.groupby(['cc_num'])['amt'].transform('sum')
# print("(12) Total spending per customer:\n", df.toal_spent.head())

## Drop unnecessary columns
# df = df.drop(columns=['gender','merchant', 'street', 'city', 'state', 'zip', 'lat', 'long', 'city_pop', 'job', 'dob', 'trans_num', 'unix_time', 'merch_lat', 'merch_long', 'is_fraud', 'merch_zipcode'])
# print("(13) -- Shape of the dataset after dropping unnecessary columns:",df.shape)

#Transaction Frequency Per Customers to see how often a customer makes a transaction
# df['transaction_freq'] = df.groupby(['cc_num'])['trans_date_trans_time'].transform('count')
# print("(14) -- Transaction Frequency Per Customers:\n", df.transaction_freq.head())
# print("(15) -- General view 1:\n",df.head)

## Changed 'unamed' to 'customer_id'
# df = df.rename(columns={'Unnamed: 0': 'customer_id'})
# print("(16) -- General view 2:\n",df.head)

# ---------------------------------------------------------------------------------------------------------------------------------------
"""Top Spending Categories by Transaction Volume and Amount 
- Transaction Volume: Number of transactions per category
- Amount Spent: Total amount spent per category
"""
## Group by category and aggregate the number of transactions and the total amount spent
# category_stats = df.groupby('category').agg(
#        {'trans_date_trans_time': 'count',
#         'amt': 'sum'})
# category_stats = df.groupby('category').agg(
#        transaction_volume=('amt', 'count'), #Number of transaction
#        total_amount_spent=('amt', 'sum')
# ).sort_values(by="total_amount_spent", ascending=False)

# print("(17) -- Top Spending Categories by Transaction Volume and Amount:\n",category_stats.head())


# ---------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------
