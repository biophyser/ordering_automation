import pandas as pd
from selenium import webdriver
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep
import uo_config
from utilities import *



# Access Purchasing Google Sheet
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(uo_config.uoauto_sheet_keyfile, scope)
client = gspread.authorize(creds)
# Get sheet data
sheet = client.open('Purchasing Requests ').sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)
# Get new orders
# CHANGE THIS, INSTEAD OF A COPY WORK WITH THE ORIGINAL DATAFRAME SO THE
# GOOGLE SHEET CAN BE UPDATED AFTER
new_orders = df[df['Order Placed'].apply(lambda x: x.lower()) != 'x'].copy()
new_orders = new_orders.iloc[get_consecutive_index(new_orders),:]
# Fix index numbers
new_orders.loc[:, "Index # used"] = check_index_nums(new_orders["Index # used"])
# Split orders by index # and vendor name
individual_orders = group_orders(new_orders)


# Connect to the ordering website
site = uo_config.site

driver = webdriver.Chrome(uo_config.chrome_driver)
driver.get(site)

for order in individual_orders:
    # Fill in the head info
    fill_form_header(driver)
    # Fill in the vendor info for the order
    fill_form_vendor_index(driver, order)
    if len(order) < 6:
        # Fill in the item info
        fill_form_item(driver, order)
        submit_button = driver.find_element_by_name("Submit") 
        submit_button.click()
    else:
        print('What! This never happens!')
        break
    driver.get(site)


