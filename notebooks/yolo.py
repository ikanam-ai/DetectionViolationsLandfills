import streamlit as st
from deta import Deta
import time

# Initialize Deta
deta = Deta('c0dahqob3d5_3pz1eEuAyAQwE4P1waUJwr4cr2anHzp8')
users_db = deta.Base('users')

import cv2
import numpy as np
import streamlit as st
import torch
from ultralytics import YOLO

# Function to perform object detection using YOLOv8
def perform_object_detection(image):
    # Load the pre-trained YOLOv8 model
    model = YOLO("yolov8n.pt")
    model.load_state_dict(torch.load(r'D:\repos\lct_2023\notebooks\best.pt'))

    # Convert the model to an OpenCV-compatible format
    net = cv2.dnn_DetectionModel()
    net.setInputSize(416, 416)
    net.setInputScale(1.0 / 255)
    net.setInputSwapRB(True)

    # Extract the output layer names
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Preprocess the image
    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Perform forward pass and get the output predictions
    outs = net.forward(output_layers)

    # Process the predictions
    class_ids = []
    confidences = []
    boxes = []
    (height, width, channels) = image.shape
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:  # Filter out weak predictions
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Calculate the top-left corner of the bounding box
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Store the class ID, confidence, and bounding box coordinates
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    return class_ids, confidences, boxes




# Registration page
def register():
    st.title('Registration')

    name = st.text_input('Name')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')

    if st.button('Register'):
        # Check if the user already exists
        existing_user = users_db.get(email)

        if existing_user is not None:
            st.error('User with the given email already exists')
        else:
            # Add the user to the database
            users_db.put({'name': name, 'email': email, 'password': password}, email)
            st.success('Registration successful!')

# Login page
def login():
    st.title('Login')

    email = st.text_input('Email')
    password = st.text_input('Password', type='password')

    # Main application code
    if st.button('Login'):
        # Retrieve the user from the database
        user = users_db.get(email)
        if user is not None and user['password'] == password:
            st.success('Logged in successfully!')
            
            # Upload the image
            image = st.file_uploader('Upload an image', type=['jpg', 'jpeg', 'png'])

            if image is not None:
                # Read the uploaded image
                img = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)

                # Perform object detection
                class_ids, confidences, boxes = perform_object_detection(img)

                # Draw bounding boxes on the image
                for i in range(len(boxes)):
                    x, y, w, h = boxes[i]
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Display the image with bounding boxes
                st.image(img, channels='BGR', caption='Object Detection Result')
        else:
            st.error('Invalid credentials')

# Main function
def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.selectbox('Select a page', ['Login', 'Register'])

    if page == 'Login':
        login()
    elif page == 'Register':
        register()

if __name__ == '__main__':
    main()
