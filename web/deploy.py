# import subprocess
# import time
# from pyngrok import ngrok

# ngrok.set_auth_token('token')
# # Start Streamlit app
# streamlit_process = subprocess.Popen(['streamlit', 'run', 'system.py'])

# # Wait for the Streamlit app to start
# time.sleep(5)  # Adjust the delay based on your app's startup time


# # Connect to ngrok
# ngrok_tunnel = ngrok.connect(addr='8501', proto='http')

# try:
#     # Print the public URL
#     public_url = ngrok_tunnel.public_url
#     print("Your ngrok URL:", public_url)

#     # Keep the script running until interrupted
#     while True:
#         time.sleep(1)

# except KeyboardInterrupt:
#     # Terminate the Streamlit app and ngrok tunnel
#     streamlit_process.terminate()
#     ngrok.kill()
