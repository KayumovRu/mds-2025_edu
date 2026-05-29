import requests
import streamlit as st

st.title("Train")

with st.form("train_form"):
    filename = st.text_input("Файл данных в data/")
    model_name = st.text_input("Название модели")
    train_size = st.number_input("Размер обучающей выборки", 0.1, 0.9, 0.8, 0.1)
    submit = st.form_submit_button("Обучить модель")

if submit:
    r = requests.post(
        "http://localhost:8000/train",
        json={"filename": filename, "model_name": model_name, "train_size": train_size},
    )
    st.write(r.json())