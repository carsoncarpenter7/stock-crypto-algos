import pandas as pd
import ccxt

EXCHANGE = ccxt.kucoin()
data = pd.DataFrame(EXCHANGE.fetch_ohlcv('BTC/USDT', timeframe='1h'))

def wyckoff_vpoc_va_vl(data, time_frame):
    """
    Function that calculates the VPOC (Volume Point of Control), VAH, and VAL using the Wyckoff method
    :param data: Dataframe containing 'time', 'open', 'high', 'low', 'close', and 'volume' columns
    :param time_frame: Time frame for the data, options are '1h', '4h', 'd', 'w', 'm'
    :return: a tuple containing (VPOC, VAH, VAL)
    """

    data = data.rename(columns={0: 'timestamp', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'})
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data.set_index('timestamp', inplace=True)
    resampled_data = data.resample(time_frame).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'}).dropna()

    prices = (resampled_data['high'] + resampled_data['low'] + resampled_data['close']) / 3.0
    volumes = resampled_data['volume']

    median_price = prices.median()
    price_diff = prices - median_price
    vol_ratio = volumes / volumes.sum()

    # Value Point of Control
    vpoc = round((vol_ratio * price_diff).sum() + median_price, 2)
    # Value area High
    vah = round(prices.max(), 2)
    # Value area Low
    val = round(prices.min(), 2)

    print("VPOC", vpoc, "| VAH", vah, "| VAL ", val)
    return vpoc, vah, val

wyckoff_vpoc_va_vl(data, "1h")
