import streamlit as st
import requests

st.set_page_config(page_title="ML via FASTAPI", layout='wide')

data_path = st.text_input("Путь к данным", value="data/iris.csv")
model_name = st.text_input("имя модели", value="model_1")
train_size = st.slider("Train Size", 0.1, 0.9, 0.7)
max_iter = st.slider("Max iter", 50, 300, 100)

if st.button("Train"):

    payload = {
        "data_path": data_path,
        "model_name": model_name,
        "train_size": train_size,
        "max_iter": max_iter
    }

    try:
        responce = requests.post(
            "http://127.0.0.1:8000/train_big",
            json=payload,
            timeout=15
        )

        if responce.status_code == 200:
            result = responce.json()

            st.success(result["message"])

            st.write("имя модели:", result["model_name"])

            st.warning(result["model_score"])

    except Exception as e:
        st.error(f"Error: {e}")