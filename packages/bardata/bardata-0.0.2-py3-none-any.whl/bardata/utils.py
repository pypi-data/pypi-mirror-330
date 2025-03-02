""" utility routines """

import logging
import warnings

import numpy as np
import pandas as pd

from .freqs import pandas_freq

logger = logging.getLogger(__name__)



def extract_datetime(prices):
    """extract datetime from index data"""

    for level in range(prices.index.nlevels):
        index = prices.index.get_level_values(level)
        if isinstance(index, pd.DatetimeIndex):
            return index.to_series(index=prices.index)
        
    raise ValueError("No datetime index!")



def get_sampling(prices, basis=365):
    """average yearly sampling rate"""

    dates = extract_datetime(prices)
    interval = dates.diff().mean()

    if interval:
        return pd.Timedelta(days=basis) / interval

    return np.nan


def resample_prices(prices, freq):
    """resample prices"""

    freq = pandas_freq(freq)

    aggspec = dict(open="first", high="max", low="min", close="last", volume="sum")
    prices = prices.resample(freq).agg(aggspec).dropna(subset=["close"])

    return prices


def concat_prices(frames, convert_utc=True, remove_duplicates=True):
    """concatanate prices and remove duplicates"""

    if convert_utc:
        frames = [f.tz_convert("UTC") for f in frames]

    prices = pd.concat(frames)

    if remove_duplicates:
        prices = prices[~prices.index.duplicated(keep="last")]

    return prices


def price_gaps(prices):
    """price gaps in series"""

    if not prices.index.is_monotonic_increasing:
        raise ValueError("Data is not ordered!")

    close = prices.close
    trange = prices.high / prices.low - 1.0
    change = close.pct_change()

    std = change.rolling(30, center=True).std()

    max_change = 0.25

    mask = (
        (change.abs() > max_change)
        & (change.abs() > std * 5.0)
        & (change.abs() > trange * 2.0)
    )

    result = change[mask].rename("gaps")

    return result


def time_gaps(prices, max_days=7):
    """time gaps in series"""

    dates = extract_datetime(prices)
    dspan = dates.diff()

    result = dspan[dspan > pd.Timedelta(days=max_days)].rename("time gap")

    return result


def check_prices(prices, ticker="series", warn=True, verbose=False):
    """check prices for possible gaps in price or time"""

    if prices is None:
        return False

    result = True

    pgaps = price_gaps(prices)
    tgaps = time_gaps(prices)

    if len(pgaps):
        result = False
        if warn:
            warnings.warn(f"{ticker} has {len(pgaps)} price gaps!", stacklevel=2)
        if verbose:
            print(pgaps)

    if len(tgaps):
        result = False
        if warn:
            warnings.warn(f"{ticker} has {len(tgaps)} time gaps!", stacklevel=2)
        if verbose:
            print(tgaps)

    return result


def slice_prices(prices, start_date=None, end_date=None, max_bars=None):
    """slice prices dataframe"""

    if start_date is not None:
        prices = prices.loc[start_date:]

    if end_date is not None:
        prices = prices.loc[:end_date]

    if max_bars:
        prices = prices.tail(max_bars)

    return prices
