import os
import pytesseract
import pandas as pd
# import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image
import cv2
import time
import json

##Clear terminal screen before run
if os.name == 'nt':
    os.system('cls')
else: 
    os.system('clear')
##-----------------------------------------------------------------------------------------------------------------------------
##Time date today
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("Running on -- ",dt_string)
print("=== Python Receipt OCR ===")

##Files
output_path = '/Users/panda/Documents/Work/Work_Main/spending_track/ouput'
##-----------------------------------------------------------------------------------------------------------------------------
"""Functions"""
##-----------------------------------------------------------------------------------------------------------------------------
class ReceiptOCR:
    def __init__(self):
        ##Version tesseract 5.5.1
        pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

        ##Common patterns for receipt data
        ##Ex: 01/05/2025 (exact 2/2/4 formats, coult be other way around)
        self.data_patterns = [
            r'\d{2}/\d{2}/\d{4}',
            r'\d{4}-\d{2}-\d{2}',
            r'\d{2}-\d{2}-\d{4}',
            r'\d{1,2}/\d{1,2}/\d{2,4}'
        ]

        ##Patterns for amount, after period is max 2 decimal
        self.amount_patterns = [
            r'TOTAL[:\s]*([0-9,]+\.?\d{0,2})',
            r'Total[:\s]*([0-9,]+\.?\d{0,2})',
            r'Amount[:\s]*([0-9,]+\.?\d{0,2})',
            r'AMOUNT[:\s]*([0-9,]+\.?\d{0,2})',
            r'(\d+\.\d{2})\s*$
        ]

    ##Use the result from matlab after crop, save from output_path
    def preprocess_image(self, image_path):
        image = Image.open(image_path)
        image = image.convert('RGB')
        image.save(image_path)

    ##Text extraction 
    def extract_text(self,image_path):
        
        
##------------------------------------------------------------------------------------------------------------
"""For mannual entry"""
##-----------------------------------------------------------------------------------------------------------------------------
"""Set up for parsing"""
##-----------------------------------------------------------------------------------------------------------------------------
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

   

##-----------------------------------------------------------------------------------------------------------------------------
"""MAIN"""
##-----------------------------------------------------------------------------------------------------------------------------
# def main():
    # ocr = ReceiptOCR()
#     print("\n === RECEIPT SPENDING TRACKER ===")
#     while True:
#         mode = input("Mode (image/manual/quit): ").strip().lower()
#         if mode == "quit":
#             print("Exiting. Final spending summary:")
#             sys.exit(0)

        # if mode == "image":
        #     img_path = input("Enter full path to receipt image: ").strip()
        
        # if mode == "manual":
        #     print("\n")


        

# if __name__ == "__main__":
#     main()