import ccxt
import pandas as pd
import matplotlib.pyplot as plt

exchange_class = getattr(ccxt,'kucoin')
exchange = exchange_class()
kucoin = ccxt.kucoin()

symbol = "BTC/USDT" # SPOT symbol
futures_symbol = "BTC/USDT:USDT" # Futures
timeframe = "1h"
num_bars = 99

symbol = input('Enter symbol: [BTC, ETH, SOL, LINK] ')
if 'BTC' in symbol or 'btc' in symbol:
    symbol = 'BTC/USDT'
elif 'ETH' in symbol or 'eth' in symbol:
    symbol = 'ETH/USDT'
elif 'SOL' in symbol or 'sol' in symbol:
    symbol = 'SOL/USDT'
elif 'LINK' in symbol or 'link' in symbol:
    symbol = 'LINK/BTC'
else:
    print("Error Symbol not supported")
# print(symbol)

# Get the historical data for the symbol
ohlcv = kucoin.fetch_ohlcv(symbol, timeframe, limit=num_bars)
# Convert the data to a dataframe
df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
# Convert the timestamp to a datetime object
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
# Calculate the 20-day simple moving average
df["sma20"] = df["close"].rolling(window=20).mean()
# # Get last value of the SMA20
# last_sma = df["sma20"].iloc[-1])

# Plot the closing price and the SMA20
plt.plot(df["timestamp"], df["close"], label="Closing Price")
plt.plot(df["timestamp"], df["sma20"], label="20-day SMA")

# Set the plot title and axis labels
plt.title(f"{symbol} {timeframe} Price Chart")
plt.xlabel("Date")
plt.ylabel("Price")

# Add a legend and show the plot
plt.legend()
plt.show()
