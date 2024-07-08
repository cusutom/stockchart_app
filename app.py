import streamlit as st
import pandas as pd
import yfinance as yf
import altair as alt

st.title('米国株価可視化アプリ')
st.sidebar.write("""
# GAFA株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")

st.sidebar.write("""
## 表示日数選択
""")



days = st.sidebar.slider('日数',  1, 5, 60)

st.write(f"""
### 過去 **{days}日間** のGAFA株価
""")

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

companies = ['apple', 'facebook']
df = get_data(tickers)
data = df.loc[companies] #locで[ ]内に指定した条件で情報を抽出できる
data.sort_index() #アルファベット順にソート
data = data.T.reset_index()
data.head()
data = pd.melt(data, id_vars=['Date']).rename(
    columns={'value': 'Stock Prices(USD)'}
) #pandasのmelt関数は雑然としたデータを'Date'を基準に整然してくれる
st.write(data)

ymin=200
ymax=300
chart = (
    alt.Chart(data)
    .mark_line(opacity=0.8, clip=True)
    .encode(
        x="Date:T",
        y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
        color='Name:N'
    )
)
st.write(chart)