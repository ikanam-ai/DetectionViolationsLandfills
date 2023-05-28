# App for object detection
from utils import get_detection_folder, check_folders
import redirect as rd

from pathlib import Path
import streamlit as st
from PIL import Image
import subprocess
import os

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
        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text='Обработка...'):
                st.sidebar.image(uploaded_file)
                picture = Image.open(uploaded_file)
                picture = picture.save(f'data/images/{uploaded_file.name}')
                source = f'data/images/{uploaded_file.name}'
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
        print('valid')
        if st.button('Сделать предсказание'):
            with rd.stderr(format='markdown', to=st.sidebar), st.spinner('Wait for it...'):
                print(subprocess.run(['yolo', 'task=detect', 'mode=predict', 'model=models/model.pt', 'conf=0.08', 'source={}'.format(source)],capture_output=True, universal_newlines=True).stderr)

                    
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