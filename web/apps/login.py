import streamlit as st
from deta import Deta
import time

deta = Deta('c0dahqob3d5_3pz1eEuAyAQwE4P1waUJwr4cr2anHzp8')
users_db = deta.Base('users')

def register():
    st.title('Регистрация')

    name = st.text_input('Имя')
    email = st.text_input('Электронная почта')
    password = st.text_input('Пароль', type='password')

    if st.button('Зарегистрироваться'):
        # Check if the user already exists
        existing_user = users_db.get(email)

        if existing_user is not None:
            st.error('Пользователь с таким адресом электронной почты уже существует')
        else:
            # Add the user to the database
            users_db.put({'name': name, 'email': email, 'password': password}, email)
            st.success('Вы успешно зарегстрировались!')

# Login page
def login():
    st.title('Вход')

    email = st.text_input('Электронная почта')
    password = st.text_input('Пароль', type='password')

    if st.button('Вход'):
        # Retrieve the user from the database
        user = users_db.get(email)
        if user is not None and user['password'] == password:
            st.success('Вход успешен!')
            # Generate HTML code for redirecting to a new page
        else:
            st.error('Неправильные данные')

# Main function
def main():

    st.sidebar.title('Навигация')
    page = st.sidebar.selectbox('Выбрать страницу', ['Вход', 'Регистрация'])

    if page == 'Вход':
        login()
    elif page == 'Регистрация':
        register()

def app():
    main()
