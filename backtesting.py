# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 19:02:41 2025

@author: samue
"""

import streamlit as st
import yfinance as yf
import pandas as pd
from scipy.stats import skew, kurtosis, norm
import matplotlib.pyplot as plt


st.title("Value at Risk (VaR) Calculator")
tickers = {
    # --- Forex (Currencies) ---
    "EURUSD=X": "Euro / US Dollar",
    "GBPUSD=X": "British Pound / US Dollar",
    "USDJPY=X": "US Dollar / Japanese Yen",
    "AUDUSD=X": "Australian Dollar / US Dollar",
    "USDCAD=X": "US Dollar / Canadian Dollar",
    "USDCHF=X": "US Dollar / Swiss Franc",
    "NZDUSD=X": "New Zealand Dollar / US Dollar",
    
    # --- Cryptocurrencies ---
    "BTC-USD": "Bitcoin (BTC)",
    "ETH-USD": "Ethereum (ETH)",
    "BNB-USD": "Binance Coin (BNB)",
    "XRP-USD": "XRP (Ripple)",
    "SOL-USD": "Solana (SOL)",
    "ADA-USD": "Cardano (ADA)",
    
    # --- Commodities (Futures) ---
    "GC=F": "Gold Future (GC)",
    "SI=F": "Silver Future (SI)",
    "CL=F": "WTI Crude Oil Future (CL)",
    "BZ=F": "Brent Crude Oil Future (BZ)",
    "NG=F": "Natural Gas Future (NG)",
    "HG=F": "Copper Future (HG)",
    "ZS=F": "Soybean Future (ZS)",
    "KC=F": "Coffee Future (KC)",
    
    # --- Indices ---
    "^GSPC": "S&P 500 Index",
    "^DJI": "Dow Jones Industrial Average",
    "^IXIC": "NASDAQ Composite Index",
    "^FTSE": "FTSE 100 (UK)",
    "^GDAXI": "DAX Index (Germany)",
    "^FCHI": "CAC 40 Index (France)",
    "^N225": "Nikkei 225 (Japan)",
    "^HSI": "Hang Seng Index (Hong Kong)",
    
    # --- Equities (Stocks) ---
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corp.",
    "AMZN": "Amazon.com Inc.",
    "GOOG": "Alphabet Inc. (Class C)",
    "META": "Meta Platforms Inc.",
    "TSLA": "Tesla Inc.",
    "NVDA": "NVIDIA Corp.",
    "JPM": "JPMorgan Chase & Co.",
    "XOM": "Exxon Mobil Corp.",
    "BRK-B": "Berkshire Hathaway Inc. (Class B)"
}
listalpha = [0.01, 0.02, 0.05, 0.10, 0.25, 0.50]
asset=st.selectbox("Select an asset:", options=list(ticker.keys()),format_func=lambda x: ticker[x])
returns_dict = {}
alpha=st.selectbox("Select the risk level", listalpha, format_func=lambda x: f"{int(x*100)}%")

analysis_date = st.date_input("")
window = st.slider("Calculation window (days)", 50, 500, 250)
data = yf.download(asset, start="2015-01-01", end=analysis_date)
data = data.tail(window)
    
    # Calcul des rendements quotidiens
data['Return'] = data['Close'].pct_change()
returns = data['Return'].dropna()
    
    # Stocker dans le dictionnaire
returns_dict[asset] = returns
returnscroissant = returns.sort_values()
nb_valeurs=len(returnscroissant)
Index_VaR=int(nb_valeurs*alpha)
VaRH=returnscroissant.iloc[Index_VaR]
Espérance=returnscroissant.mean()
Médiane=returnscroissant.median()
Variance=returnscroissant.var()
Ecarttype=returnscroissant.std()
z_score = norm.ppf(alpha)
niveauconfiance=(1-alpha)*100
st.write(f"Historical VaR at {niveauconfiance}% :", VaRH)
VaRP=(Espérance+Ecarttype*z_score)
st.write(f"Parametric VaR at {niveauconfiance}% :", VaRH)
testdate=st.date_input("Select the backtesting date (must be later than the analysis date)",min_value=analysis_date)
datatest = yf.download(asset,start=analysis_date, end=testdate, interval="1d")
    
    # Calcul des rendements quotidiens
datatest['Return'] = datatest['Close'].pct_change()
returnstest = datatest['Return'].dropna()
st.write(returnstest)
violations = returnstest[returnstest < VaRP]
num_violations=0
violation_rate=0
if len(returnstest) == 0:
    st.warning("No data available for the backtesting period.")
else:
    num_violations = len(violations)
    total_days = len(returnstest)
    violation_rate = num_violations / total_days
st.write("Number of violations",num_violations)
st.write("Violation rate:",violation_rate)
if violation_rate<=alpha:
    st.success("✅ The VaR model is consistent")
else: 
    st.error("❌ The risk is underestimated")
       # Tracer la courbe des rendements avec les violations et la VaR
fig, ax = plt.subplots(figsize=(12,4))
ax.plot(returnstest.index, returnstest.values, label='Rendement', color='blue')
ax.axhline(y=VaRP, color='red', linestyle='--', label='VaR 95%')
ax.scatter(violations.index, violations.values, color='red', label='Violations', zorder=5)
ax.set_title(f'Daily returns for {asset} with VaR and violations')
ax.set_xlabel('Date')
ax.set_ylabel('Return')
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

st.markdown(
    """
    ---
    👤 **Samuel ZEITOUN, SKEMA PGE Student**  
    🔗 [LinkedIn](https://www.linkedin.com/in/szeitoun11/)  
    📧 [Email](mailto:samuel.zeitoun@skema.edu)
    """,
    unsafe_allow_html=True
)





    






