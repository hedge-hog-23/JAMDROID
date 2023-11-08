import pyttsx3
import speech_recognition as sr
import os
import webbrowser
import smtplib
import requests
import time
import pytz
import schedule

    # Initialize the text-to-speech engine
engine = pyttsx3.init()

    # Initialize the speech recognition engine
recognizer = sr.Recognizer()

    # Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

    # Function to open applications
def open_application(application_name):
        if "notepad" in application_name:
            os.system("notepad.exe")
        elif "chrome" in application_name:
            os.system("chrome.exe")
        elif "gcr" in application_name:
            os.system("classroom.exe")

    # Function to perform web search
def search(query):
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)

    # Function to get weather information
def get_weather(city):
        api_key = "YOUR_WEATHER_API_KEY"  # Replace with your actual API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            weather_desc = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            speak(f"The weather in {city} is {weather_desc} with a temperature of {temperature} Kelvin.")
        else:
            speak("Sorry, I couldn't retrieve the weather information at the moment.")

    # Function to set reminders
def set_reminder(reminder_text, time_str):
        # Function to execute the reminder action
        def reminder_action():
            speak("Reminder: " + reminder_text)

        # Convert the time input (e.g., "5 PM") to a datetime
        try:
            reminder_time = time_str.strip()
            # Schedule the reminder
            schedule.every().day.at(reminder_time).do(reminder_action)
            speak(f"Reminder set for {reminder_time}")
        except ValueError:
            speak("Sorry, I couldn't understand the time.")

    # Function to send an email
def send_email(receiver, subject, message):
        # Configure your email server settings
        smtp_server = "smtp.gmail.com"  # Replace with your SMTP server
        smtp_port = 587  # Replace with the SMTP port (587 for TLS, 465 for SSL, or 25 for non-secure)
        smtp_username = "210701238@rajalakshmi.edu.in"  # Replace with your email address
        smtp_password = "CSE@210710238"  # Replace with your email password

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Use TLS for secure connection
            server.login(smtp_username, smtp_password)

            # Create the email message
            email_message = f"Subject: {subject}\n\n{message}"

            # Send the email
            server.sendmail(smtp_username, receiver, email_message)
            server.quit()

            speak("Email sent successfully.")
        except Exception as e:
            speak(f"Email could not be sent. Error: {str(e)}")


    # Main loop for the desktop assistant
while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source)
            print("Recognizing...")
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)

            if "open" in command:
                app_name = command.split("open", 1)[1].strip()
                open_application(app_name)
            elif "search" in command:
                search_query = command.split("search", 1)[1].strip()
                search(search_query)
            elif "weather" in command:
                city = command.split("weather", 1)[1].strip()
                get_weather(city)
            elif "set reminder" in command:
                reminder_text = command.split("set reminder", 1)[1].strip()
                speak("When should I remind you?")
                with sr.Microphone() as source:
                    audio = recognizer.listen(source)
                time = recognizer.recognize_google(audio).lower()
                set_reminder(reminder_text, time)
                speak("Reminder set successfully.")
            elif "send email" in command:
                speak("Whom do you want to send the email to?")
                with sr.Microphone() as source:
                    audio = recognizer.listen(source)
                receiver = recognizer.recognize_google(audio).lower()
                speak("What's the subject of the email?")
                with sr.Microphone() as source:
                    audio = recognizer.listen(source)
                subject = recognizer.recognize_google(audio).lower()
                speak("Please dictate the email message.")
                with sr.Microphone() as source:
                    audio = recognizer.listen(source)
                message = recognizer.recognize_google(audio).lower()
                send_email(receiver, subject, message)
                speak("Email sent successfully.")
            elif "exit" in command:
                speak("Goodbye!")
                break
            else:
                speak("I'm sorry, I don't understand that command.")

        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand your request.")
        except sr.RequestError:
            speak("Sorry, there was an issue with the speech recognition service.")
        except Exception as e:
            speak(f"An error occurred: {str(e)}")
