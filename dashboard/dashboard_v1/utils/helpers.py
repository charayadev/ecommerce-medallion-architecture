import streamlit as st
from utils.theme import CARD_COLOR, COLOR_PRIMARY, TEXT_COLOR

def load_css(file_path):
    """Reads and injects CSS into the Streamlit app."""
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def draw_kpi(col, title, value, prefix=""):
    """Renders a styled KPI card in the given column."""
    col.markdown(f"""
        <div style="background-color: {CARD_COLOR}; padding: 20px; border-radius: 10px; border-left: 5px solid {COLOR_PRIMARY}; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
            <h4 style="margin:0; color: #94A3B8; font-size: 16px;">{title}</h4>
            <h2 style="margin:0; color: {TEXT_COLOR}; font-size: 32px;">{prefix}{value}</h2>
        </div>
    """, unsafe_allow_html=True)