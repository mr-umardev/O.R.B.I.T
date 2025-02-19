import streamlit as st
import subprocess
import sys
import os
import time
import base64
import psutil
import threading
from gtts import gTTS
import tempfile

def get_base64_video(video_path):
    """Converts video file to base64 for embedding."""
    with open(video_path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode()

def set_background_video(video_name):
    """Sets the background video using base64 encoded video."""
    video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), video_name)
    if os.path.exists(video_path):
        video_base64 = get_base64_video(video_path)
        st.markdown(
            f"""
            <style>
                .stApp {{
                    background: none;
                }}
                .main {{
                    background: none !important;
                }}
                video.background-video {{
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    min-width: 100%;
                    min-height: 100%;
                    width: auto;
                    height: auto;
                    z-index: -1;
                }}
            </style>
            <video class="background-video" autoplay muted playsinline loop>
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            </video>
            """,
            unsafe_allow_html=True
        )

def change_title_color():
    """Changes the color of the title every 1 second."""
    colors = ["#FF5733", "#33FF57", "#3357FF", "#F733FF", "#FF5733"]
    st.markdown(
        f"""
        <script>
            var colors = {colors};
            var index = 0;
            function changeColor() {{
                document.getElementById("jarvis_title").style.color = colors[index];
                index = (index + 1) % colors.length;
            }}
            setInterval(changeColor, 1000);
        </script>
        """,
        unsafe_allow_html=True
    )

def add_header_navbar_footer():
    """Adds a custom header, navbar, footer."""
    st.markdown(
        """
        <style>
            .header {
                font-size: 30px;
                font-weight: bold;
                padding: 10px;
                background-color: #282828;
                color: white;
                text-align: left;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                z-index: 999;
            }
            .navbar {
                font-size: 18px;
                padding: 10px;
                background-color: #333333;
                color: white;
                display: flex;
                gap: 20px;
                position: fixed;
                top: 60px;
                left: 0;
                right: 0;
                z-index: 998;
            }
            .navbar a {
                color: white;
                text-decoration: none;
                padding: 5px 10px;
            }
            .footer {
                font-size: 14px;
                text-align: center;
                padding: 10px;
                background-color: #282828;
                color: white;
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                z-index: 999;
            }
            .stApp {
                margin-top: 120px;
                margin-bottom: 40px;
            }
        </style>
        <div class="navbar">
            <a href="#">Home</a>
            <a href="#">Features</a>
            <a href="#">About</a>
            <a href="#">Contact</a>
        </div>
        <div class="footer">© 2025 Jarvis AI By mr-umardev. All rights reserved.</div>
        """,
        unsafe_allow_html=True
    )

def is_jarvis_running():
    """Check if jarvis.py is already running."""
    for process in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        if process.info['cmdline'] and "jarvis.py" in " ".join(process.info['cmdline']):
            return True
    return False

def run_jarvis():
    """Function to run Jarvis in a separate process."""
    jarvis_path = os.path.join(os.path.dirname(__file__), "jarvis.py")
    python_exec = sys.executable
    if os.path.exists(jarvis_path):
        # Launch jarvis.py as a background subprocess
        subprocess.Popen([python_exec, jarvis_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        st.error(f"Jarvis.py not found at: {jarvis_path}")

def speak(text):
    """Uses gTTS to generate and play speech in the browser."""
    tts = gTTS(text=text, lang='en')
    
    # Save the speech to a temporary file and play it via Streamlit
    with tempfile.NamedTemporaryFile(delete=True) as temp_audio:
        tts.save(temp_audio.name)
        st.audio(temp_audio.name, format="audio/mp3")

# Page state management
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# Loading page before starting Jarvis
if st.session_state["page"] == "loading_video":
    set_background_video("IronStartUp.mp4")
    st.write("**Starting Jarvis... Please Wait...**")
    time.sleep(2)  # Shorter wait time

    # Run Jarvis in the background
    with st.spinner('Starting Jarvis...'):
        run_jarvis()

    # Use a background thread to handle speech
    threading.Thread(target=speak, args=("Jarvis is now active, ready for your commands.",)).start()

    # Change to the jarvis page
    st.session_state["page"] = "jarvis_page"

# Jarvis running page
elif st.session_state["page"] == "jarvis_page":
    # Play the sequence of videos one after the other
    set_background_video("IronStartUp.mp4")
    st.title("Jarvis is Running...")
    st.write("You can now use voice commands.")
    time.sleep(30)  # Duration of IronStartUp.mp4

    set_background_video("TechIron.mp4")
    time.sleep(30)  # Duration of TechIron.mp4

    set_background_video("Hologram.mp4")
    time.sleep(30)  # Duration of Hologram.mp4

    # Continue to display content
    if st.button("Back to Home"):
        st.session_state["page"] = "home"

# Home page
else:
    set_background_video("IronStartUp.mp4")
    change_title_color()
    add_header_navbar_footer()

    st.markdown('<h1 id="jarvis_title"><span style="font-style: italic;">Welcome to </span><span style="color: #FFD700; font-style: italic;">Jarvis AI</span></h1>', unsafe_allow_html=True)
    st.write("Click the button below to activate Jarvis.")

    if st.button("Run Jarvis"):
        st.session_state["page"] = "loading_video"
