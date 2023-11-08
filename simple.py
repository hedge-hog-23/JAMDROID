import speech_recognition as sr
from gtts import gTTS
import webbrowser

# Initialize the recognizer
recognizer = sr.Recognizer()

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    webbrowser.open("response.mp3")

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
            search_url = f"https://www.google.com/search?q={query}"
            webbrowser.open(search_url)
        else:
            speak("I'm sorry, I don't understand that command.")

if __name__ == "__main__":
    main()
