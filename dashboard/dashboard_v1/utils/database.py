import sqlite3
import pandas as pd
import streamlit as st

@st.cache_data
def load_data(db_path):
    """Loads and caches the Gold layer data."""
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql("SELECT * FROM gold_summary", conn)
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        return df
    except sqlite3.OperationalError:
        return pd.DataFrame()