# %%
# pylint: disable=no-member
import talib.stream as ta # type: ignore
import roboquant as rq
from roboquant.strategies import OHLCVBuffer, TaStrategy

# %%
class MyStrategy(TaStrategy):
    """Example using talib to create a combined RSI/BollingerBand strategy:
    - BUY => RSI < 30 and close < lower band
    - SELL => RSI > 70 and close > upper band
    - otherwise do nothing
    """

    def process_asset(self, asset: rq.Asset, ohlcv: OHLCVBuffer):

        close_prices = ohlcv.close()

        rsi = ta.RSI(close_prices, timeperiod=self.size - 1)  # type: ignore

        upper, _, lower = ta.BBANDS(close_prices, timeperiod=self.size - 1, nbdevup=2, nbdevdn=2)  # type: ignore

        close = close_prices[-1]

        if rsi < 30 and close < lower:
            return rq.Signal.buy(asset)
        if rsi > 70 and close > upper:
            return rq.Signal.sell(asset)

        return None


# %%
feed = rq.feeds.YahooFeed("IBM", "AAPL")
strategy = MyStrategy(14)
account = rq.run(feed, strategy)
print(account)
