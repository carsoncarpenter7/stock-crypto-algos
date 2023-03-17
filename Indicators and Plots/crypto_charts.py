import mplfinance as mpf
import pandas as pd
import ccxt

# Define the symbol and exchange
symbol = "BTC/USDT"
futures_symbol = "BTC/USD:BTC" # Futures

exchange_class = getattr(ccxt,'kucoin')
exchange = exchange_class()

# Define the timeframes and limit
timeframes = ['15m', '1h']
limit = 1000

def plot_linegraph(symbol, timeframe):
    # Fetch the data and convert it to a pandas dataframe
    ohlc = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(
        ohlc, columns=["timestamp", "open", "high", "low", "close", "volume"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df.set_index("timestamp")

    # Plot the data as a line chart to address the warning about plotting too much data
    mpf.plot(df, type="line", volume=True, title=f"{symbol} ({timeframe})", warn_too_much_data=len(df))

def plot_candlestick(symbol, timeframe):
    # Fetch the data and convert it to a pandas dataframe
    ohlc = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlc, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df.set_index('timestamp')
    
    # Plot the data as a candlestick chart
    mpf.plot(df, type='candle', volume=True, title=f'{symbol} ({timeframe})')

# Loop over the timeframes and plot the data for each timeframe
for timeframe in timeframes:
    plot_candlestick(symbol, timeframe)
    plot_linegraph(symbol, timeframe)