import datetime
from datetime import timedelta
from forex_python.bitcoin import BtcConverter
import csv
import pandas as pd
#Dates
startDate = datetime.datetime(int(input("Enter The Starting Year")), int(input("Enter The Starting Month")), int(input("Enter The Starting Day")))

endingDate = datetime.datetime(int(input("Enter The Ending Year")), int(input("Enter The Ending Month")), int(input("Enter The Ending Day")))

#Getting the dates in between
delta = endingDate - startDate

dates = []

for i in range(delta.days + 1):
    day = startDate + timedelta(days=i)
    dates.append(day)
    
#Convert Dates To Bitcoin Prices
columnName1 = "Price"
columnName2 = "Date"
b = BtcConverter()
dataDict = {}
prices = []
for key in dates:
    price = round(b.get_previous_price("INR", key), 1)
    prices.append(price)
    
dataDict = {"Price" : prices, "Date" : dates}
#CSV
df = pd.DataFrame(dataDict)
df.to_csv("PricesOfBitcoin.csv")
