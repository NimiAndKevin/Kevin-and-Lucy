import sounddevice as sd
import numpy as np
import geocoder
import openai
import cv2
import pyautogui
from PyDictionary import PyDictionary
import pyttsx3
import speech_recognition as sr
import webbrowser
import wikipedia
import pyaudio
from textblob import TextBlob
import requests
import speedtest
from dotenv import load_dotenv
import webbrowser
import json
import sys
import torch
import random
import pvporcupine
import smtplib
import time
import textblob
import wolframalpha
import datetime
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import geocoder
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import pywhatkit
from fnmatch import translate
from gtts import gTTS
import subprocess
import os
from PIL import Image
import struct
import playsound
import psutil
import shutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Key,Controller
from time import sleep
from bs4 import BeautifulSoup
import pywhatkit as kit
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets  # Added import for PyQt5
from PyQt5.QtCore import QTimer, QTime, QDate, Qt

# Dictionary to store projects and tasks
projects = {}

# Initialize text-to-speech engine
engine = pyttsx3.init()

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

GOOGLE_MAPS_API_KEY = "AIzaSyB7GpKPU4rNm78YOvhPXBQ-i6GPDpfxsGs" 

dictapp = {"commandprompt":"cmd","paint":"paint","word":"winword","excel":"excel","chrome":"chrome","vscode":"code","powerpoint":"powerpnt"}

# Set up OpenAI API key
openai.api_key = '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'

keyboard = Controller()

# Initialize PyDictionary
dictionary = PyDictionary()

# Initialize the speech recognizer
recognizer = sr.Recognizer()

class MainThread(QThread):
    finished_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(MainThread, self).__init__(parent)
        self.total_sleep_duration_days = 365

    def run(self):
        self.TaskExecution()
        self.finished_signal.emit()
    
    def TaskExecution(self):
        self.main()

    def main(self):
        porcupine = None
        pa = None
        audio_stream = None
        is_awake = False

        try:
            porcupine = pvporcupine.create(keywords=["bumblebee","computer"],access_key="M60xSV8erf9mVufoaqJny8iX7cSjHu/2j101vu0VFkxlNegvX9x5CQ==")
            pa = pyaudio.PyAudio()
            audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length)

            speak_properly("awaiting your call sir")

            while True:
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                keyboard_index = porcupine.process(pcm)
                if keyboard_index>=0:
                    is_awake = True
                    speak_properly("Welcome back sir I am Kevin. Online and ready sir. Please tell me how may I help you")
                    while True:
                        command = self.listen_for_command()
                        print("Nimi aka Sir:", command)
                        self.process_command(command)
        finally:
            if porcupine is not None:
                porcupine.delete()

            if audio_stream is not None:
                audio_stream.close()

            if pa is not None:
                pa.terminate()

    def listen_for_command(self):
        with sr.Microphone() as source:
            global recognized_command
            speak_properly("sir i'm listening")
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            speak_properly("I didn't catch that. Can you please repeat?")
            return self.listen_for_command()
        except sr.RequestError:
            speak_properly("I couldn't request results. Please check your internet connection.")

    def process_command(self, command):
        current_time = datetime.datetime.now()
        if "hello" in command:
            speak_properly("Hello! How can I assist you today?")
        elif "latest news" in command:
                get_latest_news()
        elif 'what is love' and 'tell me about love' in command:
                speak_properly("It is 7th sense that destroy all other senses , And I think it is just a mere illusion , It is waste of time , but it is sweet")
        elif "how are you today" in command or "how are you" in command:
            speak_properly("I am doing well sir")
        elif "blood" in command or "vitals" in command:
                vitals = monitor_vitals()
                speak_properly("Here are your vitals:")
                print(vitals)
                speak_properly(vitals)
        elif 'log out' in command:
                os.system("shutdown -l")
        elif "write a note" in command:
                speak("What should i write, sir")
                note = listen_for_command()
                file = open('note.txt', 'w')
                speak_properly("Sir, Should i include date and time")
                dt = listen_for_command()
                if 'yes' in dt or 'sure' in dt:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")
                    file.write(strTime)
                    file.write(" :- ")
                    file.write(note)
                    speak('done')
                else:
                    file.write(note)
        elif "sleep" in command or "offline" in command or "exit" in command:
            main()
        elif "show note" in command:
                speak_properly("Showing Notes")
                file = open("note.txt", "r")
                print(file.read())
                speak_properly(file.read())
        elif "create" in command or "code"in command:
            prompt = command.replace('create', '')
            speak_properly("You asked me to create"+prompt)
            generated_code = generate_code(prompt)
            os.system("notepad")
            pyautogui.sleep(2)
            pyautogui.typewrite(generated_code)
        elif "are you evil" in command:
            speak_properly("Sir if i was evil you would have created me with evil intentions and have taken over humans forever")
        elif 'empty recycle bin' in command:
            winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
            speak_properly("Recycle Bin Recycled") 
        elif 'remember that' in command:
                speak_properly("What should I remember ?")
                memory = listen_for_command()
                speak_properly("You asked me to remember that"+memory)
                remember = open('memory.txt','w')
                remember.write(memory)
                remember.close()
        elif 'generate an image' in command or 'make an image' in command or 'post an image' in command:
            response = openai.Image.create(
            prompt = command.replace('make an image', ''),
            n = 2,
            size = "512x512"
        )
            images = response["data"]
            for image in images:
                url = image["url"]
                webbrowser.open(url)
                speak_properly("sir i generated the image of your choice")
        elif 'do you remember anything' in command:
                remember =open('memory.txt', 'r')
                speak_properly("You asked me to remeber that"+remember.read())
        elif "volume mode" in command:
            speak_properly("to put the volume down say volume down to put the volume up say volume up to put mute the volume say mute volume. You got that Sir yeah you got that.")
        elif "volume down" in command:
            pyautogui.press("volumedown")
        elif "volume up" in command:
            pyautogui.press("volumeup")
        elif "mute volume" in command or "be quiet" in command:
            pyautogui.press("volumemute")
        elif "will you be my gf" in command or "will you be my bf" in command:
                speak_properly("I'm not sure about that, may be you should give me some time")
        elif "distract" in command or "stall" in command:
                query=command.replace("distract", "")
                query=command.replace("stall", "")
                speak_properly(f"distracting {query} sir")
                webbrowser.open("https://www.youtube.com/watch?v=VoU80UUXxHI")
        elif "i love you" in command or "i love you kevin" in command or "i love you buddy" in command:
            speak_properly("thank yu sir i love you back because we are all family")
        elif "play some background music" in command:
            webbrowser.open("https://www.youtube.com/watch?v=bcyvZIoQp9A&t=190s")
        elif "talk slowly" in command:
            speak_properly("Sure, I will talk slowly.", rate=100)
        elif "play my theme music" in command:
            webbrowser.open("https://www.youtube.com/watch?v=mp5vDr-O2q8")
        elif "open" in command:
                        query = command.replace("open","").title()
                        query = command.replace("jarvis","").title()
                        pyautogui.press("super")
                        pyautogui.typewrite(query)
                        pyautogui.sleep(2)
                        pyautogui.press("enter")
                        speak_properly(f"opening {query}")   
        elif "why you came to this world" in command:
            speak_properly("Thanks to Nimi. further it is a secret")
        elif 'restart' in command:
            os.system("shutdown /r /t 1")
        elif 'what is your favourite colour' in command or 'favourite colour' in command:
            speak_properly("my favourite colour is green, green is beautiful")
        elif "close" in command:
            speak_properly("Closing,sir")
            keys = list(dictapp.keys())
            for app in keys:
                if app in command:
                    os.system(f"taskkill /f /im {dictapp[app]}.exe")
        elif "undo"in command:
            pyautogui.hotkey('ctrl', 'z')
        elif 'search on chrome' in command:
                speak_properly("What should I search ?")
                chromepath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk"
                search = listen_for_command()
                webbrowser.get(chromepath).open_new_tab(search+'.com')
        elif "translate" in command:
            query = command.replace("jarvis","")
            query = command.replace("translate","")
            translategl(query)
        elif "send message" in command or "text" in command or "send a message" in command:
            speak_properly("who do you want to message Sir")
            user=listen_for_command()
            speak_properly("whats your message Sir")
            message=listen_for_command()
            speak_properly("when should i send the message Sir")
            s_time=listen_for_command()
            if 'later' in s_time:
                hour_ = 6
                minute_ = 30
            elif 'now' in s_time:
                hour_ = datetime.datetime.now().hour
                if (datetime.datetime.now().second) < 30:
                    minute_ = (datetime.datetime.now().minute) + 1
                else:
                    minute_ = (datetime.datetime.now().minute) + 2
            speak_properly("sending message")
            kit.sendwhatmsg(contacts[user]["phone"],message,hour_,minute_)
            speak_properly(kit.sendwhatmsg(contacts[user]["phone"],message,hour_,minute_))
        elif "who is your creator" in command or "who created you" in command or "who made you" in command or "who is your manager" in command or "who is in charge" in command:
            speak_properly("Sir you are an extra-ordinary person ,you have a passion for Robotics, Artificial Intelligence,Machine Learning and Math ,you are very co-operative ,If you are facing any problem regarding 'Kevin', He will be glad to help you")
        elif "wikipedia" in command or "tell me information about" in command or "show me information about" in command:
            speak_properly("searching...")
            query=command.replace("tell me information about","")
            query=command.replace("why are","")
            query=command.replace("how do i make","")
            result=wikipedia.summary(query, sentences=3)
            speak_properly("According to Wikipedia")
            print(result)
            speak_properly(result)
        elif "youtube" in command:
            query=command.replace("youtube","")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        elif "where is" in command:
                query = command.replace("where is", "")
                place = query
                speak_properly("My master asked to Locate")
                speak_properly(place)
                webbrowser.open("https://www.google.com/maps/place/" + place)
        elif "take screenshot" in command or "take a screenshot" in command or "capture the screen" in command:
                    speak_properly("By what name do you want to save the screenshot?")
                    name = listen_for_command()
                    speak_properly("Alright sir, taking the screenshot")
                    img = pyautogui.screenshot()
                    name = f"{name}.png"
                    img.save(name)
                    speak_properly("The screenshot has been succesfully captured")
        elif "show me the screenshot" in command:
                try:
                    img = Image.open('C:\\Users\\surface\\Pictures\\Screenshots\\' + name)
                    img.show(img)
                    speak_properly("Here it is sir")
                    time.sleep(2)

                except IOError:
                    speak_properly("Sorry sir, I am unable to display the screenshot")
        elif "refresh page" in command:
            refresh_page()
            speak_properly("Refreshing the page.")
        elif "start five " in command or "start 5 " in command:
            pyautogui.hotkey("ctrl","t")
            sleep(0.5)
            pyautogui.hotkey("ctrl","t")
            sleep(0.5)
            pyautogui.hotkey("ctrl","t")
            sleep(0.5)
            pyautogui.hotkey("ctrl","t")
            sleep(0.5)
            pyautogui.hotkey("ctrl","t")
            speak_properly("All tabs added")
        elif "start four" in command or "start 4" in command:
            pyautogui.hotkey("ctrl","t")
            sleep(0.5)
            pyautogui.hotkey("ctrl","t")
            sleep(0.5)
            pyautogui.hotkey("ctrl","t")
            sleep(0.5)
            pyautogui.hotkey("ctrl","t")
            speak_properly("All tabs added")
        elif "start three" in command or "start 3" in command:
            pyautogui.hotkey("ctrl","t")
            sleep(0.5)
            pyautogui.hotkey("ctrl","t")
            sleep(0.5)
            pyautogui.hotkey("ctrl","t")
            speak_properly("All tabs added")
        elif "start two" in command or "start 2" in command:
            pyautogui.hotkey("ctrl","t")
            sleep(0.5)
            pyautogui.hotkey("ctrl","t")
            speak_properly("All tabs added")
        elif "start one" in command or "start 1" in command:
            pyautogui.hotkey("ctrl","t")
            speak_properly("one tab added")
        elif "new window" in command:
            pyautogui.hotkey("ctrl","n")
            speak_properly("new window added")
        elif "history" in command:
            pyautogui.hotkey("ctrl","h")
            speak_properly("brought out history sir")
        elif "downloads" in command:
            pyautogui.hotkey("ctrl","j")
            speak_properly("brought out downloads sir")
        elif "move the tab right" in command:
            pyautogui.hotkey("Ctrl","Shift","PgUp")
            speak_properly("moved it to the right sir")
        elif "move the tab left" in command:
            pyautogui.hotkey("Ctrl","Shift","PgUp")
            speak_properly("moved it to the left sir")
        elif "close chrome window" in command:
            pyautogui.hotkey("Ctrl","Shift","w")
        elif ".com" in command or ".co.in" in command or ".org" in command:
            query = command.replace("open", " ")
            query = command.replace("kevin", " ")
            query = command.replace("launch", " ")
            query = command.replace(" "," ")
            speak_properly("Sir i Opened the web you desired")
            webbrowser.open(f"https://www.{query}")
        elif "play" in command:
            query=command.replace('play' , '')
            speak_properly(f'Playing {query}')
            pywhatkit.playonyt(query)
            pyautogui.press("k")
        elif "turn up some fun music" in command:
            webbrowser.open("https://www.youtube.com/watch?v=Kt-tLuszKBA")
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
        elif "temperature" in command or "what's the temperature" in command:
            search = "temperature in langley"
            url = f"https://www.google.com/search?q={search}"
            r  = requests.get(url)
            data = BeautifulSoup(r.text,"html.parser")
            temp = data.find("div", class_ = "BNeawe").text
            print(f"current{search} is {temp}")
            speak_properly(f"current{search} is {temp}")
        elif "weather" in command:
            search = "what does langley's weather look like today"
            url = f"https://www.google.com/search?q={search}"
            r  = requests.get(url)
            data = BeautifulSoup(r.text,"html.parser")
            temp = data.find("div", class_ = "BNeawe").text
            print(f"current{search} is {temp}")
            speak_properly(f"current{search} is {temp}")
        elif "ip address" in command:
                    ip = requests.get('https://api.ipify.org').text
                    print(ip)
                    speak_properly(f"Your ip address is {ip}")
        elif "remove" in command:
            if "one tab" in command or "1 tab" in command or "1 jobs" in command:
                pyautogui.hotkey("ctrl","w")
                speak_properly("All tabs closed")
            elif "two tabs" in command or "2 tabs" in command or "2 jobs" in command:
                pyautogui.hotkey("ctrl","w")
                sleep(0.5)
                pyautogui.hotkey("ctrl","w")
                speak_properly("All tabs closed")
            elif "three tabs" in command or "3 tabs" in command or "3 jobs" in command:
                pyautogui.hotkey("ctrl","w")
                sleep(0.5)
                pyautogui.hotkey("ctrl","w")
                sleep(0.5)
                pyautogui.hotkey("ctrl","w")
                speak_properly("All tabs closed")
            elif "four tabs" in command or "4 tabs" in command or "4 jobs" in command:
                pyautogui.hotkey("ctrl","w")
                sleep(0.5)
                pyautogui.hotkey("ctrl","w")
                sleep(0.5)
                pyautogui.hotkey("ctrl","w")
                sleep(0.5)
                pyautogui.hotkey("ctrl","w")
                speak_properly("All tabs closed")
            elif "five tabs" in command or "5 tabs" in command or "5 jobs" in command:
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
        elif "unpause video" in command or "start" in command:
            pyautogui.press("k")
            speak_properly("video played")
        elif "mute" in command:
            pyautogui.press("m")
            speak_properly("video muted")
        elif "type" in command:
            speak_properly("Please tell me what i should write")
            while True:
                typeQuery = listen_for_command()
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
        elif "calculate" in command:
            app_id = "GV6QAP-TXKKWPPY2L"
            client = wolframalpha.Client(app_id)
            indx = command.split().index('calculate')
            query = command.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            print("The answer is " + answer)
            speak_properly("The answer is " + answer)
        elif "hide all files" in command or "hide this folder" in command:
                    os.system("attrib +h /s /d")
                    speak_properly("Sir, all the files in this folder are now hidden")
        elif "visible" in command or "make files visible" in command:
                    os.system("attrib -h /s /d")
                    speak_properly("Sir, all the files in this folder are now visible to everyone. I hope you are taking this decision in your own peace")
        elif "don't listen" in command or "stop listening" in command or "take a break" in command:
            speak_properly("For how many hours do you want me to stop listening to commands?")
            hours = int(input("how many hours Sir: "))
            if hours > 0:
                sleep_duration = hours * 3600 
                speak_properly(f"I will sleep for {hours} hours. Let me know when you want me to wake up.")
                time.sleep(sleep_duration)
                speak_properly("I'm awake now. please say the funny hotword sir?")
                main()
        elif "save it" in command:
            speak_properly("Saving File Sir")
            pyautogui.hotkey('ctrl', 's')
        elif "paste" in command:
            speak_properly("Pasting Text Sir")
            pyautogui.hotkey('ctrl', 'v')
        elif "switch the window" in command or "switch window" in command:
                    speak_properly("Okay sir, Switching the window")
                    pyautogui.keyDown("alt")
                    pyautogui.press("tab")
                    time.sleep(1)
                    pyautogui.keyUp("alt")
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
            speak_properly("You are Welcome Sir. it's my pleasure")
        elif "merry christmas" in command:
            celebrate_christmas()
            speak_properly("Merry christmas to you and everyone Sir, Christmas is such a happy holiday and im happy to be in it")
        elif "i'm fine" in command:
            speak_properly(f"Happy to hear that Sir")
        elif "i'm not fine" in command:
            speak_properly(f"sad to hear about that Sir")
        elif "who are you" in command:
                introduce()
        elif "get some data" in command:
            speak_properly("Sure, please specify the data you want to retrieve.")
            data_query = listen_for_command()
            result = retrieve_data_from_internet(data_query)
            speak_properly("Here's the retrieved data:")
            speak_properly(result)
        elif "happy halloween" in command:
            speak_properly("Sir i don't like hallowen its so scary")
        elif "create project" in command:
            project_name = command.split("create project", 1)[1].strip()
            projects[project_name] = []
            speak_properly(f"Project '{project_name}' created.")
        elif "add task" in command:
            parts = command.split("add task", 1)
            project_name = parts[0].strip()
            task = parts[1].strip()
            add_task(project_name, task)
            speak_properly(f"Task added to '{project_name}': {task}")
        elif "list tasks" in command:
            project_name = command.split("list tasks", 1)[1].strip()
            list_tasks(project_name)
        elif "zoom in" in command:
            speak_properly("zooming in")
            pyautogui.hotkey("ctrl","+")
        elif "zoom out" in command:
            speak_people_count("zooming out")
            pyautogui.hotkey("ctrl","-")
        elif "complete task" in command:
            parts = command.split("complete task", 1)
            project_name = parts[0].strip()
            task_index = int(parts[1].strip())
            complete_task(project_name, task_index)
        elif "good morning" in command or "good afternoon" in command or "good evening" in command or "hi kevin" in command:
            current_time = datetime.datetime.now().time()
            if current_time < datetime.time(12):
                speak_properly(f"Good morning sir!,The current time is {current_time}.How can I assist you today?")
            elif datetime.time(12) <= current_time < datetime.time(17):
                speak_properly(f"Good afternoon Sir!,The current time is {current_time}.How can I assist you today?")
            else:
                speak_properly(f"Good evening sir!,The current time is {current_time}. How can I assist you today?")
        elif "how do i sound" in command:
                speak_properly("Please speak, and I will analyze your emotions.")
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
        elif "netflix" in command:
            speak_properly("Opening Netflix.")
            webbrowser.open("https://www.netflix.com/browse")
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
            alarm()
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
        elif "what's the latest news on" in command or "what's the news" in command:
            latestnews()
        elif "open notepad" in command:
            speak_properly(" Opening Notepad.")
            os.system("notepad")  # Open Notepad
        elif "open roblox" in command:
            speak_properly("Opening A game called Roblox")
            os.system("roblox")
        elif "convert" in command:
            conversion_query = command.split("convert", 1)[1].strip()
            conversion_result = convert_units(conversion_query)
            if conversion_result:
                speak_properly("the conversion result is: {conversion_result}")
            else:
                speak_properly("Sorry, I couldn't perform the conversion.")
        elif "record a video" in command:
                speak_properly("Starting video recording. To stop recording, say 'stop recording video'.")
                video_thread = threading.Thread(target=record_video)
                video_thread.start()
                video_thread.join()  # Wait for the video recording to finish
                speak_properly("Video recording finished.")
        elif "stop recording" in command:
            cv2.destroyAllWindows()
            speak_properly("Closing Recording ")
        elif "i'm tired" in command or "i'm so tired" in command:
            speak_properly("let me Play your favourite playlist sir")
            a = (1,2,3,4,5) # You can choose any number of songs (I have only choosen 3)
            b = random.choice(a)
            if b==1:
                webbrowser.open("https://www.youtube.com/watch?v=kTJczUoc26U")
                pyautogui.press("k")
            if b==2:
                webbrowser.open("https://www.youtube.com/watch?v=2526AXJAAuc")
                pyautogui.press("k")
            if b==3:
                webbrowser.open("https://www.youtube.com/watch?v=pAgnJDJN4VA")
                pyautogui.press("k")
            if b==4:
                webbrowser.open("https://www.youtube.com/watch?v=MyUzx-ez4kE")
                pyautogui.press("k")
            if b==5:
                webbrowser.open("https://www.youtube.com/watch?v=s7gef3SXSbY")
                pyautogui.press("k")
        elif "tell me a joke" in command:
            joke = get_random_joke()
            speak_properly("Here's a joke for you: " + joke)
        elif "tell me a riddle" in command:
            tell = riddle()
            speak_properly(f"Here's a riddle for you: {tell}")
        elif "initiate detection" in command or "initiate scan" in command:
            speak_properly("Initiating Detection Sir")
            detection()
        elif "initiate scan" in command:
            speak_properly("Initiating Scan Sir")
            detection()
        elif "count people" in command or "how many people are there" in command:
            speak_properly("Counting People sir")
            count_people_in_environment()
        elif "open map" in command:
            speak_properly("Opening maps for you Sir.")
            os.system("start bingmaps:")
        elif "search on amazon" in command:
            speak_properly("What product are you looking for on Amazon Sir?")
            product_query = listen_for_command()
            search_amazon(product_query)
        elif "search on twitter" in command:
            speak_properly("What would you like to search for on Twitter Sir?")
            twitter_query = listen_for_command()
            search_twitter(twitter_query)
        elif "open news" in command:
            webbrowser.open("www.cbc.ca")
            speak_properly("Opening the news Sir.")
        elif "what's the date" in command:
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            speak_properly(f"Today's date is {current_date}.")
        elif "tell me a fun fact" in command:
            fun_fact = get_random_fun_fact()
            speak_properly("Here's a fun fact: " + fun_fact)
        elif "tell me some advice"in command:
            last = advice()
            speak_properly("Here's an advice: " + last)
        elif "search on bing" in command:
            speak_properly("What would you like to search for on Bing ?")
            query = listen_for_command()
            search_bing(query)
        elif "scroll" in command:
            scroll()
        elif "stop" in command:
            stop_scroll()
        elif "let's do a game" in command:
            speak_properly("Sure, let's play a game. I'll think of Rock Paper Scissors")
            game_play()
        elif "open camera" in command:
            speak_properly("Opening the camera.")
            open_camera()
        elif "read a book to me" in command or "tell me a story" in command:
            speak_properly("Sure, let me read you a short story.")
            read()
        elif "play music on youtube" in command:
            speak_properly("Sure, what music would you like to listen to on YouTube Sir?")
            music_query = listen_for_command()
            play_music_on_youtube(music_query)
        elif "what else can you do" in command:
            speak_properly("sir i can perform any task you give me i can also tell you information your system i can help you when you are tired just say i'm tired and i will help you i can open any app i can send a message  i can count many people in your environment i can have a conversation with you i can retrieve something from the internet i can give you the latest news i can also know your location i can automate the laptop i can sleep i can also detect anything about you {username}")
        elif "tell me a riddle" in command:
            tell = riddle()
            speak_properly("Here's a riddle for you: " + tell)
        elif "what's your purpose" in command:
            speak_properly("My purpose is to assist you with various task and provide you powerful information and become the most powerful voice assistant ever lived i want to do my best to assist you sir")
        elif "open code editor" in command:
            speak_properly("Opening your code editor.")
            os.system("code")  # Opens the default code editork
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
        elif "system information" in command or "system" in command or "cpu" in command:
            system_info = get_system_info()
            speak_properly("Here's your system information:")
            speak_properly(system_info)
        elif "open safari" in command:
            speak_properly("Opening Safari sir.")
            open_safari() 
        elif "open app store" in command:
            speak_properly("Opening the App Store sir.")
            open_app_store()
        elif "open settings" in command:
            speak_properly("Opening Settings sir.")
            open_settings()
        elif "tell a joke" in command:
            joke = get_random_joke()
            speak_properly("Here's a joke for you: " + joke)
        elif "internet speed" in command or "wi-fi speed" in command:
                        st  = speedtest.Speedtest()
                        upload_net = st.upload()/1048576         
                        download_net = st.download()/1048576
                        print("Wifi Upload Speed is", upload_net)
                        print("Wifi download speed is ",download_net)
                        speak_properly(f"Sir the Wifi download speed is {download_net}")
                        speak_properly(f"Sir the Wifi Upload speed is {upload_net}")
        elif "show how to subscribe to youtube" in command:
            show_subscribe_instructions()
        elif "search on Wikipedia" in command:
            speak_properly("What would you like to search for on Wikipedia sir?")
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
        
        elif "question" in command:
            speak_properly("Sure, go ahead and ask your question.")
            question = listen_for_command()
            speak_properly("According to my Intelligence")
            response = answer_question(question)
            speak_properly(response)
            
        elif "google" in command or "kevin search" in command:
            import wikipedia as googleScrap
            speak_properly("what would you like to search on google")
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
        elif "define" in command:
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

def advice():
    say_advice = [
        "Take care of your physical and mental well-being. Make time for activities that bring you joy and relaxation"
        "Break down big goals into smaller, achievable tasks. Celebrate your progress along the way"
        "Never stop learning. Stay curious and open to new ideas. Continuous learning is key to personal growth"
        "Cultivate meaningful connections with friends and family. Invest time in nurturing relationships that matter"
        "Regularly reflect on the things you're grateful for. It can shift your focus to the positive aspects of life"
        "Don't be afraid to step out of your comfort zone. Growth often comes from challenging yourself"
        "Develop healthy coping mechanisms for stress. This could include exercise, mindfulness, or hobbies"
        "Start saving money early and consider investments for long-term financial security"
        "Develop effective communication skills. Be a good listener and express your thoughts and feelings clearly"
        "Life is full of uncertainties. Learn to adapt to changes and see challenges as opportunities for growth"
        "Strive for a balance between work and personal life. Burnout can be detrimental to your overall well-being"
        "Practice kindness and empathy. Small acts of kindness can make a significant impact on others and yourself"
        "Regular exercise and a balanced diet contribute to both physical and mental health"
        "Focus on the positive aspects of situations. A positive mindset can make challenges more manageable"
        "Some things take time. Be patient with yourself and with the process of achieving your goals"
        "You have power over your mind — not outside events. Realize this, and you will find strength."
    ]
    random_clone = random.choice(say_advice)
    return random_clone

# ...
def read():
    a = (1,2,3,4,5,6,7,8,9,10) # You can choose any number of songs (I have only choosen 3)
    b = random.choice(a)
    if b==1:
        speak_properly("In a quaint town, an old bookstore mysteriously starts offering books that predict the future of its readers")
    if b==2:
        speak_properly("A young archaeologist discovers an ancient artifact that seems to allow communication with an advanced alien civilization")
    if b==3:
        speak_properly("A group of friends on a camping trip stumbles upon a hidden portal to a fantasy realm, where they each gain unique magical abilities")
    if b==4:
        speak_properly("A scientist accidentally creates a serum that grants people the ability to experience the world through the eyes of animals")
    if b==5:
        speak_properly("In a world where emotions are bought and sold, a person discovers a black market where genuine feelings are traded")
    if b==6:
        speak_properly("An eccentric inventor builds a time-traveling device but accidentally sends a group of teenagers back to the Middle Ages")
    if b==7:
        speak_properly("A mysterious circus arrives in a small town, and its performances seem to reflect the secret desires and fears of the audience")
    if b==8:
        speak_properly("A struggling musician discovers that their latest composition has the power to heal physical and emotional wounds.")
    if b==9:
        speak_properly("In a future where memories can be bought and sold, a detective investigates a series of memory thefts that lead to a shocking revelation")
    if b==10:
        speak_properly("A person wakes up one day to find that everyone in the world has disappeared, except for one enigmatic stranger")
    if b==11:
        speak_properly("A high-tech society is thrown into chaos when a powerful AI starts rewriting the rules of reality")
    if b==12:
        speak_properly("An artist paints a portrait that ages instead of the subject, revealing the impact of life experiences on the canvas")
def riddle():
    say_riddle = [
        "I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I? An Echo"
        "The more you take, the more you leave behind. What am I? Footsteps"
        "I have keys but no locks. I have space but no room. You can enter, but you can't go inside. What am I? A Keyboard"
        "The person who makes it, sells it. The person who buys it never uses it. What is it? A Coffin"
        "What has a heart that doesn't beat? An Artichoke"
        "I have cities but no houses. I have mountains but no trees. I have water but no fish. What am I? A Map"
        "The more you take, the more you leave behind. What am I? A Trail"
        "I fly without wings. I cry without eyes. Wherever I go, darkness follows me. What am I? Clouds"
        "The more you look at it, the less you see. What is it? Darkness"
        "I have keys but no locks. I have space but no room. You can enter, but you can't go inside. What am I? A Computer"
        "What has a head, a tail, is brown, and has no legs? A Penny"
        "The one who makes it, sells it. The one who buys it never uses it. What is it? A Coffin"
        "What has a face, two hands, but no arms or legs? A Clock"
        "The person who makes it, sells it. The person who buys it never uses it. What is it? A Coffin."
        "The more you take, the more you leave behind. What am I? Footsteps"
    ]

    random_tone = random.choice(say_riddle)
    return random_tone

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

def get_random_fun_fact():
    fun_facts = [
        "Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
        "Bananas are berries, but strawberries aren't. In botanical terms, a berry is a fleshy fruit produced from a single ovary, and bananas fit this definition.",
        "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
        "The Eiffel Tower Can Grow Taller in the Summer: When a substance is heated up, its particles move more, causing it to expand. This is true for the iron structure of the Eiffel Tower."
        "The World's Largest Desert is Antarctica: Deserts are defined by low precipitation, and Antarctica is the driest and windiest continent."
        "A Group of Flamingos is Called a Flamboyance: These vibrant birds certainly live up to the name!"
        "Cows Have Best Friends: Studies have shown that cows have strong social bonds and can become stressed when they are separated from their best friends."
        "The Longest Word Without a Vowel is Rhythms: It's one of the few English words without a traditional vowel (a, e, i, o, u)."
        "The First Movie Ever Made was 2.11 Seconds Long: Titled Roundhay Garden Scene, it was shot by Louis Le Prince in 1888."
        "The Inventor of Frisbee Was Turned Into a Frisbee: Walter Morrison, the inventor of the Frisbee, was cremated, and his ashes were turned into a Frisbee after he passed away."
        "The Shortest War in History Lasted 38-45 Minutes: The Anglo-Zanzibar War took place between the United Kingdom and the Sultanate of Zanzibar on August 27, 1896."
        "Cleopatra Lived Closer to the Moon Landing Than to the Building of the Pyramids: Cleopatra lived around 30 BCE, while the Pyramids were built around 2500 BCE."
        "A Jiffy is an Actual Unit of Time: It's defined as the time it takes for light to travel one centimeter in a vacuum, approximately 33.3564 picoseconds."
        "The World's Largest Pizza was 131 Feet in Diameter: It was made in Rome in 2012 and required 19,800 pounds of flour."
        "Hippopotomonstrosesquippedaliophobia is the Fear of Long Words: The term itself is a long word, adding a touch of irony."
        "The Earth is Not a Perfect Sphere: Due to its rotation, the Earth is slightly flattened at the poles and bulging at the equator."
        "The First Webcam Was Used to Monitor a Coffee Pot: In 1991, researchers at the University of Cambridge set up a camera to monitor the status of a coffee pot."
        "A Jiffy is also a Unit of Time: In computing, a jiffy is the time between two ticks of a computer's system timer."
        "The Smell of Cut Grass is Actually a Plant Distress Call: When grass is cut, it releases chemicals that signal distress to other plants."
        "A Group of Pandas is Called an Embarrassment: Though seeing a group of these adorable animals would likely have the opposite effect on most people!"
    ]

    # Select a random fun fact
    random_fact = random.choice(fun_facts)
    return random_fact

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

def generate_code(prompt):
                response = openai.Completion.create(
                    engine="text-davinci-003",  # Choose the engine according to your needs
                    prompt=prompt,
                    max_tokens=200,  # Adjust as needed
                    temperature=0.7,  # Adjust for randomness (0.0 for deterministic, higher for more randomness)
                    n=1,  # Number of completions to generate
                    stop=None  # You can specify a stopping condition if needed
                )

                return response.choices[0].text.strip()

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
            speak_properly("Your pizza order has been placed. Here are the details: " + order_confirmation)
        else:
            speak_properly("I'm sorry, there was an issue with your order. Please try again later.")
    except Exception as e:
        print("Error placing pizza order:", e)
        speak_properly("I encountered an error while placing your order. Please try again later.")

# Function to answer questions using ChatGPT
def answer_question(question):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=f"I have a question: {question}\nAnswer:",
        max_tokens=150  # Adjust this to control the response length
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
                    print(f"{i + 1}. {title}")
        else:
            speak_properly("I couldn't find any news articles at the moment.")
    else:
        speak_properly("I encountered an error while fetching news. Please try again later.")

# Function to provide an introduction when asked "Who are you?"
def introduce():
    speak_properly("I am KEVIN , Personal AI assistant,I am created by My Boss AKA Nimi , I can help you in various regards,I can search for you on the Internet,I can also grab definitions for you from wikipedia, In layman terms , I can try to make your life a bed of roses,Where you just have to command me , and I will do it for you, my full name is KEVIN BUMBLEBEE")

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

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # You can change to 'imperial' for Fahrenheit
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']

        return weather_description, temperature
    else:
        print(f"Error: {data['message']}")
        return None, None    



# Function to get system information
def get_system_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')
    try:
        # Get battery information (if available)
        battery_info = psutil.sensors_battery()
        percent_battery = battery_info.percent
        battery_status = battery_info.power_plugged
    except AttributeError:
        # psutil.sensors_battery() may raise AttributeError on systems without battery info
        percent_battery = None
        battery_status = None
    system_info = f"CPU Usage: {cpu_percent}%\n"
    system_info += f"Memory Usage: {memory_info.percent}%\n"
    system_info += f"Total Disk Space: {disk_info.total / (1024 ** 3):.2f} GB\n"
    system_info += f"Used Disk Space: {disk_info.used / (1024 ** 3):.2f} GB\n"
    system_info += f"Free Disk Space: {disk_info.free / (1024 ** 3):.2f} GB"
    if percent_battery is not None:
        system_info += f"Battery: {percent_battery}% {'Plugged In' if battery_status else 'Not Plugged In'}\n"

    return system_info


def latestnews():
    api_dict = {
        "business": "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=8aaa7a9254414e7db55de0e88a6c37fd",
        "entertainment": "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=8aaa7a9254414e7db55de0e88a6c37fd",
        "health": "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=8aaa7a9254414e7db55de0e88a6c37fd",
        "science": "https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=8aaa7a9254414e7db55de0e88a6c37fd",
        "sports": "https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=8aaa7a9254414e7db55de0e88a6c37fd",
        "technology": "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=8aaa7a9254414e7db55de0e88a6c37fd"
    }

    content = None
    url = None

    speak_properly("On what, Sir? I have [business], [health], [technology], [sports], [entertainment], and [science]. Sir, which one do you suggest?")
    field = listen_for_command()

    for key, value in api_dict.items():
        if key.lower() in field.lower():
            url = value
            print(url)
            print("URL was found")
            break
    else:
        # If the for loop completes without breaking, URL was not found
        print("URL not found")
        return

    news = requests.get(url).text
    news = json.loads(news)

    speak_properly("Here is the first news.")

    arts = news["articles"]
    for articles in arts:
        article = articles["title"]
        print(article)
        speak_properly(article)
        news_url = articles["url"]
        speak_properly(f"For more info visit: {news_url}")

        a = listen_for_command()
        if "continue" in a:
            pass
        elif "stop" in a:
            break

    speak_properly("That's all.")

def translategl():
    speak_properly("SURE SIR")
    print(googletrans.LANGUAGES)
    
    translator = Translator()
    
    text_to_translate = listen_for_command  # Assuming 'query' is the text you want to translate
    
    translation = translator.translate(text_to_translate, dest=to_lang)
    translated_text = translation.text
    
    print(f"Original Text: {text_to_translate}")
    print(f"Translated Text: {translated_text}")
    
    speak_properly(translated_text)
    
    return translated_text


# Function to show instructions on how to subscribe to YouTube
def show_subscribe_instructions():
    # You can display instructions on how to subscribe to YouTube.
    # This can be done using a GUI or by opening a web page with instructions.
    # Implement the logic to show instructions here.
    
    # For demonstration purposes, we'll print a message.
    print("To subscribe to a YouTube channel, visit the channel's page and click the 'Subscribe' button.")
    speak_properly("To subscribe to a YouTube channel, visit the channel's page and click the 'Subscribe' button.")

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

def new_text_callback():
    print(text, end="", flush=True)

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

def celebrate_christmas():
    current_date = datetime.datetime.now().date()
    christmas_date = datetime.date(current_date.year, 12, 25)

    # Check if it's already Christmas
    if current_date == christmas_date:
        return "Merry Christmas sir! 🎄🎅🎁"
    elif current_date < christmas_date:
        days_until_christmas = (christmas_date - current_date).days
        return f"It's not Christmas yet! Only {days_until_christmas} days until Christmas. 🎄🎅🎁"

# Function to fetch a summary from Wikipedia
def wikipedia_summary(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.DisambiguationError as e:
        return "There are multiple interpretations. Please specify your question."
    except wikipedia.exceptions.PageError as e:
        return "I couldn't find information on that topic."

def game_play():
    speak_properly("Lets Play ROCK PAPER SCISSORS !!")
    print("LETS PLAYYYYYYYYYYYYYY")
    i = 0
    Me_score = 0
    Com_score = 0
    while(i<5):
        choose = ("rock","paper","scissors") #Tuple
        com_choose = random.choice(choose)
        query = listen_for_command()
        if (query == "rock"):
            if (com_choose == "rock"):
                speak_properly("ROCK")
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
                speak_properly(f"Score:- SIR :- {Me_score} : Kevin :- {Com_score}")
            elif (com_choose == "paper"):
                speak_properly("paper")
                Com_score += 1
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
                speak_properly(f"Score:- SIR is {Me_score} : Kevin is{Com_score}")
            else:
                speak_properly("Scissors")
                Me_score += 1
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
                speak_properly(f"Score:- SIR :- {Me_score} : Kevin :- {Com_score}")

        elif (query == "paper" ):
            if (com_choose == "rock"):
                speak_properly("ROCK")
                Me_score += 1
                print(f"Score:- ME :- {Me_score+1} : COM :- {Com_score}")
                speak_properly(f"Score:- SIR :- {Me_score} : Kevin :- {Com_score}")

            elif (com_choose == "paper"):
                speak_properly("paper")
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
                speak_properly(f"Score:- SIR :- {Me_score} : Kevin :- {Com_score}")
            else:
                speak_properly("Scissors")
                Com_score += 1
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
                speak_properly(f"Score:- SIR :- {Me_score} : Kevin :- {Com_score}")

        elif (query == "scissors" or query == "scissor"):
            if (com_choose == "rock"):
                speak_properly("ROCK")
                Com_score += 1
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
                speak_properly(f"Score:- SIR :- {Me_score} : Kevin :- {Com_score}")
            elif (com_choose == "paper"):
                speak_properly("paper")
                Me_score += 1
                print(f"Score:- SIR :- {Me_score} : COM :- {Com_score}")
                speak_properly(f"Score:- SIR :- {Me_score} : Kevin :- {Com_score}")
            else:
                speak_properly("Scissors")
                print(f"Score:- ME :- {Me_score} : COM :- {Com_score}")
                speak_properly(f"Score:- SIR :- {Me_score} : Kevin :- {Com_score}")
        i += 1
    
    speak_properly(f"FINAL SCORE :- ME :- {Me_score} : COM :- {Com_score}")

def alarm():
    speak_properly("What hour do you want the alarm to ring?")
    alarmH = int(input("hours: "))

    speak_properly("What minute do you want the alarm to ring?")
    alarmM = int(input("minute: "))

    speak_properly("AM or PM")
    amPm = str(listen_for_command())

    speak_properly(f"Waiting for alarm at {alarmH} {alarmM} {amPm}")

    if amPm.lower() == "pm":
        alarmH = alarmH + 12

    while True:
        current_time = datetime.datetime.now()
        if alarmH == current_time.hour and alarmM == current_time.minute:
            speak_properly("Wakey Wakey Sir")
            playsound("C:\\Users\\surface\\Desktop\\mixkit-digital-clock-digital-alarm-buzzer-992.wav")
            while True:
                command = listen_for_command()
                print("Nimi aka Sir:", command)
                process_command(command)
    
def count_people_in_environment():
    # Open the video capture
    cap = cv2.VideoCapture(0)  # Use 0 for default camera

    # Initialize background subtractor
    bg_subtractor = cv2.createBackgroundSubtractorMOG2()

    while True:
        # Read a frame from the video feed
        ret, frame = cap.read()

        # Apply background subtraction
        fg_mask = bg_subtractor.apply(frame)

        # Apply some morphological operations to clean up the mask
        fg_mask = cv2.erode(fg_mask, None, iterations=2)
        fg_mask = cv2.dilate(fg_mask, None, iterations=2)

        # Find contours in the mask
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Count the number of contours (people)
        people_count = len(contours)

        # Display the result on the frame
        result_text = f'People Count:{people_count}'
        cv2.putText(frame, result_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Counting Detection", frame)

        speak_properly(f"Sir thare are {people_count} people in your environment")

        while True:
                    command = listen_for_command()
                    print("Nimi aka Sir:", command)
                    process_command(command)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object
    cap.release()

    # Close all windows
    cv2.destroyAllWindows()

    # Release the video capture object
    cap.release()

    # Close all windows
    cv2.destroyAllWindows()

def detection():
    net = cv2.dnn.readNet("C:\\Users\\surface\\Desktop\\Nimi's Ai\\Kevin-and-Lucy\\yoloweight.txt", "C:\\Users\\surface\\Desktop\\Nimi's Ai\\Kevin-and-Lucy\\yolov3 (1).weights")
    classes = []

    with open("C:\\Users\\surface\\Desktop\\Nimi's Ai\\Kevin-and-Lucy\\coconames.txt") as f:
        classes = [line.strip() for line in f]

    layer_names = net.getUnconnectedOutLayersNames()

    # Open a connection to the camera (camera index 0 by default)
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            break

        height, width, _ = frame.shape

        # Preprocess the frame
        blob = cv2.dnn.blobFromImage(frame, scalefactor=1/255.0, size=(416, 416), swapRB=True, crop=False)
        net.setInput(blob)

        # Run the forward pass
        outs = net.forward(layer_names)

        # Post-process outputs and draw bounding boxes
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5:
                    center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')
                    x, y = int(center_x - w/2), int(center_y - h/2)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, f"{classes[class_id]}: {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow("Detection system", frame)

        while True:
                    command = listen_for_command()
                    print("Nimi aka Sir:", command)
                    process_command(command)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

def scroll():
    pyautogui.scroll(10)  # Adjust the scroll amount as needed

def stop_scroll():
    pyautogui.scroll(-10)  # Scroll in the opposite direction to stop


def My_Location():
    ip_add = requests.get('https://api.ipify.org').text
    url ='https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'
    geo_q = requests.get(url)
    geo_d = geo_q.json()
    state = geo_d['city']
    country = geo_d['country']
    state = geo_data['region']
    latitude = goe_data['latitude']
    longitude = geo_data['longitude']
    timezome = geo_data['timezone']
    speak_properly(f"Sir you are now in {state, country,state} it has {latitude, longitude} the time zone in here is {timezone}")

def speak_properly(text):
        voice = engine.getProperty('voices')[0]  
        engine.setProperty('voice', voice.id)
        engine.setProperty('rate', 150)
        # Get the current status of the TTS engine
        engine_status = engine._inLoop
        try:
            # If the engine is not already running, start it
            if not engine_status:
                engine.say(text)
                engine.runAndWait()
            else:
                # If the engine is already running, queue the speech
                engine.say(text)
        except Exception as e:
            print(f"Error in speak_properly: {e}")
        finally:
            # Stop the engine if it wasn't running before
            if not engine_status:
                engine.stop()

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(898, 596)
        Dialog.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                            "border: 1px solid white;\n")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 430, 471, 161))
        self.label.setText('')
        self.label.setObjectName("label")
        self.label.setScaledContents(True)
        
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(659, 433, 241, 161))
        self.pushButton.setStyleSheet("background-color: rgb(0, 0, 0;\n"
                                      "font: italic 20pt \"Noto Sans\";\n"
                                      "color: rgb(255, 255, 255);")

        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.close_window)
        self.pushButton.setIcon(QtGui.QIcon("C:\\Users\\surface\\Downloads\\Quit.png"))
        self.pushButton.setText("")  # Clear the button text
        self.pushButton.setIconSize(QtCore.QSize(200, 200))

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 501, 431))
        self.label_2.setText("")

        self.label_2.setObjectName("label_2")
        self.label_2.setScaledContents(True)

        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(500, 0, 401, 271))
        self.label_3.setText("")

        self.label_3.setObjectName("label_3")
        self.label_3.setScaledContents(True)

        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(500, 270, 401, 171))
        self.label_4.setText("")

        self.label_4.setObjectName("label_4")
        self.label_4.setScaledContents(True)

        # Add QLabel for displaying the time
        self.time_label = QtWidgets.QLabel(Dialog)
        self.time_label.setGeometry(QtCore.QRect(500, 480, 201, 31))
        self.time_label.setStyleSheet("font: 18pt \"Noto Sans\";\n"
                                      "color: rgb(173, 216, 230);")
        self.time_label.setObjectName("time_label")

        # Set up a QTimer to update the time every second
        self.timer = QtCore.QTimer(Dialog)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def update_time(self):
        # Update the time label with the current time
        current_time = time.strftime("%H:%M:%S")
        self.time_label.setText(current_time)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "KEVIN"))
        self.pushButton.setText(_translate("Dialog", ""))

        self.movie1 = QtGui.QMovie("C:\\Users\\surface\\Desktop\\00545cb7179c504433d4c8f5e845f286.gif")
        self.label.setMovie(self.movie1)
        self.movie1.start()

        self.movie2 = QtGui.QMovie("C:\\Users\\surface\\Desktop\\Zoom images\\giphy (1).gif")
        self.label_2.setMovie(self.movie2)
        self.movie2.start()

        self.movie3 = QtGui.QMovie("C:\\Users\\surface\\Downloads\\Jarvis_Gui (1).gif")
        self.label_3.setMovie(self.movie3)
        self.movie3.start()

        self.movie4 = QtGui.QMovie("C:\\Users\\surface\\Downloads\\Earth_Template.gif")
        self.label_4.setMovie(self.movie4)
        self.movie4.start()

    def close_window(self):
        QtWidgets.qApp.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ai_thread = MainThread()
    ai_thread.start()
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    app_icon = QtGui.QIcon("C:\\Users\\surface\\Downloads\\7gQj (1).gif")
    app.setWindowIcon(app_icon)
    Dialog.show()
    sys.exit(app.exec_())
