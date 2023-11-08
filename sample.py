import speech_recognition as sr
import pyttsx3
from googlesearch import search
import requests
from bs4 import BeautifulSoup

# Initialize the recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand your command.")
        return ""
    except sr.RequestError:
        print("I'm sorry, I'm having trouble connecting to the internet.")
        return ""

def search(query):
    try:
        search_results = list(search(query, num=1, stop=1, pause=2))
        if search_results:
            url = search_results[0]
            page = requests.get(url)
            page.raise_for_status()  # Check for HTTP request errors
            soup = BeautifulSoup(page.content, 'html.parser')
            paragraphs = soup.find_all('p')
            text = ' '.join(p.text for p in paragraphs)
            if text:
                speak(text)
            else:
                speak("I couldn't find any readable content for that search result.")
        else:
            speak("I couldn't find any search results for that query.")
    except requests.exceptions.RequestException as e:
        speak("There was an issue with the web request. Please check your internet connection.")
    except Exception as e:
        speak("I encountered an error while performing the search.")

def main():
    speak("Hello, I am your desktop assistant. How can I assist you today?")

    while True:
        command = listen()

        if "hello" in command:
            speak("Hello! How can I help you?")
        elif "bye" in command:
            speak("Goodbye!")
            speak("Sure! Reach me if you need stuff!")
            break
        elif "search" in command:
            query = command.split("search", 1)[-1].strip()
            search(query)
        else:
            speak("I'm sorry, I don't understand that command.")

if __name__ == "__main__":
    main()
