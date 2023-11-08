import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")

# Text you want to read aloud in real-time
text_to_read = "purla alu bye"
engine.setProperty('rate', 150)  # Speed of speech (words per minute)
engine.setProperty('volume', 1.0) 
# Convert and read the text with the Zira voice
engine.say(text_to_read)

# Wait for the speech to finish
engine.runAndWait()
