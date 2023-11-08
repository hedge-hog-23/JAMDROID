import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak something:")
    audio_data = recognizer.listen(source)
try:
    text = recognizer.recognize_google(audio_data)
    print("You said: " + text)
except sr.UnknownValueError:
    print("Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
