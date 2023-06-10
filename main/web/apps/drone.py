# App for making stream from drone 
import streamlit as st
import cv2

def play_video(rtmp_url):
    cap = cv2.VideoCapture(rtmp_url)
    if not cap.isOpened():
        st.error("Ошибка при открытии ссылки.")
        return
    
    stframe = st.empty()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert the frame to RGB for Streamlit
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Display the frame in Streamlit
        stframe.image(frame)
    
    cap.release()

def app():
    st.title("RTMP-адрес для получения видеотрансляции")
    st.write("Введите адрес.")
    
    rtmp_url = st.text_input("RTMP-адрес")
    
    if rtmp_url:
        play_video(rtmp_url)

if __name__ == "__main__":
    main()
