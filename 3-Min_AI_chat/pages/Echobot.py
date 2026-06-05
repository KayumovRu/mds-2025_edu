import streamlit as st

st.set_page_config("Чат с ИИ", layout='wide')

st.title("Чат с ИИ")

messages = st.container(height=600)

req = st.chat_input("Скажите что-нибудь")

if req:
    messages.chat_message("user").write(req)
    messages.chat_message("assistant").write(f"сам {req}!")