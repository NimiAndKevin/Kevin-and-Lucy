import sounddevice as sd
import numpy as np
import geocoder
import openai
import cv2
import pyautogui
from textblob import TextBlob
from PyDictionary import PyDictionary
from googletrans import Translator
import pyttsx3
import speech_recognition as sr
import webbrowser
import wikipedia
import requests
import json
import random
import wolframalpha
import datetime
import pywhatkit
import threading
import subprocess
import os
import psutil
import shutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Key,Controller
from time import sleep
from bs4 import BeautifulSoup

sample_rate = 44100
duration = 5.0
buffer = np.zeros(int(sample_rate * duration), dtype=np.float32)

# Define your wake word
wake_word = "Kevin"

# Dictionary to store projects and tasks
projects = {}

# Initialize text-to-speech engine
engine = pyttsx3.init()

GOOGLE_MAPS_API_KEY = "AIzaSyB7GpKPU4rNm78YOvhPXBQ-i6GPDpfxsGs" 

dictapp = {"commandprompt":"cmd","paint":"paint","word":"winword","excel":"excel","chrome":"chrome","vscode":"code","powerpoint":"powerpnt"}

# Set up OpenAI API key
openai.api_key = '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'

keyboard = Controller()

# Initialize the translator
translator = Translator()

# Initialize PyDictionary
dictionary = PyDictionary()

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Define a variable to store the current status
user_status = "I'm doing well."

# Function to process audio data
def process_audio(indata, frames, time, status):
    if status:
        print(f"Error in audio input: {status}")
    if any(indata):
        buffer[:frames] = indata

# Function to speak a given text
def speak_properly(text):
    voice = engine.getProperty('voices')[0]  
    engine.setProperty('voice', voice.id)
    engine.setProperty('rate', 150)  
    engine.say(text)
    engine.runAndWait()

# Function to listen for a voice command
def listen_for_command():
    with sr.Microphone() as source:
        global recognized_command
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        speak_properly("I didn't catch that. Can you please repeat?")
        return listen_for_command()
    except sr.RequestError:
        speak("I couldn't request results. Please check your internet connection.")

# Function to process voice commands
def process_command(command):
    current_time = datetime.datetime.now()
    if "hello" in command:
        speak_properly("Hello! How can I assist you today?")
    elif "latest news" in command:
            get_latest_news()
    elif "blood" in command or "vitals" in command:
            vitals = monitor_vitals()
            speak_properly("Here are your vitals:")
            print(vitals)
            speak_properly(vitals)
    elif "full screen a video on YouTube" in command:
        full_screen_youtube_video()
        speak_properly("The YouTube video has been set to full screen")
    elif "remember that" in command:
        rememberMessage = command.replace("remember that","")
        rememberMessage = command.replace("kevin remind me","")
        speak_properly("You told me to remember that"+rememberMessage)
        remember = open("Remember.txt","a")
        remember.write(rememberMessage)
        remember.close()
    elif "what do you remember" in command:
        remember = open("Remember.txt","r")
        speak_properly("You told me to remember that" + remember.read())
    elif "open" in command:
        query = command.replace("open","")
        query = command.replace("jarvis","")
        pyautogui.press("super")
        pyautogui.typewrite(query)
        pyautogui.sleep(2)
        pyautogui.press("enter")
        speak_properly("Opened The App you desired {username}")
    elif "close" in command:
        speak_properly("Closing,sir")
        keys = list(dictapp.keys())
        for app in keys:
            if app in command:
                os.system(f"taskkill /f /im {dictapp[app]}.exe")
    elif "undo"in command:
        pyautogui.hotkey('ctrl', 'z')
    elif "open website" in command:
        url = command.replace("open website", "").strip()
        open_website(url)
        speak_properly(f"Opening {url}")
    elif "refresh page" in command:
        refresh_page()
        speak_properly("Refreshing the page.")
    elif "close browser" in command:
        close_browser()
        speak_properly("Closing the browser.")
    elif "turn up the volume" in command:
        volumeup()
    elif "turn down the volume" in command:
        volumedown()
    elif "scroll down" in command:
        scroll_down()
        speak_properly("Scrolling down the page.")
    elif "scroll up" in command:
        scroll_up()
        speak_properly("Scrolling up the page.")
    elif "play" in command:
        query=command.replace('play' , '')
        speak_properly(f'Playing {query}')
        pywhatkit.playonyt(query)
    elif "go back" in command or "buddy go back" in command:
        speak_properly("going back Sir")
        go_back()
    elif "forward" in command or "go forward buddy" in command:
        speak_properly("going forward Sir")
        go_forward()
    elif "schedule my day" in command:
        tasks = [] #Empty list 
        speak_properly("Do you want to clear old tasks (Plz speak YES or NO)")
        if "yes" in command:
            file = open("tasks.txt","w")
            file.write(f"")
            file.close()
            no_tasks = int(input("Enter the no. of tasks :- "))
            i = 0
            for i in range(no_tasks):
                tasks.append(input("Enter the task :- "))
                file = open("tasks.txt","a")
                file.write(f"{i}. {tasks[i]}\n")
                file.close()
        elif "no" in command:
            i = 0
            no_tasks = int(input("Enter the no. of tasks :- "))
            for i in range(no_tasks):
                tasks.append(input("Enter the task :- "))
                file = open("tasks.txt","a")
                file.write(f"{i}. {tasks[i]}\n")
                file.close()
    elif "show my schedule" in command:
        file = open("tasks.txt","r")
        content = file.read()
        file.close()
        mixer.init()
        mixer.music.load("notification.mp3")
        mixer.music.play()
        notification.notify(
            title = "My schedule :-",
            message = content,
            timeout = 15
            )
    elif "temperature" in command:
        search = "temperature in langley"
        url = f"https://www.google.com/search?q={search}"
        r  = requests.get(url)
        data = BeautifulSoup(r.text,"html.parser")
        temp = data.find("div", class_ = "BNeawe").text
        print(f"current{search} is {temp}")
        speak_properly(f"current{search} is {temp}")
    elif "weather" in command:
        search = "temperature in langley"
        url = f"https://www.google.com/search?q={search}"
        r  = requests.get(url)
        data = BeautifulSoup(r.text,"html.parser")
        temp = data.find("div", class_ = "BNeawe").text
        print(f"current{search} is {temp}")
        speak_properly(f"current{search} is {temp}")
    elif "screenshot" in command:
        im = pyautogui.screenshot()
        im.save("ss.jpg")
        speak_properly("Image saved Sir")
    elif "one tab" in command or "1 tab" in command:
        pyautogui.hotkey("ctrl","w")
        speak_properly("All tabs closed")
    elif "two tabs" in command:
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        speak_properly("All tabs closed")
    elif "three tabs" in command:
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        speak_properly("All tabs closed")
        
    elif "four tabs" in command:
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        speak_properly("All tabs closed")
    elif "five tabs" in command:
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        speak_properly("All tabs closed")
    elif "pause" in command:
        pyautogui.press("k")
        speak_properly("video paused")
    elif "unpause video" in command:
        pyautogui.press("k")
        speak_properly("video played")
    elif "mute" in command:
        pyautogui.press("m")
        speak_properly("video muted")
    elif "type" in command:
        speak_properly("Please tell me what i should write")
        while True:
            typeQuery = command
            if typeQuery == "exit typing":
                speak_properly("Done Sir")
                break
            else:
                pyautogui.write(typeQuery)
    elif "minimize" in command:
        speak_properly("Minimizing Window Sir")
        minimize_window()
    elif "open Blender" in command:
        os.system("blender")  # This command opens Blender
        speak_properly("Blender is now open.")
    elif "maximize" in command:
        speak_properly("Maximizing Window Sir")
        pyautogui.hotkey('win', 'up','up')
    elif "close the application" in command:
        speak_properly("Closing Application Sir")
        pyautogui.hotkey('ctrl', 'w')
    
    elif "save it" in command:
        speak_properly("Saving File Sir")
        pyautogui.hotkey('ctrl', 's')
    elif "paste" in command:
        speak_properly("Pasting Text Sir")
        pyautogui.hotkey('ctrl', 'v')
    elif "open my blender files" in command:
        speak_properly("Opening your blender files")
        os.startfile("C:\\Users\\surface\\Desktop\\blender")
    elif "what can you do" in command:
            describe_capabilities()
    elif "kevin" in command:
        speak_properly("Yes sir")
    elif "location" in command:
        My_Location()
    elif "thanks buddy" in command or "cool" in command or "awesome" in command:
        speak_properly("{username} You are Welcome")
    elif "merry christmas" in command:
        speak_properly("Merry christmas to you and everyone Sir, Christmas is such a happy holiday and im happy to be in it")
    elif "i'm fine" in command:
        speak_properly(f"Happy to hear that {username}")
    elif "i'm not fine" in command:
        speak_properly(f"sad to hear about that {username}")
    elif "who are you" in command:
            introduce()
    elif "retrieve data" in command:
        speak("Sure, please specify the data you want to retrieve.")
        data_query = listen_for_command()
        result = retrieve_data_from_internet(data_query)
        speak("Here's the retrieved data:")
        speak(result)
    elif "happy halloween" in command:
        speak_properly("{username} i don't like hallowen its so scary")
    elif "create project" in command:
        project_name = command.split("create project", 1)[1].strip()
        projects[project_name] = []
        speak_properly(f"Project '{project_name}' created.")
    elif "exit" in command:
        speak_properly("Goodbye! {nimi} please input your username and password to use me again do any username")
    elif "add task" in command:
        parts = command.split("add task", 1)
        project_name = parts[0].strip()
        task = parts[1].strip()
        add_task(project_name, task)
        speak_properly(f"Task added to '{project_name}': {task}")

    elif "list tasks" in command:
        project_name = command.split("list tasks", 1)[1].strip()
        list_tasks(project_name)

    elif "complete task" in command:
        parts = command.split("complete task", 1)
        project_name = parts[0].strip()
        task_index = int(parts[1].strip())
        complete_task(project_name, task_index)
    elif "count people" in command:
            people_count = count_people_in_environment()
            speak_properly(people_count)
    elif "wishme" in command:
        current_time = datetime.datetime.now().time()
        if current_time < datetime.time(12):
            speak_properly("Kevin: Good morning sir! How can I assist you today?")
        elif datetime.time(12) <= current_time < datetime.time(17):
            speak_properly("Kevin: Good afternoon Sir! How can I assist you today?")
        else:
            speak_properly("Kevin: Good evening sir! How can I assist you today?")
    elif "detect emotions" in command:
            speak("Please speak, and I will analyze your emotions.")
            recorded_command = listen_for_command()
            emotion_response = analyze_emotions(recorded_command)
            speak_properly(emotion_response)
    elif"set my status to" in command:
        new_status = command.split("set my status to", 1)[1].strip()
        user_status = new_status
        speak_properly(f"Your status has been updated to: {new_status}")
    elif "open google" in command:
        speak_properly("Opening Google.")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in command:
        speak_properly("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
    elif "open firefox" in command:
        speak_properly("Opening FireFox")
        os.system("C:\\Users\\surface\\Desktop\\Others\\Firefox.lnk")
    elif "open roblox" in command:
        speak_properly("Opening Roblox.")
        webbrowser.open("https://www.roblox.com")
    elif "make a website" in command:
        speak_properly("Creating a website called Nimicodes.com.")
    elif "open prime video" in command:
        speak_properly("Opening Prime Video.")
        webbrowser.open("https://www.amazon.com/Prime-Video")
    elif "open netflix" in command:
        speak_properly("Opening Netflix.")
        webbrowser.open("https://www.netflix.com")
    elif "call" in command:
        speak_properly("Sure, whom do you want to call?")
        recipient_number = listen_for_command()
        call_on_whatsapp(recipient_number)
    elif "close file" in command:
        file_path = "C:\\Users\\surface\\Desktop\\blender"
        if close_file(file_path):
            speak_properly(f"The file {file_path} has been successfully closed.")
    elif "what's the time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak_properly(f"The current time is {current_time}.")
                
    elif "set an alarm" in command:
        speak_properly("Sure, please specify the time for the alarm in 24-hour format.")
        alarm_time = listen_for_command()
        try:
            alarm_hour, alarm_minute = map(int, alarm_time.split(":"))
            current_time = datetime.datetime.now()
            alarm_datetime = current_time.replace(hour=alarm_hour, minute=alarm_minute, second=0, microsecond=0)

            if alarm_datetime < current_time:
                alarm_datetime += datetime.timedelta(days=1)  # Set the alarm for the next day if specified time has already passed today

            time_difference = (alarm_datetime - current_time).total_seconds()
            threading.Timer(time_difference, trigger_alarm).start()
            speak_properly(f"Alarm set for {alarm_time}.")
        except ValueError:
            speak_properly("Sorry, I couldn't set the alarm. Please specify the time in the correct format.")
    elif "order pizza" in command:
        pizza_order = gather_pizza_order_details()
        api_key = ""  # Replace with your actual API key
        place_pizza_order(pizza_order, api_key)
        pizza_order = {}
        speak_properly("What type of pizza would you like to order?")
        pizza_order["type"] = listen_for_command()

        speak_properly("What size would you like (small, medium, large)?")
        pizza_order["size"] = listen_for_command()

        speak_properly("Please provide your delivery address.")
        pizza_order["address"] = listen_for_command()

        speak_properly("What is your preferred payment method?")
        pizza_order["payment"] = listen_for_command()

    elif "calculate" in command:
        WolfRamAlpha(query)
        query = command.replace("calculate","")
        Calc(query)
    elif "open notepad" in command:
        speak_properly("{username} Opening Notepad.")
        os.system("notepad")  # Open Notepad
    elif "open roblox" in command:
        speak_properly("Opening A game called Roblox {username}")
        os.system("roblox")
    elif "convert" in command:
        conversion_query = command.split("convert", 1)[1].strip()
        conversion_result = convert_units(conversion_query)
        if conversion_result:
            speak_properly(f"{username} the conversion result is: {conversion_result}")
        else:
            speak_properly("Sorry, I couldn't perform the conversion {username}.")
    elif "record a video" in command:
            speak_properly("{username} Starting video recording. To stop recording, say 'stop recording video'.")
            video_thread = threading.Thread(target=record_video)
            video_thread.start()
            video_thread.join()  # Wait for the video recording to finish
            speak_properly("{username} Video recording finished.")
    elif "stop recording" in command:
        cv2.destroyAllWindows()
        speak_properly("Closing Recording {username}")
    elif "i'm tired" in command or "i'm so tired" in command:
        speak_properly("let me Play your favourite songs, {username}")
        a = (1,2,3,4,5) # You can choose any number of songs (I have only choosen 3)
        b = random.choice(a)
        if b==1:
            webbrowser.open("https://www.youtube.com/watch?v=kTJczUoc26U")
        if b==2:
            webbrowser.open("https://www.youtube.com/watch?v=2526AXJAAuc")
        if b==3:
            webbrowser.open("https://www.youtube.com/watch?v=pAgnJDJN4VA")
        if b==4:
            webbrowser.open("https://www.youtube.com/watch?v=MyUzx-ez4kE")
        if b==5:
            webbrowser.open("https://www.youtube.com/watch?v=s7gef3SXSbY")
    elif "tell me a joke" in command:
        joke = get_random_joke()
        speak_properly("Here's a joke for you: " + joke)
    elif "tell me a riddle" in command:
        riddle = get_random_riddle()
        speak_properly("Here's a riddle for you: " + riddle)
    elif "open map" in command:
        speak_properly("Opening maps for you {username}.")
        os.system("start bingmaps:")
    elif "search on amazon" in command:
        speak_properly("What product are you looking for on Amazon {username}?")
        product_query = listen_for_command()
        search_amazon(product_query)
    elif "search on twitter" in command:
        speak_properly("What would you like to search for on Twitter {username}?")
        twitter_query = listen_for_command()
        search_twitter(twitter_query)
    elif "open news" in command:
        webbrowser.open("www.cbc.ca")
        speak_properly("Opening the news {username}.")
    elif "what's the date" in command:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        speak_properly(f"{username},Today's date is {current_date}.")
    elif "tell me a fun fact" in command:
        fun_fact = get_random_fun_fact()
        speak_properly("Here's a fun fact: " + fun_fact)
    elif "search on bing" in command:
        speak_properly("What would you like to search for on Bing {username}?")
        query = listen_for_command()
        search_bing(query)
    elif "play a game" in command:
        speak_properly("Sure, let's play a game. I'll think of a number between 1 and 10, and you try to guess it.")
        play_number_guessing_game()
    elif "open camera" in command:
        speak_properly("Opening the camera.")
        open_camera()
    elif "read a book" in command:
        speak_properly("Sure, let me read you a short story.")
        read_story()
    elif "translate" in command:
        speak_properly("Sure, please specify the text you want to translate.")
        text_to_translate = listen_for_command()
        speak_properly("To which language would you like to translate the text?")
        target_language = listen_for_command()
        translated_text = translate_text(text_to_translate, target_language)
        speak_properly(f"The translated text is: {translated_text}")
    elif "play music on youtube" in command:
        speak_properly("Sure, what music would you like to listen to on YouTube {username}?")
        music_query = listen_for_command()
        play_music_on_youtube(music_query)
    elif "send message on whatsapp" in command:
        speak_properly("Sure, whom do you want to send a message to on WhatsApp?")
        recipient_name = listen_for_command()
        speak_properly(f"What message would you like to send to {recipient_name} on WhatsApp?")
        message = listen_for_command()
        send_whatsapp_message(recipient_name, message)
    elif "tell me a riddle" in command:
        riddle = get_random_riddle()
        speak_properly("Here's a riddle for you: " + riddle)
    elif "open code editor" in command:
        speak_properly("Opening your code editor.")
        os.system("code")  # Opens the default code editor
    elif "play a joke" in command:
        random_joke = get_random_joke()
        speak_properly("Here's a joke for you: " + random_joke)
    elif "change your voice" in command:
        speak_properly("Certainly! What type of voice would you like me to use?")
        new_voice = listen_for_command()
        change_voice(new_voice)
    elif "scan for injuries" in command:
        speak_properly("Initiating body scan for injuries...")
        scan_result = scan_for_injuries()
        speak_properly("The scan is complete. Here are the results:")
        speak_properly(scan_result)
    elif "system information" in command:
        system_info = get_system_info()
        speak_properly("Here's your system information:")
        speak_properly(system_info)
    elif "open safari" in command:
        speak_properly("Opening Safari {username}.")
        open_safari() 
    elif "open app store" in command:
        speak_properly("Opening the App Store {username}.")
        open_app_store()
    elif "open settings" in command:
        speak_properly("Opening Settings {username}.")
        open_settings()
    elif "tell a joke" in command:
        joke = get_random_joke()
        speak_properly("Here's a joke for you: " + joke)
    elif "show how to subscribe to youtube" in command:
        show_subscribe_instructions()
    elif "search on Wikipedia" in command:
        speak_properly("What would you like to search for on Wikipedia {username}?")
        query = listen_for_command()
        wikipedia_result = search_wikipedia(query)
        if wikipedia_result:
            speak_properly("Here's what I found on Wikipedia:")
            speak_properly(wikipedia_result)
        else:
            speak_properly("I couldn't find information on that topic.")
    elif "play a game" in command:
        speak_properly("Sure, let's play a game. I'll think of a number between 1 and 100, and you can try to guess it.")
        play_number_guessing_game()
    
    elif "i want to ask a question" in command:
        speak_properly("Sure, go ahead and ask your question}{username}.")
        user_question = listen_for_command()
        response = answer_question(user_question)
        speak_properly(response)
        
    elif "search on google" in command:
        import wikipedia as googleScrap
        speak_properly("what would you like to search on google {username}")
        query = command.replace("kevin search","")
        query = command.replace("google search","")
        query = command.replace("google","")
        speak_properly("This is what I found on google")
        try:
            pywhatkit.search(query)
            result = googleScrap.summary(query,1)
            speak_properly(result)

        except:
            speak_properly("No speakable output available")

    elif "who is" in command:
        person = command.split("who is", 1)[1].strip()
        answer = wikipedia_summary(person)
        speak_properly("Here's what I found about " + person + ": " + answer)
    if "define" in command:
            word_to_define = command.split("define", 1)[1].strip()
            define_word(word_to_define)
    elif "what are" in command:
        query = command.split("what are", 1)[1].strip()
        answer = wikipedia_summary(query)
        speak_properly("Here's what I found about why " + query + ": " + answer)
    elif "why are" in command:
        query = command.split("why are", 1)[1].strip()
        answer = wikipedia_summary(query)
        speak_properly("Here's what I found about why " + query + ": " + answer)
    elif "what's my status" in command:
        speak_properly("Your just the man with the plan and i'm very grateful to have you!")
    elif "what is" in command:
        query = command.split("what is", 1)[1].strip()
        answer = wikipedia_summary(query)
        speak_properly("Here's what I found about " + query + ": " + answer)
    elif "shutdown" in command:
        speak_properly("Shutting down your computer.")
        os.system("shutdown /s /t 0")  # Shuts down the computer immediately
    
# Create a thread for listening to voice commands
listen_thread = threading.Thread(target=listen_for_command)

# Create a thread for processing voice commands
process_thread = threading.Thread(target=process_command)

# Start both threads
listen_thread.start()
process_thread.start()

# Function to search on Google
def search(query):
    try:
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        speak_properly(f"Here are the search results for {query}.")
    except Exception as e:
        print("Error searching:", e)
        speak_properly("I encountered an error while searching. Please try again later.")

# Function to play music on YouTube
def play_music_on_youtube(query):
    try:
        # Construct the YouTube search URL
        search_url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(search_url)
        speak_properly(f"Playing music on youTube for {query}.")
    except Exception as e:
        print("Error playing music on youTube:", e)
        speak_properly("I encountered an error while playing music on youTube. Please try again later.")
# ...

# Function to transcribe and analyze emotions in voice commands
def analyze_emotions(command):
    try:
        text_blob = TextBlob(command)
        sentiment = text_blob.sentiment

        if sentiment.polarity > 0:
            return "You sound happy!"
        elif sentiment.polarity < 0:
            return "You sound sad."
        else:
            return "Your emotion is neutral."

    except Exception as e:
        return "Emotion analysis failed. Please try again."

# Function to retrieve data from the internet
def retrieve_data_from_internet(query):
    try:
        url = f"https://api.example.com/data?query={query}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return "Failed to retrieve data from the internet."
    except Exception as e:
        return str(e)


# Function to place a pizza order
def order_pizza(pizza_order):
    api_endpoint = "https://api.pizza-ordering-service.com/place-order"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    order_data = {
        "type": order_details["type"],
        "size": order_details["size"],
        "address": order_details["address"],
        "payment": order_details["payment"]
    }

    try:
        response = requests.post(api_endpoint, json=order_data, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            order_confirmation = response_data.get("confirmation")
            speak("Your pizza order has been placed. Here are the details: " + order_confirmation)
        else:
            speak("I'm sorry, there was an issue with your order. Please try again later.")
    except Exception as e:
        print("Error placing pizza order:", e)
        speak("I encountered an error while placing your order. Please try again later.")

def volumeup():
    for i in range(5):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        sleep(0.1)

def volumedown():
    for i in range(5):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        sleep(0.1)

# Function to answer questions using ChatGPT
def answer_question(question):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"I have a question: {question}\nAnswer:",
        max_tokens=100  # Adjust this to control the response length
    )
    return response.choices[0].text

# Function to get and say user's vitals
def get_vitals():
    # In a real implementation, you would retrieve vitals data from a secure source.
    # For demonstration, we'll use fictional data.
    vitals_data = {
        "heart_rate": 75,
        "blood_pressure": "120/80",
        "temperature": 98.6,
        "oxygen_saturation": 98,
    }

    # Construct a response
    response = "Here are your vitals:\n"
    for key, value in vitals_data.items():
        response += f"{key}: {value}\n"

    return response

# Function to open device settings
def open_settings():
    try:
        os.system("control")
        speak_properly("Opening settings.")
    except Exception as e:
        print("Error opening settings:", e)
        speak_properly("I encountered an error while opening settings. Please try again later.")

# Function to count people in the environment
def count_people_in_environment():
    people_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Implement people detection logic here using OpenCV or other computer vision libraries
        # You can use pre-trained models like Haar cascades or deep learning models like YOLO for people detection

        # Update the people_count based on the detection results

        # Display the frame with people count
        cv2.putText(frame, f'People Count: {people_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Environment Monitoring', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

    return people_count

# Function to minimize the active window
def minimize_window():
    pyautogui.hotkey('win', 'down','down')

# Function to speak the people count
def speak_people_count(people_count):
    engine.say(f"There are {people_count} people in the environment.")
    engine.runAndWait()

# Function to respond to the question "What can you do?"
def describe_capabilities():
    speak_properly("I can perform various tasks, such as opening websites, answering questions, providing information from the web, playing music, and more. You can ask me to do something specific, and I'll do my best to assist you.")

# Function to open Safari
def open_safari():
    try:
        subprocess.run(["open", "-a", "Safari"])
    except Exception as e:
        print("Error:", e)
# Function to open the App Store
def open_app_store():
    try:
        subprocess.run(["open", "-a", "App Store"])
    except Exception as e:
        print("Error:", e)

# Function to fetch the latest news
def get_latest_news():
    news_api_key = "47156559aded4b2ca80bcc2f581b4687"  # Replace with your actual API key
    news_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
    
    response = requests.get(news_url)
    news_data = json.loads(response.text)

    if news_data.get("status") == "ok":
        articles = news_data.get("articles")
        if articles:
            speak_properly("Here are the latest news headlines:")
            for i, article in enumerate(articles):
                if i < 5:
                    title = article.get("title")
                    speak_properly(f"{i + 1}. {title}")
        else:
            speak_properly("I couldn't find any news articles at the moment.")
    else:
        speak_properly("I encountered an error while fetching news. Please try again later.")

# Function to provide an introduction when asked "Who are you?"
def introduce():
    speak_properly("I am Kevin, your personal voice assistant. I can assist you with various tasks and answer your questions. Some of the things I can do include searching the web, opening websites, providing information, and much more.")

# Function to add a task to a project
def add_task(project_name, task):
    if project_name not in projects:
        projects[project_name] = []
    projects[project_name].append(task)

# Function to list tasks in a project
def list_tasks(project_name):
    if project_name in projects:
        tasks = projects[project_name]
        if not tasks:
            print(f"No tasks found in '{project_name}'.")
        else:
            print(f"Tasks in '{project_name}':")
            for i, task in enumerate(tasks, start=1):
                status = "✔" if task["completed"] else "❌"
                print(f"{i}. [{status}] {task['description']}")
    else:
        print(f"Project '{project_name}' does not exist.")

# Function to mark a task as completed
def complete_task(project_name, task_index):
    if project_name in projects and 1 <= task_index <= len(projects[project_name]):
        task = projects[project_name][task_index - 1]
        print(f"Completed task: {task}")
        projects[project_name].pop(task_index - 1)
    else:
        print("Task not found.")


# Function to define a word
def define_word(word):
    try:
        definition = dictionary.meaning(word)
        if definition:
            speak(f"The definition of {word} is: {', '.join(definition[word])}")
        else:
            speak("I couldn't find a definition for that word.")
    except Exception as e:
        speak("I encountered an error while defining the word. Please try again later.")         



# Function to get system information
def get_system_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')

    system_info = f"CPU Usage: {cpu_percent}%\n"
    system_info += f"Memory Usage: {memory_info.percent}%\n"
    system_info += f"Total Disk Space: {disk_info.total / (1024 ** 3):.2f} GB\n"
    system_info += f"Used Disk Space: {disk_info.used / (1024 ** 3):.2f} GB\n"
    system_info += f"Free Disk Space: {disk_info.free / (1024 ** 3):.2f} GB"

    return system_info

# Function to send a WhatsApp message
def send_whatsapp_message(recipient_name, message):
    try:
        # Use pywhatkit to send the WhatsApp message
        # Replace 'your_country_code' with your country code (e.g., +1 for the USA)
        # and 'your_whatsapp_number' with your WhatsApp number
        pywhatkit.sendwhatmsg(f"+2349070067842", message, 0, 0)
        speak_properly(f"Message sent to {recipient_name} on WhatsApp.")
    except Exception as e:
        print("Error sending WhatsApp message:", e)
        speak_properly("I encountered an error while sending the WhatsApp message. Please try again later.")

# Function to show instructions on how to subscribe to YouTube
def show_subscribe_instructions():
    # You can display instructions on how to subscribe to YouTube.
    # This can be done using a GUI or by opening a web page with instructions.
    # Implement the logic to show instructions here.
    
    # For demonstration purposes, we'll print a message.
    print("To subscribe to a YouTube channel, visit the channel's page and click the 'Subscribe' button.")
    speak("To subscribe to a YouTube channel, visit the channel's page and click the 'Subscribe' button.")

# Function to call someone on WhatsApp
def call_on_whatsapp(recipient_number):
    try:
        # Use pywhatkit to make a WhatsApp call
        # Replace 'your_country_code' with your country code (e.g., +1 for the USA)
        pywhatkit.call_on_whatsapp(f"+2349070067842", recipient_number)
        speak_properly(f"Calling {recipient_number} on WhatsApp.")
    except Exception as e:
        print("Error making WhatsApp call:", e)
        speak_properly("I encountered an error while making the WhatsApp call. Please try again later.")

def full_screen_youtube_video():
    # Set up the Chrome web driver
    driver = webdriver.Chrome()
    driver.get("https://www.youtube.com")

    # Find the YouTube video element by searching for a video to watch
    search_box = driver.find_element_by_name("search_query")
    search_box.send_keys("sample video")
    search_box.send_keys(Keys.RETURN)

    # Select the first video in the search results
    video = driver.find_element_by_css_selector("ytd-video-renderer")
    video.click()

    # Maximize the browser window for full-screen effect
    driver.maximize_window()

def open_website(url):
    driver = webdriver.Chrome()
    driver.get(url)

def refresh_page():
    driver.refresh()

def close_browser():
    driver.quit()

def scroll_down():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def scroll_up():
    driver.execute_script("window.scrollTo(0, 0);")

def go_back():
    driver.back()

def go_forward():
    driver.forward()

class VitalsMonitor:
    def __init__(self):
        self.blood_toxicity = 0
        self.heart_rate = 0
        self.blood_pressure = "120/80"

    def update_vitals(self):
        # Simulate random changes in vitals for demonstration purposes
        self.blood_toxicity = random.uniform(0, 1)  # Simulate blood toxicity between 0 and 1
        self.heart_rate = random.randint(60, 100)  # Simulate heart rate between 60 and 100
        self.blood_pressure = f"{random.randint(90, 140)}/{random.randint(60, 90)}"  # Simulate blood pressure

    def get_vitals(self):
        return {
            "blood_toxicity": self.blood_toxicity,
            "heart_rate": self.heart_rate,
            "blood_pressure": self.blood_pressure
        }

# Create a VitalsMonitor instance
vitals_monitor = VitalsMonitor()

# Function to monitor vitals
def monitor_vitals():
    vitals_monitor.update_vitals()
    vitals = vitals_monitor.get_vitals()
    return vitals



# Function to get a random joke from an API
def get_random_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        joke_data = json.loads(response.text)
        setup = joke_data["setup"]
        punchline = joke_data["punchline"]
        return setup + " " + punchline
    except Exception as e:
        print("Error fetching joke:", e)
        return "Why did the chicken cross the road? To get to the other side!"

# Function to fetch a summary from Wikipedia
def wikipedia_summary(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.DisambiguationError as e:
        return "There are multiple interpretations. Please specify your question."
    except wikipedia.exceptions.PageError as e:
        return "I couldn't find information on that topic."

def My_Location():

    ip_add = requests.get('https://api.ipify.org').text
    url ='https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'
    geo_q = requests.get(url)
    geo_d =geo_q.json()
    state = geo_d['city']
    country =geo_d['country']
    speak_properly(f"{username} you are now in {state, country}")

# Main loop for listening to voice commands
if __name__ == "__main__":
    speak_properly("Hello Sir I'm Kevin your virtual assistant. How can I assist you today?")
    while True:
        command = listen_for_command()
        print("You said:", command)
        process_command(command)
    