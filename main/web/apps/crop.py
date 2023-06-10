# App for cropping images
import streamlit as st
from PIL import Image
from itertools import product
import os
import uuid
import shutil
import zipfile
import base64

def tile(photo, output_folder):
    w, h = photo.size
    grid = product(range(0, h - (h % (h//3)), h//3), range(0, w- (w % (w // 6)), w//6))
    photos = []
    for num, (i, j) in enumerate(grid):
        box = (j, i, j+ h//3, i+w//6)
        cropped_photo = photo.crop(box).resize((1440, 900), Image.LANCZOS)
        output_path = os.path.join(output_folder, f"output_{num}.jpg")
        cropped_photo.save(output_path)
        photos.append(cropped_photo)
    return photos

def app():
    st.title("Обрезка фотографии")
    st.write("Загрузите фотографии для разрезки на части")

    uploaded_file = st.file_uploader("Выбор фото", type=["jpg", "jpeg", "png"])

    output_path = st.text_input("Введите путь к папке для вывода")

    if uploaded_file is not None and output_path:
        photo = Image.open(uploaded_file)

        session_id = str(uuid.uuid4())  # Generate a unique session ID
        output_folder = os.path.join(output_path, f"output_{uploaded_file.name}")
        os.makedirs(output_folder, exist_ok=True)

        tile(photo, output_folder)

        st.write("Фото успешно разделено по частям!")
        st.write("Части фотографии:")

        for i in range(18):
            split_photo_path = os.path.join(output_folder, f"output_{i}.jpg")
            split_photo = Image.open(split_photo_path)

            split_output_path = os.path.join(output_folder, f"split_{i+1}.jpg")
            split_photo.save(split_output_path)

            st.image(split_photo, caption=f"Часть фотографии номер: {i+1}", use_column_width=True)

        # Add download link for each photo
        download_links = []
        for i in range(18):
            split_output_path = os.path.join(output_folder, f"split_{i+1}.jpg")
            download_links.append(split_output_path)

        if len(download_links) > 0:
            with st.expander("Скачать все"):
                all_zip_path = os.path.join(output_folder, "all_images.zip")

                with zipfile.ZipFile(all_zip_path, "w") as zipf:
                    for file_path in download_links:
                        zipf.write(file_path, os.path.basename(file_path))

                download_link = get_download_link(all_zip_path, "Скачать все фото")
                st.markdown(download_link, unsafe_allow_html=True)

def get_download_link(file_path, text):
    with open(file_path, "rb") as f:
        data = f.read()
    b64_data = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64_data}" download="{os.path.basename(file_path)}">{text}</a>'
    return href
    
if __name__ == '__main__':
    app()
