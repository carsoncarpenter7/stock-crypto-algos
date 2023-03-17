#!/usr/bin/env python3

import ccxt
import private_key # API KEYS CONFIG FILE
import schedule
import pandas as pd
import numpy as np
from datetime import datetime
import time
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_rows', None)

EXCHANGE = ccxt.kucoinfutures(
    {
        "enableRateLimit": True,
        "apiKey": private_key.kucoinfutures_key,  # keep private
        "secret": private_key.kucoinfutures_secret,  # keep private
        "password": private_key.kucoinfutures_pass,  # keep private
    }
)

def price_close(data):
    data['previous_close'] = data['close'].shift(1)
    data['high-low'] = abs(data['high'] - data['low'])
    data['high-pc'] = abs(data['high'] - data['previous_close'])
    data['low-pc'] = abs(data['low'] - data['previous_close'])
    price_close = data[['high-low', 'high-pc', 'low-pc']].max(axis=1)
    return price_close

def atr(data, period):
    data['price_close'] = price_close(data)
    atr = data['price_close'].rolling(period).mean()
    return atr

def supertrend(df, period=7, atr_multiplier=3):
    hl2 = (df['high'] + df['low']) / 2
    df['atr'] = atr(df, period)
    df['upperband'] = hl2 + (atr_multiplier * df['atr'])
    df['lowerband'] = hl2 - (atr_multiplier * df['atr'])
    df['in_uptrend'] = True

    for current in range(1, len(df.index)):
        previous = current - 1

        if df['close'][current] > df['upperband'][previous]:
            df['in_uptrend'][current] = True
        elif df['close'][current] < df['lowerband'][previous]:
            df['in_uptrend'][current] = False
        else:
            df['in_uptrend'][current] = df['in_uptrend'][previous]

            if df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
                df['lowerband'][current] = df['lowerband'][previous]

            if not df['in_uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
                df['upperband'][current] = df['upperband'][previous]
        
    return df

def check_buy_sell_signals(df):
    print("checking for buy and sell signals")
    print(df.tail(5))
    last_row_index = len(df.index) - 1
    previous_row_index = last_row_index - 1
    in_pos = True
    if not df['in_uptrend'][previous_row_index] and df['in_uptrend'][last_row_index]:
        print("changed to uptrend, buy")
        in_pos = True
    if df['in_uptrend'][previous_row_index] and not df['in_uptrend'][last_row_index]:
        if in_pos:
            print("changed to downtrend, sell")
            in_pos = False
        else:
            print("You aren't in position, nothing to sell")

def run():
    symbol = "BTC/USD:BTC"
    print(f"Fetching new 15m data for {datetime.now().isoformat()}")
    bars = EXCHANGE.fetch_ohlcv(symbol, timeframe='15m', limit=100)
    df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    supertrend_data = supertrend(df)
    
    check_buy_sell_signals(supertrend_data)

# Refresh every 15 seconds
schedule.every(15).seconds.do(run)

while True:
    schedule.run_pending()
    time.sleep(1)

