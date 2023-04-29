from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import yfinance as yf
from forex_python.converter import CurrencyRates
import quandl

quandl.ApiConfig.api_key = "3qzKshxVDHS9sL7vkphZ"
c = CurrencyRates()

# Read input CSV file
df = pd.read_csv('investments.csv')
dfCash = pd.read_csv('cashSavings.csv')

# Define a function to calculate the USD value of an investment based on the amount invested and the current market value
def calculate_value_today(row):
    ticker = row['investment']
    amount = row['investedAmountinUSDValue']
    asset = yf.Ticker(ticker)
    market_price = asset.history(period='1m')['Close'][0]
    return round((amount / market_price),6)

    
def calculate_value_yday(row):
    ticker = row['investment']
    amount = row['investedAmountinUSDValue']
    if row['type'] == 'crypto':
        asset = yf.Ticker(ticker)
        market_price = asset.history(period='1d')['Open'][0]
        return  round((amount / market_price),6)
    elif row['type'] == 'stocks':
        asset = yf.Ticker(ticker)
        market_price = asset.history(period='1d')['Close'][0]
        return  round((amount / market_price),6)

    
def calculate_value_lweek(row):
    ticker = row['investment']
    amount = row['investedAmountinUSDValue']
    asset = yf.Ticker(ticker)
    market_price = asset.history(period='1w')['Open'][0]
    return  round((amount / market_price),6)



#To do:
#1. Add column type, crpyto, stocks/ETF/etc, Cash/Fiat savings, commodities, Property 

#value in USD: TAKE the value today, USDVal/Value Today = num of shares.
#Let the user input and aut convert the amount in fiat to the number of shares to 6 decimal places 
def instConverter(val, curr, ticker):
    if curr != 'USD':
        usdVal = c.convert(curr, 'USD', val)
        asset = yf.Ticker(ticker)
        market_price = asset.history(period='1m')['Close'][0]
        return usdVal / market_price
    else:
        asset = yf.Ticker(ticker)
        market_price = asset.history(period='1m')['Close'][0]
        return val / market_price



#fiat inflation calc
#CPI inflation calculator API - ####SEPARATE SHEET FOR CASH INFLATION STUFF. STOCKS/CRYPTO/COMMODITIES/ETFs On the main
def inflationCal(curr, initialAmt, startdate):
    now = datetime.now()
    if curr == 'USD':
        data = quandl.get("RATEINF/CPI_USA", start_date=startdate, end_date=now.strftime("%Y-%m-%d")) #replace dates
    elif curr == 'GBP':
        data = quandl.get("RATEINF/CPI_GBR", start_date=startdate, end_date=now.strftime("%Y-%m-%d")) #replace dates
    elif curr == 'EUR':
       data = quandl.get("RATEINF/CPI_EUR", start_date=startdate, end_date=now.strftime("%Y-%m-%d"))
    elif curr == 'NZD':
        data = quandl.get("RATEINF/CPI_NZL", start_date=startdate, end_date=now.strftime("%Y-%m-%d"))
    elif curr == 'AUD':
        data = quandl.get("RATEINF/CPI_AUS", start_date=startdate, end_date=now.strftime("%Y-%m-%d"))
    elif curr == 'CAD':
        data = quandl.get("RATEINF/CPI_CAN", start_date=startdate, end_date=now.strftime("%Y-%m-%d"))
    elif curr == 'CHF':
        data = quandl.get("RATEINF/CPI_CHE", start_date=startdate, end_date=now.strftime("%Y-%m-%d"))
    

    # Calculate inflation rate
    inflation_rate = (data.iloc[-1]['Value'] - data.iloc[0]['Value']) / data.iloc[0]['Value']
    return inflation_rate



# Apply the function to calculate USD value of investments today and yesterday
df['valueInShares_yesterday'] = df.apply(lambda row: calculate_value_yday(row), axis=1)
df['valueInShares_today'] = df.apply(lambda row: calculate_value_today(row), axis=1)
df['valueInShares_lastweek'] = df.apply(lambda row: calculate_value_lweek(row), axis=1)

# Calculate daily percentage change
df['change in daily %'] =  round((((df['valueInShares_today'] - df['valueInShares_yesterday']) / df['valueInShares_yesterday']) * 100),6)

# Calculate weekly percentage change
df['change in weekly %'] =  round((((df['valueInShares_today'] - df['valueInShares_lastweek']) / df['valueInShares_lastweek']) * 100),6)

def inflationComputing(row):
    ######PUT THIS IN A SEPARATE SHEET? STOCKS/CRYPTO/COMMODITIES/ETFs On the main
    curr = row['currency'][:-2]
    amount = row['initial amount']
    openDate = datetime.strptime(row['date put aside'], "%Y-%m-%d")

    inflationRate = inflationCal(curr, amount, openDate)
    difference = amount * inflationRate
    realAmt = amount - difference

    row['buying power now'] = realAmt
    row['buying power decrease %']=inflationRate
    return row

####cash file
dfCash = dfCash.apply(lambda row: inflationComputing(row), axis=1)

# Output results to a new CSV file
dfCash.to_csv('outputCash.csv', index=False)


# Output results to a new CSV file
df.to_csv('output.csv', index=False)

# Display the updated dataframe
print(df)
print(dfCash)




#Get some kind of list from yfinance of these things, all Commodities, ETFs, Stocks, Cryptos.
    #List doesnt look possible - need to make my own custom list that is connected to a drop down. 
    #Add a way for user to input the yfinance ticker


#Set up Manual input for Mortgage

#Polish everything and do the first github push


#For UI:
    # 1. Have the user create a table where they can input each column. This is in a panel, and is a FORM. Not a table. Tanble with form data is above, form clears after every input
    # 2. Dropdown box for "ticker" and "type", invested amount (converts to usd in backend) 
    # 3. Save button to add table to main page, runs script automatically
    # 4. Refresh button runs the script upon request.
    # 5. Value yesterday and all that will be grayed out, should never be editable 
    # 6. Different tabs for stocks/commodities/crypto/etfs, and for cash, property. 
    # 7. but under the tabs will have pie charts, etc. 
    # 8. login/register. 
    # 9. Push to GitHub.
    # 10. Server stuff
    # 11. Advert stuff


#Needs error handling for invalid ticker if user input is to be accepted, and bad chars filtered out, etc
#use of database?
#encryption so i can't see peoples portfolios + passwords