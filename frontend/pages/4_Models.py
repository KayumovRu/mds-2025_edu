import sqlite3
import pandas as pd
import streamlit as st

st.title("Models")

def load_data():
    conn = sqlite3.connect("models.db")
    df = pd.read_sql_query("SELECT * FROM training_results ORDER BY id DESC", conn)
    conn.close()
    return df

st.button("Обновить")

try:
    df = load_data()
    st.dataframe(df)
except Exception as e:
    st.error(str(e))