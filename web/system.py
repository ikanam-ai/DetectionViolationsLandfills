import streamlit as st
from multiapp import MultiApp
from apps import login, crop, yolo, label, drone # import your app modules here

app = MultiApp()

st.markdown("""
# Приложение для детекции свалок. Задача 11. Команда @ikanam
""")

# Add all your application here
app.add_app("Войти & Регистрация", login.app)

app.add_app('Обрезка панорамной фотографии', crop.app)

app.add_app('Подключение видеотрансляции с БПЛА', drone.app)

# Only add the YOLO prediction app if the login is successful
app.add_app("Детекция объектов", yolo.app)

app.add_app('Разметка изображений', label.app)


# The main app
app.run()