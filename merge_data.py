"""
Description:
This script merges two different financial transaction datasets with differing structures:
1. Credit Card Transactions (df1)
2. Daily Transactions (df2)

The goal is to create a unified and clean dataset suitable for expense tracking, analysis, or machine learning.

Key Steps:
- Credit Card Dataset (df1):
    - Contains customer_id as an unnamed column (renamed appropriately)
    - Includes: trans_date_trans_time(format: YYYY-MM-DD HH:MM:SS), category, amt(in USD), 
    - Does NOT include subcategories
    - Does NOT include note

- Daily Transaction Dataset (df2):
    - Does NOT include customer_id (generated during merge)
    - Includes: Date(format: DD/MM/YYYY HH:MM:SS) some have time and some not if not put in random time
Category, Subcategory, Note, Amount(INR need to convert to USD)
    

Data Standardization:
- Common columns are aligned (renamed where needed)
- Missing columns in either dataset are filled with `None` (e.g., subcategory in df1, note in df2)
- All date columns are converted to `datetime` format
- Category names are standardized to lowercase with underscores (e.g., 'Shopping Net' → 'shopping_net')

Merging:
- Rows from both datasets are concatenated into a single DataFrame
- New `customer_id`s are generated consecutively for df2 to avoid overlap with df1
- Final DataFrame includes:
    ['customer_id', 'transaction_date', 'amount', 'category', 'subcategory', 'description', 'note']


Output
- Visualization of each dataset for all categories and amount (in USD) in histogram named df1_histogram.png, df2_histogram.png
- Save the new csv file with merged data under /Users/panda/Documents/Work/Work_Main/spending_track/demo_project/dataset/after_merge

Author: Phung Vuong
Date: 2025-06-12
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap
from datetime import datetime, timedelta
import random
import os

# --------------------------------------------------Load Datasets------------------------------------------------------------------------
##Dataset 1 and 2
df1 = pd.read_csv('/Users/panda/Documents/Work/Work_Main/spending_track/demo_project/dataset/before_merge/credit_card_transactions.csv')
df2 = pd.read_csv('/Users/panda/Documents/Work/Work_Main/spending_track/demo_project/dataset/before_merge/Daily Household Transactions.csv')

## Folders for save df1 and df2 visulization
data_info_path = '/Users/panda/Documents/Work/Work_Main/spending_track/demo_project/dataset/data_info'
# ---------------------------------------------------------------------------------------------------------------------------------------
##Set randome seed for reproducibility
random.seed(42) 

# Define pastel color palette
pastel_colors = [
    '#70A1D7', '#98C8E6', '#AACFE4', '#BECFE8', '#E9764C', '#FDB683', 
    '#FDC394', '#F9D7B0', '#A7D3B8', '#B5DFC5', '#C2E5CD', '#CBEAD2', 
    '#A19ACB', '#C5B8DD'
]
pastel_cmap = ListedColormap(pastel_colors)
# ----------------------------------------------- Clean and Standardize df1 --------------------------------------------------------------
# Rename unnamed column to 'customer_id' if necessary
if df1.columns[0] != 'customer_id':
    df1.rename(columns={df1.columns[0]: 'customer_id'}, inplace=True)

#Rename column to 'customer_id' 
df1.rename(columns={
    'trans_date_trans_time': 'transaction_date',
    'amt': 'amount',
}, inplace=True)

#Convert transaction_date to datetime
df1['transaction_date'] = pd.to_datetime(df1['transaction_date'], format='mixed', dayfirst=True)

# Ensure subcategory column exists
if 'subcategory' not in df1.columns:
    df1['subcategory'] = 'other'

#Standardize subcategory format
df1['subcategory'] = df1['subcategory'].fillna('other').astype(str).str.lower().str.replace(' ', '_')

# Fix customer_id: Reassign to 0 to 1048575
df1 = df1.sort_values('customer_id')  # Ensure sorting for consistency
df1['customer_id'] = np.arange(0, len(df1))  # Assign 0 to 1048575 for 1048575 rows

# ---------------------------------------------------------------------------------------------------------------------------------------

# ------------------ Visualize df1 ------------------
cat_sum_1 = df1.groupby('category')['amount'].sum().sort_values()
n_cat_1 = len(cat_sum_1)

plt.figure(figsize=(12, max(6, 0.3 * n_cat_1)))  # Dynamically scaled height
plt.barh(cat_sum_1.index, cat_sum_1.values, color=pastel_cmap.colors[:n_cat_1])
##Save plot
plt.title('Credit Card Transactions by Category (USD)')
plt.xlabel('Total Amount (USD)')
plt.tight_layout()

# Save in folder
plt.savefig(os.path.join(data_info_path, 'd1_histogram.png'))
plt.close()

# ----------------------------------------------- Clean and Standardize df2 --------------------------------------------------------------
# Rename columns
df2.rename(columns={
    'Date': 'transaction_date',
    'Category': 'category',
    'Subcategory': 'subcategory',
    'Amount': 'amount',
}, inplace=True)


# Convert transaction_date to datetime
def parse_date(d):
    d = str(d).strip()
    try:
        if len(d) > 10 and ':' in d: 
            ##Format: DD/MM/YYYY HH:MM:SS
            return datetime.strptime(d, '%d/%m/%Y %H:%M:%S')

        elif len(d) == 10 and '/' in d:
            ## Format: DD/MM/YYYY (no time), add random time
            base = datetime.strptime(d, '%d/%m/%Y')
            rand_time = timedelta(hours=random.randint(0, 23),
                                minutes=random.randint(0, 59),
                                seconds=random.randint(0, 59))
            return base + rand_time
    except ValueError:
        return pd.NaT
    return pd.NaT


df2['transaction_date'] = df2['transaction_date'].astype(str).apply(parse_date)

#Drop rows with invalid dates
df2 = df2.dropna(subset=['transaction_date'])

##Convert INR to USD, 1 USD = 86 INR
df2['amount'] = df2['amount'] / 86

#Standardize category/subcategory names
df2['category'] = df2['category'].astype(str).str.lower().str.replace(' ', '_')
df2['subcategory'] = df2['subcategory'].astype(str).str.lower().str.replace(' ', '_')

##Create customer_id for df2 after the last customer_id in df1
# df1['customer_id'] = pd.to_numeric(df1['customer_id'], errors='coerce')  # Convert to numeric if possible
# last_id = df1['customer_id'].dropna().astype(int).max()
# df2['customer_id'] = np.arange(last_id + 1, last_id + len(df2) + 1)

#Assign new customer_id starting from 1048576
df2['customer_id'] = np.arange(1048576, 1048576 + len(df2))  # 1048576 to 1051036

# Keep only required columns
df2 = df2[['customer_id', 'transaction_date', 'amount', 'category', 'subcategory']]


# ------------------ Visualize df2 ------------------

cat_sum_2 = df2.groupby('category')['amount'].sum().sort_values()
n_cat_2 = len(cat_sum_2)

plt.figure(figsize=(12, max(6, 0.3 * n_cat_2)))  # Dynamically scaled height
plt.barh(cat_sum_2.index, cat_sum_2.values,color=pastel_cmap.colors[:n_cat_2])
plt.title('Daily Household Transactions by Category (USD)')
plt.xlabel('Total Amount (USD)')
plt.tight_layout()

# Save in folder
plt.savefig(os.path.join(data_info_path, 'df2_histogram.png'))
plt.close()

# ------------------ Merge df1 and df2 ------------------
merged_df = pd.concat([df1, df2], ignore_index=True)

##Sort by dates
merged_df.sort_values(by='transaction_date', inplace=True)
merged_df.reset_index(drop=True, inplace=True)

# Keep only required columns
merged_df = merged_df[['customer_id', 'transaction_date', 'amount', 'category', 'subcategory']]

# ------------------ Visualization of Merged Dataset ------------------
category_totals = merged_df.groupby('category')['amount'].sum().sort_values()
num_categories = len(category_totals)
colors = cm.get_cmap('tab20', num_categories)(range(num_categories))  # distinct colors

## Save CSV
folder_path = '/Users/panda/Documents/Work/Work_Main/spending_track/demo_project/dataset/after_merge'
os.makedirs(folder_path, exist_ok=True)
merged_df.to_csv(os.path.join(folder_path, 'merged_transactions.csv'), index=False)

##Plot merged
cat_sum_merge = merged_df.groupby('category')['amount'].sum().sort_values()
plt.figure(figsize=(14, max(8, 0.3 * len(cat_sum_merge))))# Dynamically adjust height
plt.barh(cat_sum_merge.index, cat_sum_merge.values, color=pastel_cmap.colors[:len(cat_sum_merge)])
plt.title('All Transactions by Category (USD)')
plt.xlabel('Total Amount (USD)')
plt.tight_layout()
plt.savefig(os.path.join(folder_path, 'merge_histogram.png'))
plt.show()
plt.close()

print('--------------------------------------------------------------------')
print("✅ Processing complete. Histograms saved as:")
print(" - df1_histogram.png")
print(" - df2_histogram.png")
print(" - merge.png")
print("Files generated")
