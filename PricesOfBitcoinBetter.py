from datetime import datetime
import datetime
from datetime import timedelta
from forex_python.bitcoin import BtcConverter
from forex_python.converter import CurrencyRates
import csv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics


predDate = datetime.date(2020, 5, 20)

#%%
def GetInputDates():
    startDatestr = input("Enter the start date as DD/MM/YYYY")
    endDatestr = input("Enter the end date as DD/MM/YYYY")
    predDatestr = input("Enter the prediction date as DD/MM/YYYY")
    startDatelist=startDatestr.split('/')
    endDateList=endDatestr.split('/')
    predDateList=endDatestr.split('/')
    startDate = datetime.datetime(int(startDatelist[2]), int(startDatelist[1]), int(startDatelist[0]))
    
    endDate = datetime.datetime(int(endDateList[2]), int(endDateList[1]), int(endDateList[0]))
    
    predDate = datetime.datetime(int(predDateList[2]), int(predDateList[1]), int(predDateList[0]))
    #Getting the dates in between
    delta = endDate - startDate

    dates = []
                                        
    for i in range(delta.days + 1):
        day = startDate + timedelta(days=i)
        dates.append(day)
        
    return dates, delta, startDate, endDate

dates, delta, startDate, endDate = GetInputDates()
print(f"Considering {delta.days} Days From {startDate.date()} To {endDate.date()}")

#%%
def ChooseCurrency():
    currencies = {"BTC" : "Bitcoin", "EUR" : "Euro", "USD" :"American Dollar", "GBP" : "UK Pound", "CHF" : "Switzerland Franc", "JPY" : "Japan Yen"}
    for i in currencies:
        print(f"{i} : {currencies[i]}")
    
    while True:
        inputCurrency = input("Enter A Currency Code : ")
        if inputCurrency in currencies:
            print(f"You Chose {inputCurrency} Which Is {currencies[inputCurrency]}")
            return inputCurrency
            break
        else:
            print(f"{inputCurrency} is not in the list of currencies available")
            
#currency = ChooseCurrency()
currency="BTC"

#%%  
def GetPrices(dates, currency):
    if currency == "BTC":
        b = BtcConverter()
        prices = list(b.get_previous_price_list("INR", startDate, endDate).values())
    else:
        c = CurrencyRates()
        prices = []
        for key in dates:
            price = round(c.get_rate(currency, "INR", key), 4)
            prices.append(price)
    dataDict = {"Date" : dates, f"{currency} To INR" : prices}
    df = pd.DataFrame(dataDict)
    return df

df = GetPrices(dates, currency)


#%%
def Plot(df, currency):
    '''import matplotlib.pyplot as plt
    plt.plot(df["Date"], df[f"{currency} To INR"])
    plt.title(f"{currency} To INR")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)
    plt.show()'''
    df_min=df[df[f"{currency} To INR"]==df[f"{currency} To INR"].min()]
    df_max=df[df[f"{currency} To INR"]==df[f"{currency} To INR"].max()]
    df["SMA"] = df[f"{currency} To INR"].rolling(window = 3).mean()
    print(df.head())
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = df["Date"], y = df[f"{currency} To INR"], mode = "lines"))
    fig.add_trace(go.Scatter(x = df["Date"], y = df["SMA"], mode = "lines"))
    fig.add_trace(go.Scatter(x = df_min["Date"], y = df_min[f"{currency} To INR"],marker={'size':15}))
    fig.add_trace(go.Scatter(x = df_max["Date"], y = df_max[f"{currency} To INR"],marker={'size':15}))
    fig.add_trace(go.Scatter(x = df["Date"], y = [df[f"{currency} To INR"].mean()]*len(df["Date"]),mode = 'lines'))
    
    fig.show()
    
Plot(df, currency)

#%%
def LinearReggeresion(df):
    X = df["Date"]
    y = df[f"{currency} To INR"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 10, shuffle = True)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    new_date = [[predDate]]
    
    prediction = model.predict(new_date)
    print(prediction)
LinearReggeresion(df)