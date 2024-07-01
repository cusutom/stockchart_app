import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

aapl = yf.Ticker('AAPL')
days = 50 #何日分のデータを取得するか
hist = aapl.history(period=f'{days}d')
