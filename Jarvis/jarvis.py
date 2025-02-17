import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import pyjokes
import psutil

engine = pyttsx3.init()

def choose_voice(): 
    """Allows the user to select a Male or Female voice at startup using voice command."""
    voices = engine.getProperty('voices')

    speak("Would you like a male or female voice?")
    print("Listening for voice choice... (Say 'Male' or 'Female')")

    choice = takecommand()

    if choice:
        if "male" in choice:
            engine.setProperty('voice', voices[0].id)  # Male voice
            speak("You have selected the male voice.")
        elif "female" in choice:
            engine.setProperty('voice', voices[1].id)  # Female voice
            speak("You have selected the female voice.")
        else:
            speak("I couldn't understand your choice, using the default voice.")
    else:
        speak("No input detected, using the default voice.")

    engine.setProperty('rate', 150)  # Adjust speed
    engine.setProperty('volume', 1)  # Set volume to max

def speak(audio) -> None:
    """Speaks the given text."""
    engine.say(audio)
    engine.runAndWait()


def time() -> None:
    """Tells the current time."""
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak("The current time is")
    speak(current_time)
    print("The current time is", current_time)


def date() -> None:
    """Tells the current date."""
    now = datetime.datetime.now()
    speak("The current date is")
    speak(f"{now.day} {now.strftime('%B')} {now.year}")
    print(f"The current date is {now.day}/{now.month}/{now.year}")


def wishme() -> None:
    """Greets the user based on the time of day."""
    speak("Welcome back, Boss!")
    print("Welcome back, Boss!")

    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        speak("Good morning!")
        print("Good morning!")
    elif 12 <= hour < 16:
        speak("Good afternoon!")
        print("Good afternoon!")
    elif 16 <= hour < 24:
        speak("Good evening!")
        print("Good evening!")
    else:
        speak("Good night, see you tomorrow.")

    assistant_name = load_name()
    speak(f"{assistant_name} at your service. Please tell me how may I assist you.")
    print(f"{assistant_name} at your service. Please tell me how may I assist you.")


def screenshot() -> None:
    """Takes a screenshot and saves it."""
    img = pyautogui.screenshot()
    img_path = os.path.expanduser("~\\Pictures\\screenshot.png")
    img.save(img_path)
    speak(f"Screenshot saved as {img_path}.")
    print(f"Screenshot saved as {img_path}.")

def takecommand() -> str:
    """Takes microphone input from the user and returns it as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1

        try:
            audio = r.listen(source, timeout=5)  # Listen with a timeout
        except sr.WaitTimeoutError:
            speak("Timeout occurred. Please try again.")
            return None

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(query)
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return None
    except Exception as e:
        speak(f"An error occurred: {e}")
        print(f"Error: {e}")
        return None

def play_music(song_name=None) -> None:
    """Plays music from the user's Music directory."""
    song_dir = os.path.expanduser("~\\Music")
    songs = os.listdir(song_dir)

    if song_name:
        songs = [song for song in songs if song_name.lower() in song.lower()]

    if songs:
        song = random.choice(songs)
        os.startfile(os.path.join(song_dir, song))
        speak(f"Playing {song}.")
        print(f"Playing {song}.")
    else:
        speak("No song found.")
        print("No song found.")

def set_name() -> None:
    """Sets a new name for the assistant."""
    speak("What would you like to name me?")
    name = takecommand()
    if name:
        with open("assistant_name.txt", "w") as file:
            file.write(name)
        speak(f"Alright, I will be called {name} from now on.")
    else:
        speak("Sorry, I couldn't catch that.")

def load_name() -> str:
    """Loads the assistant's name from a file, or uses a default name."""
    try:
        with open("assistant_name.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Jarvis"  # Default name


def search_wikipedia(query):
    """Searches Wikipedia and returns a summary."""
    try:
        speak("Searching Wikipedia...")
        result = wikipedia.summary(query, sentences=2)
        speak(result)
        print(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple results found. Please be more specific.")
    except Exception:
        speak("I couldn't find anything on Wikipedia.")


if __name__ == "__main__":
    choose_voice()  # Added voice selection at the start
    wishme()

    while True:
        query = takecommand()
        if not query:
            continue

        if "time" in query:
            time()
            
        elif "date" in query:
            date()

        elif "wikipedia" in query:
            query = query.replace("wikipedia", "").strip()
            search_wikipedia(query)

        elif "play music" in query:
            song_name = query.replace("play music", "").strip()
            play_music(song_name)

        elif "open youtube" in query:
            wb.open("youtube.com")
            
        elif "open google" in query:
            wb.open("google.com")

        elif "change your name" in query:
            set_name()

        elif "screenshot" in query:
            screenshot()
            speak("I've taken a screenshot, please check it.")

        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)
            print(joke)

        elif "shutdown" in query:
            speak("Shutting down the system, goodbye!")
            os.system("shutdown /s /f /t 1")
            break
            
        elif "restart" in query:
            speak("Restarting the system, please wait!")
            os.system("shutdown /r /f /t 1")
            break
            
        elif "offline" in query or "exit" in query:
            speak("Going offline. Have a good day!")
            break

        elif "open" in query:
            query = query.replace("open", "").strip()
            site_url = f"https://{query}.com"
            speak(f"Opening {query}")
            wb.open(site_url)
        
        elif "tell me about voice assistant" in query:
            speak("A voice assistant is an AI-powered software that can perform tasks or answer questions based on voice commands.")
            print("A voice assistant is an AI-powered software that can perform tasks or answer questions based on voice commands.")

        elif "what is your name" in query:
            assistant_name = load_name()
            speak(f"My name is {assistant_name}.")
            print(f"My name is {assistant_name}.")
        
        elif "who is" in query:
            person = query.replace("who is", "").strip()
            if person:
                try:
                    speak(f"Searching for {person}...")
                    result = wikipedia.summary(person, sentences=1)
                    speak(result)
                    print(result)
                except wikipedia.exceptions.DisambiguationError:
                    speak(f"There are multiple results for {person}. Please be more specific.")
                except wikipedia.exceptions.PageError:
                    speak(f"Sorry, I couldn't find any information on {person}.")
                except Exception:
                    speak("I encountered an error while searching.")
            else:
                speak("Please specify a name after 'who is'.")
        
        elif "open" in query:
            app_name = query.replace("open", "").strip().lower()
    
            app_paths = {
               "notepad": "C:\\Windows\\System32\\notepad.exe",
               "calculator": "C:\\Windows\\System32\\calc.exe",
               "command prompt": "C:\\Windows\\System32\\cmd.exe",
               "whatsapp": "C:\\Users\\UMAR\\AppData\\Local\\WhatsApp\\WhatsApp.exe",  # Update path
               "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
               "vs code": "C:\\Users\\UMAR\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",  # Update path
               "spotify": "C:\\Users\\UMAR\\AppData\\Roaming\\Spotify\\Spotify.exe",  # Update path
            # Add more applications with correct paths
            }

            if app_name in app_paths:
              speak(f"Opening {app_name}...")
              os.startfile(app_paths[app_name])
            else:
              speak(f"Sorry, I don't have the path for {app_name}. Please add it manually.")
            
        elif "battery" in query or "power status" in query:
    
         battery = psutil.sensors_battery()
         percent = battery.percent

         speak(f"Your system battery is at {percent} percent.")
         print(f"Battery Percentage: {percent}%")




