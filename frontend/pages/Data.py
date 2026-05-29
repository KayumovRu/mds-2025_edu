import os
import pandas as pd
import streamlit as st

os.makedirs("data", exist_ok=True)

st.title("Data")

f = st.file_uploader("Upload file")
if f:
    with open(os.path.join("data", f.name), "wb") as w:
        w.write(f.getvalue())
    st.success(f.name)

files = os.listdir("data")
name = st.selectbox("Files in data", files) if files else None

if name:
    st.write(name)
    if name.lower().endswith(".csv"):
        st.dataframe(pd.read_csv(os.path.join("data", name)).head(20))