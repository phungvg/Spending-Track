"""
==============================================================================
 Financial Transaction Data Merging Script
==============================================================================
Author: Phung Vuong(Victoria)
Date: June 12, 2025

Purpose: This script merges two financial transaction datasets (credit card and
#          daily household transactions) into a single consolidated dataset for
#          analysis. The goal is to combine transaction data with standardized
#          dates, categories, and subcategories and save the result as a CSV file.
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

# --------------------------------------------------CONFIGURATION-------------------------------------------------------------------------------
##Dataset 1 and 2
df1 = pd.read_csv('/Users/panda/Documents/Work/Work_Main/spending_track/demo_project/dataset/before_merge/credit_card_transactions.csv')
df2 = pd.read_csv('/Users/panda/Documents/Work/Work_Main/spending_track/demo_project/dataset/before_merge/Daily Household Transactions.csv')

## Folders for save df1 and df2 visulization
data_info_path = '/Users/panda/Documents/Work/Work_Main/spending_track/demo_project/dataset/data_info'

##After merge folder
after_merge = '/Users/panda/Documents/Work/Work_Main/spending_track/demo_project/dataset/after_merge'

##Set randome seed for reproducibility
random.seed(40) 

# Define pastel color palette
pastel_colors = [
    '#70A1D7', '#98C8E6', '#AACFE4', '#BECFE8', '#E9764C', '#FDB683', 
    '#FDC394', '#F9D7B0', '#A7D3B8', '#B5DFC5', '#C2E5CD', '#CBEAD2', 
    '#A19ACB', '#C5B8DD'
]
pastel_cmap = ListedColormap(pastel_colors)

random_start = datetime(2015, 1, 1)
random_end = datetime.now()

#------------------------------------------------------- HELPERS -----------------------------------------------
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

# Generate random datetime for missing dates
def random_datetime(start, end):
    """Generate a random datetime between start and end."""
    time_between = end - start
    days_between = time_between.days
    random_days = random.randrange(days_between)
    random_seconds = random.randrange(24 * 60 * 60)  # Random time within the day
    return start + timedelta(days=random_days, seconds=random_seconds)

##Generate merchant
def generate_merchant(df):
    merchant = []
    for _, row in df.iterrows():
        category = row['category']
        #Get the list of merchants for this category
        choices = merchant_options.get(category, general_merchant)
        #Randomly select one merchant
        selected_merchant = random.choice(choices)
        merchant.append(selected_merchant)
    return merchant

##Generate subcategory with merchant-specific mapping
def generate_subcategory(df):
    subs = []
    for _, row in df.iterrows():
        merchant = row['merchant']
        if merchant in merchant_subcategory_options:
            options = merchant_subcategory_options[merchant]
        else:
            options = subcategory_options.get(row['category'], general_subcategory)
        selected_sub = random.choice(options)
        subs.append(selected_sub)
    return subs

# ----------------------------------------------- Generate more data --------------------------------------------------------------
subcategory_options = {
    'food':          ['restaurant','cafe','fast_food','food_truck','bistro','bakery','dessert','ice_cream','juice_bar','pizzeria','brewery','fine_dining'],
    'grocery_net':   ['milk','bread','egg','butter','yogurt','cereal','grains','produce','meat','seafood','frozen_food','spices','beverages','snacks'],
    'transportation':['train','bus','taxi','metro','tram','ferry','ride_share','bike_share','car_rental','parking'],
    'clothing':      ['men_clothing','women_clothing','children_clothing','sportswear','accessories'],
    'electronics':   ['mobile_phones','computers','audio','cameras','accessories','home_appliances', 'monitor'],
    'utilities':     ['electricity','water','gas','internet','phone'],
    'entertainment': ['movies','concerts','streaming','amusement_park','theatre'],
    'health':        ['pharmacy','doctor','dentist','optician','gym'],
    'travel':        ['airfare','hotel','tour','cruise','airport_transport'],
    'education':     ['books','online_courses','school_supplies','tuition','seminars']
}

merchant_options = {
    'transportation': ['CTA', 'MTA', 'City Bus Co.', 'Amtrak', 'Greyhound', 'Lyft','Flix Bus'],
    'food':          ['McDonalds','Starbucks','Subway','Burger King','Panera Bread','Chipotle','Olive Garden','Taco Bell','Dunkin','KFC','Red Lobster','Blue Bottle Coffee','Garden Fresh','California Pizza Kitchen','Gyros-Gyros','Tamarine','La Strada'],
    'grocery_net':   ['Walmart','Target','Costco','Whole Foods','Trader Joe\'s','Aldi','Safeway','Kroger','Publix','HEB','Lidl','Hmart','Jungboo'],
    'transportation':['CTA','MTA','Uber','Lyft','Amtrak','Greyhound','Enterprise Rent-A-Car','Zipcar','Bird','Lime'],
    'clothing':      ['Gap','H&M','Uniqlo','Zara','Nike','Adidas','Forever21','Old Navy','Nordstrom','Macy\'s'],
    'electronics':   ['Apple Store','Best Buy','Samsung','Microsoft Store','B&H Photo','Newegg','GameStop'],
    'utilities':     ['ComEd','AT&T','Verizon','Spectrum','PG&E','DTE Energy','Water Works','Con Ed'],
    'entertainment':['AMC Theatres','Regal Cinemas','Netflix','Spotify','Universal Studios','Disney Parks','Ticketmaster'],
    'health':        ['CVS Pharmacy','Walgreens','Rite Aid','Planet Fitness','1-800-Contacts','Kaiser Permanente'],
    'travel':        ['Delta Airlines','Hilton Hotels','Marriott','Expedia','Airbnb','Southwest Airlines','Lyft','Uber'],
    'education':     ['Amazon Education','Coursera','Udemy','Barnes & Noble','Chegg','Khan Academy']
}

##General Merchant
general_merchant = [
    'Walmart', 'Amazon', 'eBay', 'Home Depot', 'CVS', 'Walgreens',
    'Best Buy', 'Barnes & Noble','Apple Store','Nike','eBay','Home Depot']

general_subcategory = [
    'toiletries', 'electronics', 'clothing', 'accessories', 'snacks',
    'stationery', 'pet_food', 'garden_tools', 'health_care', 'cleaning_supplies',
    'pet_supplies','home_goods','auto_maintenance','garden_supplies','books'
    ]

merchant_subcategory_options = {
    'McDonalds':       ['burger','fries','nuggets','coke','milkshake'],
    'Starbucks':       ['coffee','latte','cappuccino','pastry','sandwich','frappuccino'],
    'Dunkin':          ['coffee','donut','bagel','muffin','latte'],
    'Chipotle':        ['burrito','taco','bowl','chips','salsa'],
    'Olive Garden':    ['pasta','soup','salad','breadsticks','steak'],
    'Taco Bell':       ['taco','burrito','nachos','quesadilla'],
    'Apple Store':     ['mac','ipad','iphone','imac'],
    'Nike':            ['jacket','shorts','socks','shoes','pants','shirt'],
}

# ----------------------------------------------- Clean and Standardize df1 --------------------------------------------------------------
print('Loading df1... ⏬⏬')
print('======================================================')
print('======================================================')

# Rename unnamed column to 'customer_id' if necessary
if df1.columns[0] != 'customer_id':
    df1.rename(columns={df1.columns[0]: 'customer_id'}, inplace=True)

#Rename column to 'customer_id' 
df1.rename(columns={
    'trans_date_trans_time': 'transaction_date',
    'amt': 'amount',
}, inplace=True)

df1['merchant'] = generate_merchant(df1)

##Assign the generated subcategories back to df1
df1['subcategory'] = generate_subcategory(df1)

##Standardize date format
df1['transaction_date'] = pd.to_datetime(df1['transaction_date'], errors='coerce')
mask = df1['transaction_date'].isna()
df1.loc[mask,'transaction_date'] = df1.loc[mask].apply(lambda _: random_datetime(random_start,random_end), axis=1)
df1['transaction_date'] = pd.to_datetime(df1['transaction_date']).dt.strftime('%m/%d/%Y %H:%M:%S')

# Reassign customer IDs
df1 = df1.sort_values('customer_id').reset_index(drop=True)
df1['customer_id'] = np.arange(len(df1))
df1 = df1[['customer_id','transaction_date','merchant','category','subcategory','amount']]

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
print('Loading df2... ⏬⏬')
print('======================================================')
print('======================================================')
# Rename columns
rename_map = {'Date':'transaction_date','Category':'category','Subcategory':'subcategory','Amount':'amount'}
df2.rename(columns=rename_map,inplace=True)

##Convert amount to USD
inr_to_usd = 1/86
df2['amount'] = df2['amount'] * inr_to_usd
df2['category'] = df2['category'].astype(str).str.lower().str.replace(' ','_')

##Generate merchant
df2['merchant'] = generate_merchant(df2)

##Generate subcategory with merchant-specific mapping
df2['subcategory'] = generate_subcategory(df2)

##Standardize date format
df2['transaction_date'] = pd.to_datetime(df2['transaction_date'], errors='coerce')
mask = df2['transaction_date'].isna()
df2.loc[mask,'transaction_date'] = df2.loc[mask].apply(lambda _: random_datetime(random_start,random_end), axis=1)
df2['transaction_date'] = pd.to_datetime(df2['transaction_date']).dt.strftime('%m/%d/%Y %H:%M:%S')

# Assign customer IDs after df1
start_id = df1['customer_id'].max() + 1
df2 = df2.reset_index(drop=True)
df2['customer_id'] = df2.index + start_id
df2 = df2[['customer_id','transaction_date','merchant','category','subcategory','amount']]

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
merged_df = merged_df[['customer_id', 'transaction_date', 'merchant', 'amount', 'category', 'subcategory']]
# ------------------ Visualization of Merged Dataset ------------------
print('Merging datasets... ⛓️⛓️')
print('======================================================')
print('======================================================')

category_totals = merged_df.groupby('category')['amount'].sum().sort_values()
num_categories = len(category_totals)
colors = cm.get_cmap('tab20', num_categories)(range(num_categories))  # distinct colors

## Save CSV
os.makedirs(after_merge, exist_ok=True)
merged_df.to_csv(os.path.join(after_merge, 'merged_transactions.csv'), index=False)

##Plot merged
cat_sum_merge = merged_df.groupby('category')['amount'].sum().sort_values()
plt.figure(figsize=(14, max(8, 0.3 * len(cat_sum_merge))))# Dynamically adjust height
plt.barh(cat_sum_merge.index, cat_sum_merge.values, color=pastel_cmap.colors[:len(cat_sum_merge)])
plt.title('All Transactions by Category (USD)')
plt.xlabel('Total Amount (USD)')
plt.tight_layout()
plt.savefig(os.path.join(after_merge, 'merge_histogram.png'))
plt.show()
plt.close()

print('======================================================')
print("🟢🔵🟢🔵🟢🔵🟢")
print("Processing complete. Histograms saved as:")
print(" - df1_histogram.png ✔️")
print(" - df2_histogram.png ✔️")
print(" - merge.png ✔️")
print("Files generated")
print('Done')
