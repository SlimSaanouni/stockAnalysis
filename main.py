import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

import investmentStrategies as invStrat
from investmentStrategies import MONTH_YEAR

# Seaborn customization
custom_params = {
    "axes.facecolor": "black",   # Fond des axes en noir
    "figure.facecolor": "black", # Fond de la figure en noir
    "axes.edgecolor": "grey",   # Bordures des axes en blanc
    "axes.labelcolor": "white",  # Couleur des étiquettes des axes en blanc
    "xtick.color": "white",      # Couleur des ticks de l'axe x en blanc
    "ytick.color": "white",      # Couleur des ticks de l'axe y en blanc
    "text.color": "white",       # Couleur du texte en blanc
    "legend.edgecolor": "white", # Bordure de la légende en blanc
    "legend.facecolor": "black"  # Fond de la légende en noir
}

sns.set_context("notebook")
sns.set_style("dark", custom_params)

st.sidebar.header("Investment properties")

# List of stocks
stocks = ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "NVDA", "JPM", "V", "JNJ"]

# Sidebar widgets
selected_action = st.sidebar.selectbox("Select a stock name", stocks)
invest_amount = st.sidebar.number_input("Amount to invest (€)", min_value=0, value=1000, step=100)
invest_freq = int(st.sidebar.number_input("Frequency (months)", min_value=1, value=1, step=1))
invest_horiz = int(st.sidebar.number_input("Horizon of investment (months)", min_value=1, value=12, step=1))

# Dates
historical_data = yf.download(selected_action)
min_date = historical_data.index.min().date()
max_date = historical_data.index.max().date()

start_date = st.sidebar.date_input("Start date", min_value=min_date, value=min_date)
end_date = st.sidebar.date_input("End date", min_value=min_date, value=max_date)

# Checks
if start_date >= end_date:
    st.sidebar.error("La date de début doit être antérieure à la date de fin.")
elif invest_horiz > (end_date.year - start_date.year) * 12 + end_date.month - start_date.month:
    st.sidebar.error("L'horizon d'investissement ne doit pas excéder la période sélectionnée.")
else:
    
    if historical_data.empty:
        st.error("Aucune donnée disponible pour cette action et cette période.")
    else:
        ls_colname  = "Lump Sum"
        dac_colname = "Dollar Average Cost"
        
        #Reduce the quantity of data to handle
        mask_up = (historical_data.index <= end_date - pd.DateOffset(months = invest_horiz))
        mask_down = (historical_data.index >= start_date + pd.DateOffset(months = 0))
        closing_idx = historical_data["Close"][mask_down]
        historical_data = historical_data[["Close"]][mask_down & mask_up]

        # Volatility calculus
        volatility = closing_idx.pct_change().rolling(window=30).std() * np.sqrt(252)

        # LS and DAC ROIs calculus
        historical_data[ls_colname]     = invStrat.lump_sum_approach(closing_idx,
                                                       historical_data.index,
                                                       invest_horiz)
        historical_data[dac_colname]    = invStrat.dollar_average_cost_approach(closing_idx,
                                                        historical_data.index,
                                                        invest_horiz,
                                                        invest_freq)
        ls_roi  = historical_data[ls_colname]
        dac_roi = historical_data[dac_colname]

        # Expected returns
        ls_mean_roi = ls_roi.mean()
        dac_mean_roi = dac_roi.mean()
        
        '''
        ### Historical data
        '''
        # Index & Volatility graphs
        fig, ax1 = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=closing_idx, ax=ax1, color="blue", label = 'Price')
        ax1.set_ylabel("Prix de clôture (€)")
        ax1.tick_params(axis="y")
        ax1.legend(loc = 0)
        ax2 = ax1.twinx()
        sns.lineplot(data=volatility, ax=ax2, color="red", label = "Volatility")
        ax2.set_ylabel("Volatilité")
        ax2.tick_params(axis="y")
        ax2.legend(loc = 0)
        plt.title(f"Prix de clôture et volatilité de {selected_action}")
        st.pyplot(fig)

        '''
        ### Forecasts
        '''
        # Metrics
        metrics_container = st.container()
        ls_col, dac_col = metrics_container.columns(2)
        with ls_col:
            '''
            #### Lump sum
            '''
            ls_col.metric("Annualized return rates", f"{ls_mean_roi * 100:.2f}%") 
            ls_amt      = invest_amount * (ls_mean_roi + 1) **  (invest_horiz/ MONTH_YEAR)
            ls_delta    = ls_amt - invest_amount
            ls_col.metric("Expected return amounts", f"{ls_amt:.2f}€", f"{ls_delta:.2f}€") 
        with dac_col:
            '''
            #### Dollar average cost
            '''
            dac_col.metric("Annualized return rates", f"{dac_mean_roi * 100:.2f}%")
            dac_amt      = invest_amount * (dac_mean_roi + 1) **  (invest_horiz/ MONTH_YEAR)
            dac_delta    = dac_amt - invest_amount
            dac_col.metric("Expected return amounts", f"{dac_amt:.2f}€", f"{dac_delta:.2f}€")

        '''
        ### Statistics
        '''
        used_colnames = [ls_colname ,dac_colname]
        historical_data = historical_data[used_colnames]

        fig, axes = plt.subplots(1, 2, figsize=(14, 7))

        # Violin plot
        sns.violinplot(data=historical_data, ax=axes[0], palette="pastel")
        axes[0].set_title("Violin Plot des ROI annualisés glissants")
        axes[0].set_xlabel("Type de ROI")

        # Boxplot
        sns.boxplot(data=historical_data, ax=axes[1], palette="pastel")
        axes[1].set_title("Boxplot des ROI annualisés glissants")
        axes[1].set_xlabel("Type de ROI")
        plt.tight_layout()
        st.pyplot(fig)

