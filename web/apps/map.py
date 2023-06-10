import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

def create_map():
    df_poly = pd.read_csv('data_csv/polygons.csv', index_col=0)
    df_aero = pd.read_csv('data_csv/aero.csv').drop(columns=['full_id', 'osm_id', 'osm_type'])

    m = folium.Map((54.384700, 38.707636), zoom_start=7)
    aero = folium.FeatureGroup(name="Аэродромы")
    polygons = folium.FeatureGroup(name="Полигоны ТБО")
    for i in range(len(df_aero)):
        folium.CircleMarker([df_aero.iloc[i]['lat'], df_aero.iloc[i]['lon']],
                            tooltip=df_aero.iloc[i]['name'], radius=4).add_to(aero)

    for i in range(len(df_poly)):
        # TODO: код, который будет выводить нарушения в строку для html
        violations = ''
        html = f"""
        <h3>{df_poly.iloc[i]['name']}</h3>
        <p>Адрес: {df_poly.iloc[i]['address']}</p>
        <p><b>Нарушения:</b></p>
        <p>{violations}</p>
        """
        iframe = folium.IFrame(html=html, width=500, height=300)
        popup = folium.Popup(iframe, max_width=2650)
        folium.CircleMarker([df_poly.iloc[i]['lat'], df_poly.iloc[i]['lon']],
                            popup=popup, radius=6,
                            color='red').add_to(polygons)


    polygons.add_to(m)
    aero.add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)

    return m


def app():
    st.title("Карта местоположений полигонов ТБО и аэродромов")
    m = create_map()
    st_data = st_folium(m, width=700)

if __name__ == "__main__":
    app()
