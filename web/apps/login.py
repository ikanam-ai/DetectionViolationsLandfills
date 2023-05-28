import streamlit as st
from deta import Deta
import time

deta = Deta('c0dahqob3d5_3pz1eEuAyAQwE4P1waUJwr4cr2anHzp8')
users_db = deta.Base('users')

def register():
    st.title('Registration')

    name = st.text_input('Name')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')

    if st.button('Register'):
        # Check if the user already exists
        existing_user = users_db.get(email)

        if existing_user is not None:
            st.error('User with the given email already exists')
        else:
            # Add the user to the database
            users_db.put({'name': name, 'email': email, 'password': password}, email)
            st.success('Registration successful!')

# Login page
def login():
    st.title('Login')

    email = st.text_input('Email')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        # Retrieve the user from the database
        user = users_db.get(email)
        if user is not None and user['password'] == password:
            st.success('Logged in successfully!')
            # Generate HTML code for redirecting to a new page
        else:
            st.error('Invalid credentials')

# Main function
def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.selectbox('Select a page', ['Login', 'Register'])

    if page == 'Login':
        login()
    elif page == 'Register':
        register()

def app():
    main()
