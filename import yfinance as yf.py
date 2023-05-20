import yfinance as yf
import pandas_ta as ta
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import numpy as np

yf.pdr_override()
symbol = "HDFC"

stock_data = yf.download(symbol+".ns", period="1y", interval="1h")
bbands = ta.bbands(stock_data["Close"], length=20, std=2)
data = pd.concat([stock_data[["Open", "High", "Low", "Close"]], bbands[["BBM_20_2.0", "BBU_20_2.0"]]], axis=1)
graphdata = pd.concat([stock_data, bbands], axis=1)

data["Signal"] = np.where(data["Close"] > data["BBU_20_2.0"], "Buy",
                          np.where(data["Close"] < data["BBM_20_2.0"], "Sell", ""))
print(data)
markers = pd.DataFrame(index=data.index)

markers["Buy"] = np.where(data["Signal"] == "Buy", data["Close"], np.nan)

markers["Sell"] = np.where(data["Signal"] == "Sell", data["Close"], np.nan)

markers["Short"] = np.where(data["Signal"] == "Short", data["Close"], np.nan)

markers["SquareOff"] = np.where(data["Signal"] == "Square Off", data["Close"], np.nan)

fig, axes = mpf.plot(graphdata, type="candle", mav=(20), volume=False,
                     title=f"{symbol} Candlestick Chart with Bollinger Bands",
                     tight_layout=True, style="yahoo",
                     addplot=[
                         mpf.make_addplot(graphdata["BBU_20_2.0"], color="b"),
                         mpf.make_addplot(graphdata["BBM_20_2.0"], color="b"),
                         mpf.make_addplot(graphdata["BBL_20_2.0"], color="b")
                     ],
                     returnfig=True)

axes[0].scatter(markers.index, markers["Buy"], marker="^", color="green", s=100)
axes[0].scatter(markers.index, markers["Sell"], marker="v", color="red", s=100)
axes[0].scatter(markers.index, markers["Short"], marker="v", color="black", s=100)
axes[0].scatter(markers.index, markers["SquareOff"], marker="^", color="yellow", s=100)

plt.show()

print(data)
