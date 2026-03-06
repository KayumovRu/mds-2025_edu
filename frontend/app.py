import streamlit as st

st.title("Делаем демо Streamlit")

# Ввод имени
name = st.text_input("Введите ваше имя:", placeholder="Студент")

# Слайдер для числа
number = st.slider("Выберите число (0-10):", 0, 10, 5)

# Кнопка для расчёта
if st.button("Посчитать квадрат!"):
    result = number ** 2
    st.info(f"Привет, {name}! Квадрат числа {number} = {result}")
    st.balloons()  # Весёлый эффект