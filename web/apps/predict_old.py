# App for object detection
from utils import get_detection_folder, check_folders
from crop import tile
import redirect as rd

from pathlib import Path
import streamlit as st
from PIL import Image
import subprocess
import os
import uuid
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
    polygon_name = st.text_input("Введите путь к папке для вывода")
    
    
    if source_index == 0 and polygon_name:
        uploaded_file = st.sidebar.file_uploader(
            "Загрузка фотографии", type=['png', 'jpeg', 'jpg'])
        
        photo = Image.open(uploaded_file)

        session_id = str(uuid.uuid4())  # Generate a unique session ID
        output_folder = os.path.join("cropping_imgs", polygon_name)
        os.makedirs(output_folder, exist_ok=True)

        tile(photo, output_folder)

    if st.button('Сделать предсказание'):
        with st.spinner('Подождите...'):

            process = subprocess.run(['yolo', 'task=detect', 'mode=predict', 'model=models/best.pt', 'conf=0.01', 'source={}'.format(source)], capture_output=True, universal_newlines=True)
            output = process.stderr

            russian_labels = re.findall(r'\d+ ([а-яА-ЯёЁ\s]+)', output)
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