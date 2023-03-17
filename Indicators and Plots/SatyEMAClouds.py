import ccxt  # package to connect to exchanges
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt

# Define the symbol and exchange
symbol = "BTC/USDT"
futures_symbol = "BTC/USD:BTC" # Futures

exchange_class = getattr(ccxt,'kucoin')
exchange = exchange_class()

timeframe = "15m"
time_warp = "15m"
fast_ema = 8
pivot_ema = 21
slow_ema = 34
bullish_fast_cloud_color = "green"
bearish_fast_cloud_color = "red"
bullish_slow_cloud_color = "aqua"
bearish_slow_cloud_color = "yellow"
cloud_transparency = 60
show_fast_ema_highlight = False
fast_ema_highlight_color = "green"
show_pivot_ema_highlight = False
pivot_ema_highlight_color = "grey"
show_slow_ema_highlight = False
slow_ema_highlight_color = "white"
show_conviction_arrows = True
bullish_conviction_color = "blue"
bearish_conviction_color = "red"
show_fast_conviction_ema = True
fast_conviction_ema = 13
fast_conviction_ema_color = "green"
show_slow_conviction_ema = True
slow_conviction_ema = 48
slow_conviction_ema_color = "black"

# Initialize exchange and symbol
exchange = ccxt.kucoin()

# Define the symbol 
symbol = "BTC/USDT"
futures_symbol = "BTC/USD:BTC" # Futures
num_bars = 300

# Get historical data
ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
# Convert data to numpy array
np_ohlcv = np.array(ohlcv)
# Extract the close price
price = np_ohlcv[:, 4]

# Calculate the indicators
fast_ema_value = pd.Series(price).ewm(span=fast_ema).mean()
pivot_ema_value = pd.Series(price).ewm(span=pivot_ema).mean()
slow_ema_value = pd.Series(price).ewm(span=slow_ema).mean()
fast_conviction_ema_value = pd.Series(price).ewm(span=fast_conviction_ema).mean()
slow_conviction_ema_value = pd.Series(price).ewm(span=slow_conviction_ema).mean()

# Create plots
fig, ax = plt.subplots()
ax.plot(price, label="Price")
ax.plot(fast_ema_value, label="Fast EMA")
ax.plot(pivot_ema_value, label="Pivot EMA")
ax.plot(slow_ema_value, label="Slow EMA")

# Fill in the plots to create clouds
fast_cloud_color = np.where(fast_ema_value >= pivot_ema_value, bearish_fast_cloud_color, bullish_fast_cloud_color)
ax.fill_between(range(len(price)), fast_ema_value, pivot_ema_value, where=fast_ema_value >= pivot_ema_value, color=fast_cloud_color, alpha=cloud_transparency/100, label="Fast Cloud")
slow_cloud_color = np.where(pivot_ema_value >= slow_ema_value, bearish_slow_cloud_color, bullish_slow_cloud_color)
ax.fill_between(range(len(price)), pivot_ema_value, slow_ema_value, where=pivot_ema_value >= slow_ema_value, color=slow_cloud_color, alpha=cloud_transparency/100, label="Slow Cloud")

# Conviction Arrows (default based on 13/48)
if show_conviction_arrows:
    bullish_conviction = fast_conviction_ema_value >= slow_conviction_ema_value
    bearish_conviction = fast_conviction_ema_value < slow_conviction_ema_value
    bullish_conviction_confirmed = bullish_conviction[:-1] & ~bullish_conviction[1:]
    bearish_conviction_confirmed = bearish_conviction[:-1] & ~bullish_conviction[1:]

    # Conviction EMA
    if show_fast_conviction_ema:
        ax.plot(fast_conviction_ema_value, label="Fast Conviction EMA", color=fast_conviction_ema_color)
    if show_slow_conviction_ema:
        ax.plot(slow_conviction_ema_value, label="Slow Conviction EMA", color=slow_conviction_ema_color)

    # Highlight EMAs
    if show_fast_ema_highlight:
        ax.plot(fast_ema_value, label="Fast EMA Highlight", color=fast_ema_highlight_color)
    if show_pivot_ema_highlight:
        ax.plot(pivot_ema_value, label="Pivot EMA Highlight", color=pivot_ema_highlight_color)
    if show_slow_ema_highlight:
        ax.plot(slow_ema_value, label="Slow EMA Highlight", color=slow_ema_highlight_color)

    # Format plot
    ax.legend()
    ax.set_title(f"{symbol} ({time_warp})")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")

    # Show plot
    plt.show()
