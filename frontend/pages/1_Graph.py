import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Синусоида", layout='wide')

with st.sidebar:
    delta = st.slider("Delta", 1, 10, 2)

col_1, col_2 = st.columns(2)

x = np.linspace(0, 10, 100)
y = np.sin(x) + delta

df = pd.DataFrame({
    'x': x,
    'sin(x)': y
})

# колонка
with col_1:
    st.header("График: синусоида")
    st.line_chart(df.set_index('x')['sin(x)'])
