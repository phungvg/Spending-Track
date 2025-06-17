"""
==============================================================================
 Financial Transaction Data Merging Script
==============================================================================
Author: Phung Vuong(Victoria)
Date: June 12, 2025

Purpose: This script merges two financial transaction datasets (credit card and
#          daily household transactions) into a single consolidated dataset for
#          analysis. The goal is to combine transaction data with standardized
#          categories, customer IDs, and dates, and save the result as a CSV file.
#
# Data Sources:
# - credit_card_transactions.csv: Contains 1,048,575 rows of credit card transactions
#   with original customer IDs ranging from 0 to potentially higher values, including
#   outliers (e.g., 1,048,575 to 1,049,963).
# - Daily Household Transactions.csv: Contains 2,461 rows of daily household
#   transactions with varying date formats and currency.
#
# Processing Steps:
# 1. Load and preprocess the credit card dataset (df1):
#    - Rename columns (e.g., 'trans_date_trans_time' to 'transaction_date', 'amt' to 'amount').
#    - Convert transaction dates to datetime format.
#    - Standardize category and subcategory names (lowercase, replace spaces with underscores).
#    - Add a 'subcategory' column if missing, filling with 'other'.
#    - Reassign customer IDs from 0 to 1,048,575, moving outliers to the end and renumbering.

# 2. Load and preprocess the household dataset (df2):
#    - Rename columns (e.g., 'Date' to 'transaction_date', 'Amount' to 'amount').
#    - Parse and standardize transaction dates with random time additions.
#    - Convert amounts to USD (divide by 86).
#    - Standardize category and subcategory names.
#    - Assign new customer IDs from 1,048,576 to 1,051,036.

# 3. Merge the datasets:
#    - Concatenate df1 and df2, preserving original customer IDs.
#    - Sort by transaction date for chronological order.
#    - Reset the index for a clean sequence.
#    - Select only relevant columns (customer_id, transaction_date, amount, category, subcategory).

# 4. Save the merged dataset to 'merged_transactions.csv' in the after_merge directory.
#
# Output:
# - merged_transactions.csv: Contains 1,051,036 rows with customer IDs ranging from
#   0 to 1,051,036, reflecting all transactions in chronological order.
#
# Notes:
# - Visualizations (histograms) are generated for category-wise spending but are
#   not included in this merge-specific script.
# - Ensure the data_info and after_merge directories exist or will be created.
# - The script assumes proper file paths and handles missing values by filling
#   subcategories with 'other'.
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
print('Done')
