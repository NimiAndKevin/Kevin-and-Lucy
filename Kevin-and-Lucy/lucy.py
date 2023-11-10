import sounddevice as sd
import numpy as np
import openai
import speech_recognition as sr
import pyttsx3
from bs4 import BeautifulSoup

# Set up OpenAI API key
openai.api_key = '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'

# Text-to-speech setup
tts_engine = pyttsx3.init()

def text_to_speech(text):
    # You can adjust the voice parameters as needed
    voice = tts_engine.getProperty('voices')[1]  
    tts_engine.setProperty('voice', voice.id)
    tts_engine.setProperty('rate', 150)  
    tts_engine.say(text)
    tts_engine.runAndWait()

# Speech recognition setup
recognizer = sr.Recognizer()

def listen_for_voice():
    with sr.Microphone() as source:
        print("Lucy: Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio).strip()
        print(f"You: {user_input}")
        return user_input
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand what you said."
    except sr.RequestError as e:
        return f"Error: {str(e)}"

def process_user_input(user_input):
    if "sleep" in user_input:
        text_to_speech("Please Clap to Use Me")
        def detect_clap(indata, frames, time, status):
            if np.max(indata) > 0.5:
                print("Clap detected!")
        duration = 10  # Adjust as needed
        sample_rate = 44100  # Adjust as needed
        with sd.InputStream(callback=detect_clap, channels=1, samplerate=sample_rate):
            sd.sleep(int(duration * 1000))
            text_to_speech("Hello i'm Lucy Nimi's Female ChatGPT Voice Assistant! Ask me any question and i will answer it")
    elif "what is the weather" in user_input:
        search = "temperature in langley"
        url = f"https://www.google.com/search?q={search}"
        r  = requests.get(url)
        data = BeautifulSoup(r.text,"html.parser")
        temp = data.find("div", class_ = "BNeawe").text
        text_to_speech(f"current{search} is {temp}")
    elif "location" in command:
        My_Location()

def My_Location():

    ip_add = requests.get('https://api.ipify.org').text
    url ='https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'
    geo_q = requests.get(url)
    geo_d =geo_q.json()
    state = geo_d['city']
    country =geo_d['country']
    speak_properly(f"you are now in {state, country}")

# Function to detect claps
def detect_clap(indata, frames, time, status):
    if np.max(indata) > 0.5:
        print("Clap detected!")

def chat_with_gpt3(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1500,
        )
        reply = response['choices'][0]['text'].strip()
        return reply
    except Exception as e:
        return str(e)

text_to_speech("Please Clap to Use Me")

# Set the audio input parameters
duration = 10  # Adjust as needed
sample_rate = 44100  # Adjust as needed

with sd.InputStream(callback=detect_clap, channels=1, samplerate=sample_rate):
        sd.sleep(int(duration * 1000))
        text_to_speech("Hello i'm Lucy Nimi's Female ChatGPT Voice Assistant! Ask me any question and i will answer it")
    
while True:
    
    user_input = listen_for_voice()
    process_user_input(user_input)

    conversation_history = f"You: {user_input}\nLucy"
    response = chat_with_gpt3(conversation_history)
    print(f"Lucy: {response}")
    text_to_speech(response)