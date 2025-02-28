import logging
from typing import List

import pandas as pd
from candlestix import Exchange
from candlestix.candle_loader import CandleDataLoader
from candlestix.candleconf import CandleLength
from pandas import DataFrame


class Level:
    def __init__(self, date, price):
        self.date = date
        self.count = 1
        self.price = price
        self.merged = []
        self.diff_pct = 0.0

    def inc_count(self):
        self.count = self.count + 1

    def __repr__(self):
        return f'Level({self.date}, {self.price}, {self.diff_pct}, {self.count}, {self.merged})'


class SupportResistance:
    def __init__(self, supports: List[Level] = None, resistances: List[Level] = None):
        self.__supports: List[Level] = supports if supports is not None else []
        self.__resistances: List[Level] = resistances if resistances is not None else []

    def get_supports(self) -> List[Level]:
        return self.__supports

    def get_resistances(self) -> List[Level]:
        return self.__resistances

    def __repr__(self):
        indent = '  '  # 2 spaces
        resp = (f'SupportResistance(\n'
                f'{indent}resistances:\n')

        for r in self.__resistances:
            resp += f'{indent*2}{r}\n'

        resp += f'{indent}supports: \n'

        for s in self.__supports:
            resp += f'{indent * 2}{s}\n'

        resp += '\n)'

        return resp


class SupportResistanceDetector:

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def _load_candles(self, symbol: str):
        # 1. fetch candles
        df = CandleDataLoader().candles(symbol, Exchange.NSE, CandleLength.DAY, duration_in_days=365)
        df.reset_index(inplace=True)
        df['date'] = pd.to_datetime(df['date'])
        self._logger.info(f'Loaded candles for {symbol}')
        return df

    # 2. No sweep from last trading  day backwards
    def _detect(self, df: DataFrame, n: int, squash: float) -> SupportResistance:
        cmp = df.iloc[len(df) - 1]['close']
        highs: List[Level] = []
        t = len(df) - 2
        while t > 0:

            # check if this is the highest amongst previous 'N' candles
            i = 1
            res_prev = True
            while i <= n:
                if t - i < 0:
                    break
                res_prev = res_prev and self._higher(df.iloc[t - i]) < self._higher(df.iloc[t])
                i = i + 1

            # check if this is the highest amongst next 'N' candles
            i = 1
            res_nxt = True
            while i <= n:
                if t + i > len(df) - 1:
                    break
                res_nxt = res_nxt and self._higher(df.iloc[t + i]) < self._higher(df.iloc[t])
                i = i + 1

            if res_prev and res_nxt:
                level = Level(df.iloc[t]['date'], self._higher(df.iloc[t]))
                level.diff_pct = 100 * (level.price - cmp) / cmp
                level.diff_pct = round(level.diff_pct, 2)
                highs.append(level)
            t = t - 1

        highs = sorted(highs, key=lambda x: x.price, reverse=True)

        indices_to_remove = []
        for i in range(len(highs)):
            if i in indices_to_remove:  # if this index is marked for deletion, do not process
                continue
            current_price = highs[i].price
            price_threshold = current_price * (1 - squash / 100)
            for j in range(i + 1, len(highs)):
                next_price = highs[j].price
                if next_price >= price_threshold:
                    # If the price difference is within the threshold, mark the row for removal
                    indices_to_remove.append(j)
                    highs[i].inc_count()
                    highs[i].merged.append(highs[j].date.strftime('%Y-%m-%d'))
                    # print(f'marked for removal: {highs[j].date}')
                else:
                    break

        l1 = len(highs)
        # Remove rows marked for removal
        indices_to_remove.sort(reverse=True)
        for i in range(len(indices_to_remove)):
            highs.pop(indices_to_remove[i])

        highs = sorted(highs, key=lambda x: x.date, reverse=True)
        l2 = len(highs)
        # print(f'dropped {l1 - l2} rows')

        # break up into support and resistance collections
        supports: List[Level] = []
        resistances: List[Level] = []
        for l in highs:
            if l.diff_pct >= 0:
                resistances.append(l)
            else:
                supports.append(l)

        resistances = sorted(resistances, key=lambda x: x.diff_pct, reverse=False)
        supports = sorted(supports, key=lambda x: x.diff_pct, reverse=True)
        self._logger.info(f'Levels detected.')
        return SupportResistance(supports=supports, resistances=resistances)

    def _higher(self, df):
        return df["close"] if df["close"] > df["open"] else df["open"]

    def detect(self, stock_symbol: str, level_merge_pct_threshold: float = 2, candles_to_compare: int = 3) -> SupportResistance:
        df = self._load_candles(stock_symbol)
        return self._detect(df, n=candles_to_compare, squash=level_merge_pct_threshold)

    def detect_df(self, df: DataFrame, level_merge_pct_threshold: float = 2, candles_to_compare: int = 3) -> SupportResistance:
        df.reset_index(inplace=True)
        df['date'] = pd.to_datetime(df['date'])
        result = self._detect(df, n=candles_to_compare, squash=level_merge_pct_threshold)
        df.set_index('date', inplace=True)
        return result
