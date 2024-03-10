import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import datetime
import os
import pywhatkit
import smtplib
import json  # For reading configuration file

# Configuration file
CONFIG_FILE = "config.json"

def load_config():
    """Loads configuration from JSON file."""
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        print("Config file not found. Using default configurations.")
        return {}

def save_config(config):
    """Saves configuration to JSON file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def listen():
    """Records audio from microphone and returns recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="en-US")
        print("You said: " + text)
        return text.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

def speak(text):
    """Speaks text using pyttsx3."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def respond(text, config):
    """Handles various commands based on user input and configuration."""
    if "wikipedia" in text:
        search_term = text.split("wikipedia")[1].strip()
        speak("Searching Wikipedia for " + search_term)
        results = wikipedia.summary(search_term, sentences=2)
        speak(results)
    elif "open youtube" in text:
        video_to_open = text.split("open youtube")[1].strip()
        speak("Opening " + video_to_open + " on YouTube")
        webbrowser.open("https://www.youtube.com/results?search_query=" + video_to_open)
    elif "what time is it" in text:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak("The current time is " + current_time)
    elif "open" in text:  # Open applications
        app_name = text.split("open")[1].strip()
        if app_name in config["applications"]:
            os.system(config["applications"][app_name])
            speak("Opening " + app_name)
        else:
            speak("Application not found in configuration.")
    elif "send email" in text:
        try:
            sender_email = config["email"]["sender_email"]
            sender_password = config["email"]["sender_password"]
            recipient_email = config["email"]["recipient_email"]
            subject = text.split("send email")[1].strip().split("subject")[0].strip()
            message = text.split("send email")[1].strip().split("subject")[1].strip()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, f"Subject: {subject}\n\n{message}")
            speak("Email sent successfully.")
        except Exception as e:
            print("Error sending email:", e)
            speak("Failed to send email. Please check configuration.")
    elif "weather" in text:
        try:
            if "current" in text:
                weather_type = "current"
            elif "tomorrow" in text:
                weather_type = "tomorrow"
            else:
                weather_type = None
            if weather_type and "in" in text:
                location = text.split("weather in")[1].strip()
                weather_info = get_weather(location, weather_type, config)
                if weather_info:
                    speak(weather_info)
                else:
                    speak("Weather information not available.")
            else:
                speak("Please specify location and weather type (current or tomorrow).")
        except Exception as e
