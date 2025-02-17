import streamlit as st
import subprocess
import sys
import os
import time
import base64
import psutil

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
            <video class="background-video" autoplay muted playsinline>
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
        <div class="header">Jarvis AI - Powered by Streamlit</div>
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

# Page state management
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# Loading page before starting Jarvis
if st.session_state["page"] == "loading_video":
    set_background_video("IronStartUp.mp4")
    st.write("**Starting Jarvis... Please Wait...**")
    time.sleep(5)  # Reduced waiting time

    # Correct path to jarvis.py
    jarvis_path = os.path.join(os.path.dirname(__file__), "jarvis.py")
    python_exec = sys.executable

    # Check if jarvis.py exists before running
    if os.path.exists(jarvis_path):
        if not is_jarvis_running():
            subprocess.Popen(
                [python_exec, jarvis_path],  
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                shell=True
            )
            st.session_state["page"] = "jarvis_page"
            st.rerun()
        else:
            st.warning("Jarvis is already running.")
            st.session_state["page"] = "jarvis_page"
            st.rerun()
    else:
        st.error(f"Jarvis.py not found at: {jarvis_path}")
        st.session_state["page"] = "home"

# Jarvis running page
elif st.session_state["page"] == "jarvis_page":
    # Loop the background video sequence
    while True:
        set_background_video("IronStartUp.mp4")
        st.title("Jarvis is Running...")
        st.write("You can now use voice commands.")

        # Play the next video after a delay
        time.sleep(30)  # Duration of first video
        set_background_video("TechIron.mp4")

        # Play the next video after a delay
        time.sleep(30)  # Duration of second video
        set_background_video("Hologram.mp4")

        # Continue looping the sequence
        time.sleep(30)  # Duration of third video

        if st.button("Back to Home"):
            st.session_state["page"] = "home"
            st.rerun()

# Home page
else:
    set_background_video("IronStartUp.mp4")
    change_title_color()
    add_header_navbar_footer()

    st.markdown('<h1 id="jarvis_title"><span style="font-style: italic;">Welcome to </span><span style="color: #FFD700; font-style: italic;">Jarvis AI</span></h1>', unsafe_allow_html=True)
    st.write("Click the button below to activate Jarvis.")

    if st.button("Run Jarvis"):
        st.session_state["page"] = "loading_video"
        st.rerun()
