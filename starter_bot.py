#!/usr/bin/env python3

import ccxt
import utils as help
import private_key # API KEYS CONFIG FILE
import time, schedule

# Global Variables
EXCHANGE = ccxt.kucoinfutures(
    {
        "enableRateLimit": True,
        "apiKey": private_key.kucoinfutures_key,  # keep private
        "secret": private_key.kucoinfutures_secret,  # keep private
        "password": private_key.kucoinfutures_pass,  # keep private
    }
)
kucoin = ccxt.kucoin()
symbol = "BTC/USDT" # SPOT symbol
futures_symbol = "BTC/USD:BTC" # Futures
timeframe = "1d"
num_bars = 99

# ORDERBOOK FUNCTION
order_book_signal = help.ORDERBOOK(symbol)[0]
total_bid_orderbook_vol = help.ORDERBOOK(symbol)[1]
total_ask_orderbook_vol = help.ORDERBOOK(symbol)[2]
imbalance = help.ORDERBOOK(symbol)[3]
print(f"ORDERBOOK SIGNAL = {order_book_signal}")
print(f'Bid Volume [BUY] = {total_bid_orderbook_vol}')
print(f'ASK Volume [SELL]  = {total_ask_orderbook_vol}')
print(f"ORDERBOOK IMBALANCE =  {imbalance}%")

# BID_ASK FUNCTION
ask = help.ask_bid()[0]
bid = help.ask_bid()[1]
print(f'\nbid = {bid}\nask = {ask}\n')

# DAY_HILO FUNCTION
help.day_hilo()

# ACCOUNT OVERVIEW
help.account()

# GET POSITIONS
help.get_positions()

# TODO: 
# Implement Strategy
# Implement buying and Selling 

# RUN THIS EVERY 30 seconds
def bot():
    """PUT THE STRATEGY HERE
    """
    print("-------------------- Starting Bot --------------------")
    schedule.every(3).seconds.do(bot)
    # schedule.every(30).seconds.do(bot)

    while True:
        try:
            schedule.run_pending()
        except:
            print('+++ maybe an internet problem... code failed, sleeping 10')
            time.sleep(10)

if __name__ == "__main__":
    bot()