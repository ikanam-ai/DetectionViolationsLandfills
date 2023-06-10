import webbrowser
import streamlit as st
import streamlit.components.v1 as components


def app():
    st.title("Просмотр панорамы")
    url = 'http://46.243.226.119/'
    if st.button('Открыть панораму'):
        webbrowser.open_new_tab(url)


if __name__ == "__main__":
    app()
