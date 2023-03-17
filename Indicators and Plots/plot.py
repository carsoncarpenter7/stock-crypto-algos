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
markets = exchange.load_markets()
symbols = list(markets.keys())
# print(symbols)
# for i in symbols:
#     print (i)

# Loop through symbols and identify those with BTC and USDT only
# Remove items that do not include /BTC or /USDT
# Sort symbols using lambda function as sorting key
sorted_symbols = sorted(symbols, key=lambda sym: (0, sym) if '/USDT' in sym else (1, sym) if '/BTC' in sym else (2, sym))
# print(sorted_symbols)


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
print(symbol)

timeframe = input('Enter timeframe: [1m, 3m, 5m, 15m, 1h, 1d, 1w]: ')  # allow user input for timeframe
chart_type = input('Enter chart type: [C = candlestick | L = line]: ')  # allow user input for chart type

if chart_type == 'C' or chart_type == 'c':
    chart_type = 'candlestick'
elif chart_type == 'L' or chart_type == 'l':
    chart_type = 'line'
else:
    print("Error: Chart type not supported.")

def plot_chart(symbol, timeframe, chart_type):
    # Fetch the data and convert it to a pandas dataframe
    ohlc = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlc, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df.set_index('timestamp')
    
    # filter data by date starting from 2000
    df = df.loc['2000-01-01':]
    
    if chart_type == 'candlestick':
        # Plot the data as a candlestick chart
        mpf.plot(df, type='candle', volume=True, title=f'{symbol} ({timeframe})')
    elif chart_type == 'line':
        # Plot the data as a line chart to address the warning about plotting too much data
        mpf.plot(df, type='line', volume=True, title=f'{symbol} ({timeframe})', warn_too_much_data=len(df))
    else:
        print('Invalid chart type entered.')
        
plot_chart(symbol, timeframe, chart_type)
