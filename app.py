import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

tickers = {
    'apple':'AAPL',
    'facebook':'META', #facebook社の名前が(2024/7/7時点)変わっているため、METAにする
    'google':'GOOGL',
    'netflix':'NFLX',
    'amazon':'AMZN',
}

def get_data(tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        days = 5 #何日分のデータを取得するか
        hist = tkr.history(period=f'{days}d')
        print(hist)
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns= [company]
        hist = hist.T #hist.T=Tranceport(グラフの縦横軸の転換)
        hist.index.name = 'Name'
        df = pd.concat([df, hist]) #concatで表を縦に連結    
    return df

st.write(get_data(tickers))