from ultralytics import YOLO
import cv2
import random
import numpy as np
import streamlit as st

full_labels = ['Веса автомобилей',
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
               'Портативное сетчатое ограждение']

def generate_random_color():
    # Generate random RGB values
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (b, g, r)


label_colors = {}

i = 0
for label in full_labels:
    color = generate_random_color()
    label_colors[label] = color
    i += 1

model = YOLO("models/best.pt")

def get_predict(file_name, model=model, CONFIDENCE_THRESHOLD=0.15, path_save='runs/detect'):
    frame = cv2.imread(file_name)
    detections = model(frame)[0]
    for data in detections.boxes.data.tolist():
        confidence = data[4]

        label = full_labels[int(data[5])]
        color = label_colors[label]
        if float(confidence) < CONFIDENCE_THRESHOLD:
            continue
        xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])

        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
        cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # Save the file
    file_path = f"{path_save}/{file_name}"
    cv2.imwrite(file_path, frame)

    # Save the label coordinates mask
    mask_data = np.array([[xmin, ymin, xmax, ymax, label, confidence] for data in detections.boxes.data.tolist() if float(data[4]) >= CONFIDENCE_THRESHOLD])
    mask_file_path = f"{path_save}/mask_{file_name}.txt"
    np.savetxt(mask_file_path, mask_data, fmt='%d,%d,%d,%d,%s,%f')

    return file_path, mask_file_path


def apply_labels_to_image(file_name, mask_file_path):
    # Load the image
    image = cv2.imread(file_name)

    # Load the label coordinates mask
    mask_data = np.loadtxt(mask_file_path, delimiter=',', dtype=str)

    for data in mask_data:
        xmin, ymin, xmax, ymax, label, confidence = map(int, data[:4]), data[4], float(data[5])
        color = label_colors[label]

        # Draw rectangle and label
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)
        cv2.putText(image, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    return image


# Streamlit app
def main():
    st.title("Object Detection with Streamlit")

    # File uploader
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display uploaded image
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)
        st.image(image, channels="BGR")

        # Apply object detection
        file_path, mask_file_path = get_predict(uploaded_file.name)
        predicted_image = cv2.imread(file_path)
        st.image(predicted_image, channels="BGR")

        # Apply labels to the image
        labeled_image = apply_labels_to_image(uploaded_file.name, mask_file_path)
        st.image(labeled_image, channels="BGR")


if __name__ == "__main__":
    main()