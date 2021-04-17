from datetime import datetime
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
    
dataDict = {"PriceINR" : prices, "Date" : dates}
#CSV
df = pd.DataFrame(dataDict)
df.to_csv("Prices.csv")
print(dataDict)
#Adding Difference
df["Difference"] = df["PriceINR"].diff()

#Getting USD
from datetime import datetime
from forex_python.converter import CurrencyRates
c = CurrencyRates()
now = datetime.now()

dollarRate = c.get_rate('USD', 'INR', now)

df["PriceUSD"] = round(df["PriceINR"] / dollarRate, 1)
print(df)

#Plotting
import matplotlib.pyplot as plt
plt.plot(df["Date"], df["PriceUSD"])
plt.title('LineGraph')
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True)
plt.show()
