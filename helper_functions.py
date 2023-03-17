#!/usr/bin/env python3
#
# Carson Carpenter
#

import ccxt
import pandas as pd
import numpy as np
import private_key  # API KEYS CONFIG FILE
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
pd.set_option("display.max_rows", None)

# SPOT DATA
exchange_class = getattr(ccxt,'kucoin')
exchange = exchange_class()
kucoin = ccxt.kucoin()
symbol = "BTC/USDT" # SPOT symbol

# Futures Data
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
futures_symbol = "BTC/USDT:USDT" # Futures

timeframe = "1d"
num_bars = 99

# Get Current Price
def current_price(symbol=symbol):
    # Get the current price
    current_price = EXCHANGE.fetch_ticker('BTC/USDT:USDT')['last']
    return print(f'Price: {current_price}')

# Get the current bid/ask
def ask_bid(symbol=futures_symbol):
    """Function to return current bid and ask of ticker"""
    order_book = EXCHANGE.fetch_order_book(symbol)
    bid = order_book["bids"][0][0]
    ask = order_book["asks"][0][0]
    # print(f'\tOrder Book [{symbol}]:\nBid:  {bid}\nAsk:  {ask}\n')
    # print('===============================================================================')
    return ask, bid

# calculate the 24 hour daily_low and high prices
def DailyRange(symbol=symbol):
    """ Calculate the 24 hour daily_low, daily_high, trading_range in dollars
    """
    symbol = "BTC/USD:BTC"
    timeframe = "15m"
    num_bars = 100
    bars = EXCHANGE.fetch_ohlcv(symbol, timeframe=timeframe, limit=num_bars)
    # create a dataframe from the OHLCV data
    ohlcv = bars
    test_dataframe = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])

    # reset the time to milliseconds
    test_dataframe["timestamp"] = pd.to_datetime(test_dataframe["timestamp"], unit="ms")
    # print(test_dataframe)
    
    daily_low = test_dataframe["low"].min()
    daily_high = test_dataframe["high"].max()

    # calculate the low to high range
    trading_range = daily_high - daily_low

    ask, bid = EXCHANGE.fetch_ticker(symbol)["ask"], EXCHANGE.fetch_ticker(symbol)["bid"]
    return daily_low, daily_high, trading_range, ask, bid

# Get Daily High-Low
def day_hilo(symbol=symbol):
    daily_low = DailyRange(symbol)[0]
    daily_high = DailyRange(symbol)[1]
    trading_range = DailyRange(symbol)[2]
    # print(f'daily_low = {daily_low}')
    # print(f'daily_high = {daily_high}')
    # print(f'trading_range = {trading_range}')
    # print the low, daily_high, and low to daily_high range
    ticker_data = kucoin.fetch_ticker("BTC/USDT")
    # print(ticker_data)
    # for symbol2 in ticker_data:
        # print(symbol2)
        
    BTC_vwap = float(ticker_data['vwap'])
    BTC_datetime = ticker_data['datetime']
    BTC_high = float(ticker_data['high'])
    BTC_low = float(ticker_data['low'])
    # print(f'{symbol} DATA:\n{BTC_datetime}\nvwap: {BTC_vwap}\nHigh: {BTC_high}\nLow: {BTC_low}')

    return print(f"\nVWAP: {BTC_vwap}\nDaily Low: {daily_low}\nDaily High: {daily_high}\n")

# Get order_book_signal, bid_volume, ask_volume, imbalance [BID VS ASK IMBALANCE]
def ORDERBOOK(symbol=symbol):
    """Function to return,
        order_book_signal, [BUY/LONG] OR [SELL/SHORT]
        total_bid_orderbook_vol,
        total_ask_orderbook_vol,
        imbalance [BID VS ASK IMBALANCE]"""
    symbol = "BTC/USD:BTC" # Futures?
    ask = ask_bid()[0]
    bid = ask_bid()[1]
    # print(f"============================================= ORDERBOOK ============================================================ \n ")
    order_book = EXCHANGE.fetch_order_book(symbol=symbol, params={"group": 10})

    # print(order_book)
    # for i in order_book:
    #     print(i)

    order_book_symbol = order_book["symbol"]
    order_book_bids = order_book["bids"]
    order_book_ask = order_book["asks"]
    order_book_time = order_book["datetime"]
    # print(f'{order_book_symbol}:\nBids:\n {order_book_bids}\nAsk:\n{order_book_ask}')
    # print(order_book_bids)
    # print(order_book_ask)
    # print(order_book_time)

    bid_vol = []
    bid_price = []

    for i in order_book_bids:
        price = i[0]
        vol = i[1]
        # print(vol)
        # print(price)
        bid_vol.append(vol)
        bid_price.append(vol)

    # print(bid_vol)
    # print(bid_price)

    total_bid_orderbook_vol = sum(bid_vol) * 1000
    # print(f"TOTAL BID ORDERBOOK VOLUME: {total_bid_orderbook_vol}")

    ask_vol = []
    ask_price = []

    for i in order_book_ask:
        price = i[0]
        vol = i[1]
        # print(vol)
        # print(price)
        ask_vol.append(vol)
        ask_price.append(vol)

    # print(ask_vol)
    # print(ask_price)

    total_ask_orderbook_vol = sum(ask_vol) * 1000
    # print(f"TOTAL ASK ORDERBOOK VOLUME: {total_ask_orderbook_vol}")

    # COmpare BID vs ASK
    if total_ask_orderbook_vol > total_bid_orderbook_vol:
        # print("[SHORT] [SELLERS PRESENT] Sum of ASK are greater than BIDS. ")
        order_book_signal = "SHORT"
        orderbook_difference = total_ask_orderbook_vol - total_bid_orderbook_vol
        imbalance = round(orderbook_difference / total_ask_orderbook_vol * 100, 2)
        orderbook_difference = orderbook_difference * -1
        imbalance = imbalance * -1
        # print(f"DIFFERENCE =  {orderbook_difference} which is {imbalance}%")

    elif total_bid_orderbook_vol > total_ask_orderbook_vol:
        # print("[BUY] [BUYERS PRESENT] Sum of BIDS are greater than ASK. ")
        order_book_signal = "BUY"
        orderbook_difference = total_bid_orderbook_vol - total_ask_orderbook_vol
        imbalance = round(orderbook_difference / total_bid_orderbook_vol * 100, 2)
        # print(f"DIFFERENCE =  +{orderbook_difference} which is +{imbalance}%")
    else:
        print("++++ BID VS ASK VOL IS EQUAL ++++++ OR SOME ERROR")

    return (
        order_book_signal,
        total_bid_orderbook_vol,
        total_ask_orderbook_vol,
        imbalance,
    )

# Get Active Positions
def get_positions():
    try:
        positions = EXCHANGE.fetch_positions()
        print(f"Number of open positions: {len(positions)}")
        for position in positions:
            #if "size" in position['info'] and float(position['info']["size"]) > 0:
                print("Symbol:", position["symbol"])
                print("Side:", position["side"])
                print("Size:", position['info']["size"])
                print("Entry Price:", position["entryPrice"])
                print("Mark Price:", position["markPrice"])
                print("Unrealized PNL:", position["unrealizedPnl"])
                print("Leverage:", position["leverage"])
                if position['info']["crossMargin"]:
                    print("Margin Type: Cross")
                else:
                    print("Margin Type: Isolated")
                print("-----------------------------")

    except ccxt.AuthenticationError as e:
        print("Authentication error: ", e)

    except ccxt.ExchangeError as e:
        print("Exchange error: ", e)

    except ccxt.NetworkError as e:
        print("Network error: ", e)

    except Exception as e:
        print("Unknown error: ", e)

# Get Account Balance and Equity
def account():
    # Parameters (Ignore) Limit ORDERS ONLY
    parameters = {"timeInForce": "PostOnly"}
    markets = EXCHANGE.load_markets()
    balance = EXCHANGE.fetchBalance(parameters)
    securities = pd.DataFrame(EXCHANGE.load_markets()).transpose()
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Get the value for accountEquity
    for i in balance:
        # Get the values for accountEquity, availableBalance, and total
        accountEquity = balance["info"]["data"]["accountEquity"]
        unrealisedPNL = balance["info"]["data"]["unrealisedPNL"]
        availableBalance = balance["info"]["data"]["availableBalance"]
        total_USDT = balance["total"]["USDT"]
        free_USDT = balance["free"]["USDT"]
        used_USDT = balance["used"]["USDT"]
        # open_positions = balance['info']['data']['positions']

    print("\n\tAccount Overview:")
    # Print the values
    print(f"Total USDT =  {total_USDT}")
    print(f"Account Equity =  {accountEquity}")
    print(f"Settled USDT =  {availableBalance}")
    print(f"Unrealised PNL =  {unrealisedPNL}")
    print(f"USDT Available to trade =  {free_USDT}")
    print(f"USED USDT  =  {used_USDT}\n")
    # print(f"Open_positions =  {open_positions}\n")
    
if __name__ == "__main__":

    # ORDERBOOK FUNCTION
    order_book_signal = ORDERBOOK(symbol)[0]
    total_bid_orderbook_vol = ORDERBOOK(symbol)[1]
    total_ask_orderbook_vol = ORDERBOOK(symbol)[2]
    imbalance = ORDERBOOK(symbol)[3]
    print(f"ORDERBOOK SIGNAL = {order_book_signal}")
    print(f'Bid Volume [BUY] = {total_bid_orderbook_vol}')
    print(f'ASK Volume [SELL]  = {total_ask_orderbook_vol}')
    print(f"ORDERBOOK IMBALANCE =  {imbalance}%")

    # BID_ASK FUNCTION
    # ask_bid()
    ask = ask_bid()[0]
    bid = ask_bid()[1]
    print(f'\nBID: {bid}\nASK: {ask}\n')
    
    # GET CURRENT PRICE
    current_price()
    
    # DAY_HILO FUNCTION
    day_hilo()

    # GET OPEN POSITIONS
    get_positions()
    
    # ACCOUNT OVERVIEW
    account()
