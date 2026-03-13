import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Синусоида", layout='wide')

if "delta" not in st.session_state:
    st.session_state.delta = 3

with st.sidebar:
    st.session_state.delta = st.slider("Delta", 1, 10, st.session_state.delta)

col_1, col_2 = st.columns(2)

x = np.linspace(0, 10, 100)
y = np.sin(x) + st.session_state.delta

df = pd.DataFrame({
    'x': x,
    'sin(x)': y
})

# колонка
with col_1:
    st.header("График: синусоида")
    st.line_chart(df.set_index('x')['sin(x)'])

expander = st.expander("DEBUG", expanded=True)

expander.text(st.session_state)
