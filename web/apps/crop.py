# App for cropping images
import streamlit as st
from PIL import Image
from itertools import product
import os
import uuid

def tile(photo, output_folder):
    w, h = photo.size
    grid = product(range(0, h - (h % (h//3)), h//3), range(0, w- (w % (w // 6)), w//6))
    for num, (i, j) in enumerate(grid):
        box = (j, i, j+ h//3, i+w//6)
        cropped_photo = photo.crop(box).resize((1440, 900), Image.LANCZOS)
        output_path = os.path.join(output_folder, f"output_{num}.jpg")
        cropped_photo.save(output_path)

def app():
    st.title("Обрезка фотографии")
    st.write("Загрузите фотографии для разрезки на части")

    uploaded_file = st.file_uploader("Выбор фото", type=["jpg", "jpeg", "png"])

    output_path = st.text_input("Введите путь к папке для вывода")

    if uploaded_file is not None and output_path:
        photo = Image.open(uploaded_file)

        session_id = str(uuid.uuid4())  # Generate a unique session ID
        output_folder = os.path.join(output_path, f"output_{session_id}")
        os.makedirs(f'cropping_imgs/{output_folder}', exist_ok=True)

        tile(photo, f'cropping_imgs/{output_folder}')

        st.write("Фото успешно разделено по частям!")
        st.write("Части фотографии:")

        for i in range(18):
            split_folder = os.path.join(f'cropping_imgs/{output_folder}', f"split_{i+1}")
            os.makedirs(split_folder, exist_ok=True)

            split_photo_path = os.path.join(f'cropping_imgs/{output_folder}', f"output_{i}.jpg")
            split_photo = Image.open(split_photo_path)

            split_output_path = os.path.join(split_folder, f"split_{i+1}.jpg")
            split_photo.save(split_output_path)

            st.image(split_photo, caption=f"Часть фотографии номер: {i+1}", use_column_width=True)

if __name__ == '__main__':
    app()
