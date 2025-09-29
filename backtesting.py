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
tickers = [
    # Forex
    "EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "USDCAD=X", "USDCHF=X", "NZDUSD=X",
    # Cryptos
    "BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", "SOL-USD", "ADA-USD",
    # Commodities
    "GC=F", "SI=F", "CL=F", "BZ=F", "NG=F", "HG=F", "ZS=F", "KC=F",
    # Indices
    "^GSPC", "^DJI", "^IXIC", "^FTSE", "^GDAXI", "^FCHI", "^N225", "^HSI",
    # Equities
    "AAPL", "MSFT", "AMZN", "GOOG", "META", "TSLA", "NVDA", "JPM", "XOM", "BRK-B"
]
listalpha = [0.01, 0.02, 0.05, 0.10, 0.25, 0.50]
asset=st.selectbox("Select an asset:",tickers)
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
niveauconfiance=1-alpha
st.write(f"Historical VaR at {int{niveauconfiance*100}}% :", VaRH)
VaRP=(Espérance+Ecarttype*z_score)
st.write(f"Parametric VaR at {int{niveauconfiance*100}}% :", VaRH)
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





    




