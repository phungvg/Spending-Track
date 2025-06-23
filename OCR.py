import os
import re
import sys
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image
import cv2

# --------------------------------------------------CONFIGURATION-------------------------------------------------------------------------------
##API keys

# --------------------------------------------------CONFIGURATION-------------------------------------------------------------------------------


# --------------------------------------------------SET UP FOR PARSING-------------------------------------------------------------------------------
def parse_item_price(item: str) -> float:
    """
    Given a line-item string like 'latte 3.25', parse the LAST token as float.
    If parsing fails, return None.
    """
    parts = item.strip().split()
    try:
        return float(parts[-1])
    except:
        return None

def mannual_entry():
    print("====Manual Entry Mode====")
    merchant = input("Merchant name: ").strip()
    while merchant is None:
        merchant = input("Merchant cannot be empty. Please re-enter: ").strip()

    date = input("Date (dd/mm/yyyy or dd-mm-yyyy): ").strip()
    while date is None:
        date = input ("Date cannot be empty. Please re-enter: ").strip()
    
    date = input("Date (dd/mm/yyyy or dd-mm-yyyy): ").strip()
    total = None
    while total == None:
        val = input("Total amount (e.g., 193.00): ").strip()
        try:
            total = float(val)
        except:
            print("Invalid amount. Please enter a numeric value (e.g., 193.00).")
            