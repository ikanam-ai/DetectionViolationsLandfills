import streamlit as st
from multiapp import MultiApp
from apps import login, yolo, label # import your app modules here

app = MultiApp()

st.markdown("""
# Team Ikanam
""")

# Add all your application here
app.add_app("Login & Registration", login.app)

# Only add the YOLO prediction app if the login is successful
app.add_app("Yolo Prediction", yolo.app)

app.add_app('Mini-Label', label.app)
# The main app
app.run()