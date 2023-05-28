import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas

def app():
    st.sidebar.title("Drawing Options")

    # Specify canvas parameters in application
    drawing_mode = "rect"  # Set drawing mode to "rect" for drawing boxes
    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Stroke color hex: ")
    bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
    bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])

    realtime_update = st.sidebar.checkbox("Update in realtime", True)

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


def get_labels(objects):
    labels = []
    for _ in range(len(objects)):
        label = st.text_input(f"Label for Box {_+1}")
        labels.append(label)
    return labels


if __name__ == '__main__':
    main()
