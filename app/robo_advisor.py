# this is the "app/robo_advisor.py" file

import csv
import json
import os
from dotenv import load_dotenv

import requests

load_dotenv()

#code for date/time copied from w3resource.com
import datetime
now = datetime.datetime.now()

#for sorting dates
from datetime import datetime

# currency format conversion def given
def to_usd(my_price):
    return f"${my_price:,.2f}" #> $12,000.71

# INFO INPUTS

while True:
    symbol = input("Please specify the stock or cryptocurrency symbol you are interested in exploring (ex. 'MSFT').")
    if len(symbol) > 5:
        print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again.")
        True
    else:
        if not symbol.isalpha():
            print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again.")
            True
        else:
            break

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

get_response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}")

parsed_response = json.loads(get_response.text)

#try/except method adapted from https://www.pythonforbeginners.com/error-handling/python-try-and-except
try:
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
except:
    print("Stock symbol not found. Please start over and try again.")
    exit()

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys())

# sort dates from recent to least recent
dates.sort(key = lambda date: datetime.strptime(date, '%Y-%m-%d'), reverse=True) 

# latest day is now first in the list
latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]

high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)

# INFO OUTPUTS 

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })

date = now.strftime("%Y-%m-%d %H:%M %p")

# DETERMINE RECOMMENDATION:
#
#
#





print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA")
print("REQUEST AT:", date)
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


# if latest close is less than half way between high and low, buy
# if latest close is more than half way between high and low, don't buy