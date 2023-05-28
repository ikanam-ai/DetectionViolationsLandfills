# App for object detection
from utils import get_detection_folder, check_folders
import redirect as rd

from pathlib import Path
import streamlit as st
from PIL import Image
import subprocess
import os
import re
import pandas as pd

full_labels = [
    'Автовесы (горка из пдд)',
    'Вода лужи и лужища',
    'Горы перекопанной земли на свалке',
    'Заборы',
    'КПП, Ворота, Шлагбаум',
    'Мусор за пределами участка',
    'Огонь или дым',
    'Пожарный резервуар',
    'Прямоугольная фигня с водой/без для колес',
    'Птица',
    'Ров вокруг свалки',
    'Черные ядовитые лужи',
    'переносное сетчатое ограждение'
]

Image.MAX_IMAGE_PIXELS = None
# This will check if we have all the folders to save our files for inference
check_folders()

def app():   
    st.title('Детекция объектов')

    source = ("Изображение", "Видеозапись")
    source_index = st.sidebar.selectbox("Выбор типа файла", range(
        len(source)), format_func=lambda x: source[x])
    
    
    
    if source_index == 0:
        uploaded_file = st.sidebar.file_uploader(
            "Загрузка фотографии", type=['png', 'jpeg', 'jpg'])
        name = st.sidebar.text_input("Название полигона: ")
        region = st.sidebar.text_input("Регион: ")
        address = st.sidebar.text_input("Фактический адрес: ")
        lon = st.sidebar.text_input("Долгота: ")
        lat = st.sidebar.text_input("Широта: ")
        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text='Обработка...'):
                st.sidebar.image(uploaded_file)
                picture = Image.open(uploaded_file)
                picture.save(f'data/images/{uploaded_file.name}')
                source = f'data/images/{uploaded_file.name}'

                # Save information to a dataframe
                df_info = pd.DataFrame({'Название полигона': [name], "Регион":[region], 'Фактический_адрес': [address], "Долгота":[lon], "Широта":[lat], 'Image': [uploaded_file.name]})
                df_info.to_csv(f'data/information/{uploaded_file.name}.csv', index=False)

        else:
            is_valid = False
    else:
        uploaded_file = st.sidebar.file_uploader("Загрузка видео", type=['mp4'])
        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text='Обработка...'):
                st.sidebar.video(uploaded_file)
                with open(os.path.join("data", "videos", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                source = f'data/videos/{uploaded_file.name}'
        else:
            is_valid = False

    if is_valid:
        if st.button('Сделать предсказание'):
            with st.spinner('Подождите...'):
                process = subprocess.run(['yolo', 'task=detect', 'mode=predict', 'model=models/model.pt', 'conf=0.08', 'source={}'.format(source)], capture_output=True, universal_newlines=True)
                output = process.stderr
                st.text(output)

                russian_labels = re.findall(r'\d+ ([а-яА-ЯёЁ\s]+)', output)
                st.write(russian_labels)
                # Create dataframe with labels column
                df = pd.DataFrame(full_labels, columns=['Объекты'])

                # Add a column to check if label exists in output labels
                df['Наличие'] = df['Объекты'].apply(lambda label: "YES" if label in russian_labels else "NO")

                st.dataframe(df)

            if source_index == 0:
                with st.spinner(text='Подготовка изображения.'):
                    for img in os.listdir(get_detection_folder()):
                        st.image(str(Path(f'{get_detection_folder()}') / img))

                    st.balloons()
            else:
                with st.spinner(text='Подготовка видеозаписи.'):
                    for vid in os.listdir(get_detection_folder()):
                        st.video(str(Path(f'{get_detection_folder()}') / vid))

                    st.balloons()