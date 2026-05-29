import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ирисы", layout='wide')

@st.cache_data(ttl=10)
def load_data():
    df = pd.read_csv("data/Iris.csv")
    print("Загрузил снова...")
    return df

df = load_data()

species_options = df["Species"].unique()

select_species = st.selectbox(
    label="Выберите класс",
    options=species_options,
    label_visibility='collapsed',
    index=None
)

filtred_df = df[df["Species"] == select_species]

st.dataframe(filtred_df)

x_axis = "Id"
y_axis = st.selectbox("Y", df.columns[:-1])

st.scatter_chart(
    filtred_df,
    x=x_axis,
    y=y_axis,
    color="Species"
)
