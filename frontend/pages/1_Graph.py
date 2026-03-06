import streamlit as st
import numpy as np
import pandas as pd

st.header("График: синусоида")

delta = st.slider("Delta", 1, 10, 2)

x = np.linspace(0, 10, 100)
y = np.sin(x) + delta

df = pd.DataFrame({
    'x': x,
    'sin(x)': y
})

st.line_chart(df.set_index('x')['sin(x)'])