# App for object detection
from utils import get_detection_folder, check_folders
import redirect as rd
import base64

from pathlib import Path
import streamlit as st
from PIL import Image
import subprocess
import os
import re
import pandas as pd
import zipfile



def get_download_link(file_path, text):
    with open(file_path, "rb") as f:
        data = f.read()
    b64_data = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64_data}" download="{os.path.basename(file_path)}">{text}</a>'
    return href


full_labels = [
    'Веса автомобилей',
    'Лужи и грязь на дороге',
    'Горы вырытой земли на свалке',
    'Ограждения',
    'Контрольный пункт, ворота, шлагбаум',
    'Мусор вне территории',
    'Пожар или дым',
    'Пожарный резервуар',
    'Прямоугольные объекты с/без воды для колес',
    'Птица',
    'Ров вокруг свалки',
    'Черные ядовитые лужи',
    'Портативное сетчатое ограждение'
]

Image.MAX_IMAGE_PIXELS = None
# This will check if we have all the folders to save our files for inference
check_folders()

def app():
    st.title('Детекция объектов')
    download_links = []

    source = ("Изображение", "Видеозапись")
    source_index = st.sidebar.selectbox("Выбор типа файла", range(len(source)), format_func=lambda x: source[x])

    if source_index == 0:
        uploaded_files = st.sidebar.file_uploader("Загрузка фотографий", type=['png', 'jpeg', 'jpg'], accept_multiple_files=True)
        name = st.sidebar.text_input("Название полигона: ")
        region = st.sidebar.text_input("Регион: ")
        address = st.sidebar.text_input("Фактический адрес: ")
        lon = st.sidebar.text_input("Долгота: ")
        lat = st.sidebar.text_input("Широта: ")

        if uploaded_files is not None:
            with st.spinner(text='Обработка...'):
                for uploaded_file in uploaded_files:
                    st.sidebar.image(uploaded_file)
                    picture = Image.open(uploaded_file)
                    picture.save(f'data/images/{uploaded_file.name}')
                    source = f'data/images/{uploaded_file.name}'

                # Save information to a dataframe
                df_info = pd.DataFrame({'Название полигона': [name], "Регион": [region], 'Фактический_адрес': [address], "Долгота": [lon], "Широта": [lat]})
                df_info.to_csv(f'data/information/{name}.csv', index=False)
        else:
            st.warning('Загрузите фотографии.')

    else:
        uploaded_file = st.sidebar.file_uploader("Загрузка видео", type=['mp4'])
        if uploaded_file is not None:
            with st.spinner(text='Обработка...'):
                st.sidebar.video(uploaded_file)
                with open(os.path.join("data", "videos", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                source = f'data/videos/{uploaded_file.name}'
        else:
            st.warning('Загрузите видео.')

    if uploaded_files:
        if st.button('Сделать предсказание'):
            with st.spinner('Подождите...'):
                for uploaded_file in uploaded_files:
                    st.sidebar.image(uploaded_file)
                    picture = Image.open(uploaded_file)
                    picture.save(f'data/images/{uploaded_file.name}')
                    source = f'data/images/{uploaded_file.name}'

                    process = subprocess.run(['yolo', 'task=detect', 'mode=predict', 'model=models/best.pt', 'conf=0.15', 'source={}'.format(source)], capture_output=True, universal_newlines=True)
                    output = process.stderr


                    russian_labels = re.findall(r'\d+ ([а-яА-ЯёЁ\s]+)', output)
                    # Create dataframe with labels column
                    df = pd.DataFrame(russian_labels, columns=['Объекты'])

                    # Add a column to check if label exists in output labels
                    df['Наличие'] = df['Объекты'].apply(lambda label: "YES" if label in russian_labels else "NO")

                    st.dataframe(df)

                    if source_index == 0:
                        detection_folder = get_detection_folder()
                        for img in os.listdir(detection_folder):
                            if img.endswith('.jpg') or img.endswith('.jpeg') or img.endswith('.png'):
                                image_path = os.path.join(detection_folder, img)
                                st.image(image_path)

                                download_link = get_download_link(image_path, f"Скачать фотографию для редактирования")
                                st.markdown(download_link, unsafe_allow_html=True)
                                download_links.append(image_path)


                    else:
                        for vid in os.listdir(get_detection_folder()):
                            if vid.endswith('.mp4'):
                                video_path = os.path.join(get_detection_folder(), vid)
                                st.video(video_path)
                
                st.balloons()

            if len(download_links) > 0:
                pathing = st.sidebar.text_input("Путь для скачивания всех картинок: ")
                with st.expander("Скачать все"):
                    all_zip_path = os.path.join(f'/{pathing}', "all_images.zip")

                    with zipfile.ZipFile(all_zip_path, "w") as zipf:
                        for file_path in download_links:
                            zipf.write(file_path, os.path.basename(file_path))

                download_link = get_download_link(all_zip_path, "Скачать все фото")
                st.markdown(download_link, unsafe_allow_html=True)
