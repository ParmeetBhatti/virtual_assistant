import pyttsx3
import speech_recognition as sr
import wikipedia
import datetime
import json
from urllib.request import urlopen
from playsound import playsound
import webbrowser
import pywhatkit
import os
import pyjokes
import re
import time


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate", 178)

def speak(audio):
    engine.say(audio)
    print(f"Param: \"{audio}\"\n")
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 8 and hour < 12:
        speak("Good Morning Sir!")
    elif hour >= 12 and hour < 17:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")

    speak("I am Param, Your Virtual Assistant")
    speak("How May I Help you Today?")

def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 1000
        r.pause_threshold = 0.8
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"You: \"{query}\"\n")
        except Exception as e:
            speak("Sorry I couldn't catch that")
            speak("Please try again")
            taskExec()
    return query

def lastWord(str):
    newstr = ""
    l = len(str)
    for i in range(l-1, 0, -1):
        if(str[i] == " "):
            return newstr[::-1]
        else:
            newstr = newstr + str[i]

def seclastWord(str):
    test = re.search(r'(?<=\s)\w+', str[::-1])
    return (test.group(0)[::-1])

def taskExec():
    while True:
        query = takeCommand().lower()
        # Logic for executing tasks based on query
        if 'hello' in query or 'hi' in query:
            speak("Hello Sir, How Can I Help You")
        elif 'how are you' in query:
            speak("I am Fine, What about you?")
        elif 'i am fine' in query:
            speak("Wonderful to Hear Sir, is there anything I can do for you")
        elif 'what is your name' in query:
            speak("My Name is Param, What's Yours?")
        elif 'my name is' in query:
            query = query.replace("my name is","")
            speak("Hello" + query + ", How can I help you?")
        elif 'wikipedia' in query:
            speak('Searching Wikipedia')
            query = query.replace("search","")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'search' in query:
            speak("Showing Search Results on Google")
            query = query.replace("search","")
            pywhatkit.search(query)
            time.sleep(15)
        elif 'open' in query:
            speak("Opening...")
            query = lastWord(query)
            web1 = query + '.com'
            webbrowser.open(web1)
            time.sleep(15)
        elif 'music' in query or 'song' in query:
            speak("Ok, Playing Music")
            music_dir = r'C:\Users\Parmeet\Dropbox\My PC (LAPTOP-AMOBL683)\Desktop\Virtual_Assistant\Music'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))
            time.sleep(15)
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the current time is {strTime}")
        elif 'greetings to' in query:
            query=query.replace("give greetings to","")
            speak(f" Hello...{query}...Hope you have a great day ahead of you")
        elif 'alarm' in query:
            speak("Alright, when for?") 
            tim = input("Param: Enter the time(in HH:MM:SS): ")
            speak("Alarm Set for " + tim)
            while True:
                Time_Ac = datetime.datetime.now()
                now = Time_Ac.strftime("%H:%M:%S")
                if now == tim:
                    playsound(r'C:\Users\Parmeet\Dropbox\My PC (LAPTOP-AMOBL683)\Desktop\Virtual_Assistant\Alarm.mp3')
                elif now > tim:
                    speak("Alarm Over")
                    break
        elif 'timer for' in query:
            tm = (lastWord(query))
            tm1 = int((seclastWord(query)))
            if tm == "seconds":
                timer = tm1
                speak(f"Timer has been set for {tm1} seconds")
            elif tm == "minutes":
                timer = tm1 * 60
                speak(f"Timer has been set for {tm1} minutes")
            elif tm == "hours":
                timer = tm1 * 3600
                speak(f"Timer has been set for {tm1} hours")
            while timer > 0:
                time.sleep(1)
                timer -= 1
            playsound(r'C:\Users\Parmeet\Dropbox\My PC (LAPTOP-AMOBL683)\Desktop\Virtual_Assistant\Alarm.mp3')
            speak(f"Your timer has completed")
        elif 'joke' in query:
            get = pyjokes.get_joke()
            speak(get)
        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            speak("Showing " + location + " in google maps")
            webbrowser.open("https://www.google.nl/maps/place/" + location)
        elif 'news' in query:
            try:
                jsonObj = urlopen('''https://newsapi.org/v2/top-headlines?sources=google-news-in&apiKey=da9c509c936c41c09a1d6e5df2621134''')
                data = json.load(jsonObj)
                i = 1
                speak('Here are some Top Headlines from Google News')
                print('''=============== GOOGLE NEWS ============'''+ '\n')
                for item in data['articles']:
                    print(str(i) + '. ' + item['title'] + '\n')
                    # print(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    i += 1
            except Exception as e:
                print(str(e))
        elif 'thank you' in query:
            speak("Bye Sir. Have a Great Day")
            exit()
        elif 'stop' in query:
            speak("Thanks for giving me your time, Hope you have a great day ahead!")
            exit()

wishMe()
taskExec()
