import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas


def app():
    st.sidebar.title("Опции для рисования")

    # Specify canvas parameters in application
    drawing_mode = "rect"  # Set drawing mode to "rect" for drawing boxes
    stroke_width = st.sidebar.slider("Ширина: ", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Цвет обрамления: ")
    bg_color = st.sidebar.color_picker("Цвет фона: ", "#eee")
    bg_image = st.sidebar.file_uploader("Фотография на фоне:", type=["png", "jpg"])

    realtime_update = st.sidebar.checkbox("Обновлять в режиме реального времени", True)

    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=Image.open(bg_image) if bg_image else None,
        update_streamlit=realtime_update,
        height=600,  # Increase canvas height
        drawing_mode=drawing_mode,
        key="canvas",
    )

    # Do something interesting with the image data and paths
    if canvas_result.image_data is not None:
        st.image(canvas_result.image_data)
    if canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        for col in objects.select_dtypes(include=['object']).columns:
            objects[col] = objects[col].astype("str")
        objects["Label"] = get_labels(objects)  # Get labels for each box
        st.dataframe(objects)

        # Add a button to save the DataFrame to Excel
        if st.button("Сохранить в расширении Excel"):
            save_to_excel(objects)

        # Convert bounding boxes to YOLOv3 format and display
        yolo_labels = convert_to_yolo(objects)
        st.text_area("Наименования лейблов для YOLOv8", value="\n".join(yolo_labels))


def get_labels(objects):
    labels = []
    for _ in range(len(objects)):
        label = st.text_input(f"Лейбл для прямоугольника номер: {_+1}")
        labels.append(label)
    return labels


def save_to_excel(df):
    file_path = st.text_input("Введите путь для сохранения файла:")
    if file_path:
        df.to_excel(file_path, index=False)
        st.success("Успешное сохранение.")


def convert_to_yolo(objects):
    yolo_labels = []
    for index, row in objects.iterrows():
        label = row["Label"]
        x, y, width, height = row["left"], row["top"], row["width"], row["height"]
        image_width = row["width"]
        image_height = row["height"]

        # Normalize the coordinates
        x_center = (x + width / 2) / image_width
        y_center = (y + height / 2) / image_height
        normalized_width = width / image_width
        normalized_height = height / image_height

        # Format the label in YOLOv3 format
        yolo_label = f"{label} {x_center:.6f} {y_center:.6f} {normalized_width:.6f} {normalized_height:.6f}"
        yolo_labels.append(yolo_label)

    return yolo_labels


if __name__ == '__main__':
    app()
