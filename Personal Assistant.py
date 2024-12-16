import operator
import smtplib
import time
import PyPDF2
import cv2
import pyttsx3
import requests
import speech_recognition as sr
import datetime
import os
import random
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import secure_smtplib
import sys
import subprocess
import pyjokes
import pyautogui
import instaloader
from bs4 import BeautifulSoup
from pywikihow import search_wikihow
import psutil
import speedtest
from twilio.rest import Client

is_paused = False

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)

def say(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source,timeout=1,phrase_time_limit=5)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User Said: {query}")

    except Exception as e:
        # say('Say that again Please...')
        return None
    return query

def wish():
    hour = int(datetime.datetime.now().strftime("%H"))
    if hour>=0 and hour<=12:
        say("Good Morning Sir...")
    elif hour>12 and hour<18:
        say("Good Afternoon Sir...")
    else:
        say("Good Evening Sir...")

    say("I am Your Assitant How can I help you ")

def set_alarm(alarm_time):
    global alarm_process
    print(f"Alarm set for {alarm_time}")
    music_dir = r"C:\Users\it\Music"
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == alarm_time:
            # print("Time to wake up Sir!")
            # print(f"Its {current_time} Please Wake Up...")
            if os.path.exists(music_dir):
                songs = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav', '.aac'))]
                if songs:
                    song_to_play = os.path.join(music_dir, random.choice(songs))
                    print(f"Playing: {song_to_play}")
                    
                    alarm_process = subprocess.Popen(['start', '', song_to_play], shell=True)
                else:
                    print("No valid audio files found in the directory.")
            else:
                print("Music folder does not exist. Please check the path.")

            say("Time to wake up Sir!")
            say(f"Its {current_time} Please Wake Up...")
            time.sleep(15)
            break
        time.sleep(30)
        
def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=yourkey'
    try:
        main_page = requests.get(main_url).json()
        if 'articles' not in main_page:
            print("No articles found in the response.")
            say("Sorry, I couldn't fetch the news.")
            return
        articles = main_page['articles']
        head = []
        day = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
        for ar in articles:
            head.append(ar['title'])
        for i in range(len(day)):
            if i < len(head):
                # print(f"Today's {day[i]} news is: {head[i]}")
                say(f"Today's {day[i]} news is: {head[i]}")
    except Exception as e:
        print(f"An error occurred: {e}")
        say("Sorry, there was an error fetching the news.")

def pdf_reader():
    book = open('file name','rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    say(f"Total Numbers of Pages in this book {pages}")
    say("Sir, Please enter the Page Number I have to Read")
    pg = int(input("Please Enter the Page Number: "))
    page = pdfReader.getPage(pg)
    text = page.extractText()
    say(text)
    
# def sendEmail(to,content):
#     server = smtplib.SMTP('smtp.gmail.com' , 587)
#     server.ehlo()
#     server.starttls()
#     server.login('email address','password')
#     server.sendmail('email address', to , content)
#     server.close()

def TaskExecution():
    global is_paused 
    wish()
    while True:
        if is_paused:
            say("I am currently paused. Say 'resume' to continue.")
            while is_paused:
                time.sleep(1)  
                query = takeCommand()
                if query and 'wake up' in query:
                    is_paused = False
                    say("Resuming operations, How can I assist you?")
                    break  
        query = takeCommand()
        if query is None:
            say('Please repeat your command.')
            continue  
        if 'sleep now' in query:
            is_paused = True
            say("Okay Sir, You can say 'wake up' to continue.")
            continue

        sites = [['youtube','https://www.youtube.com'],['wikipedia','https://www.wikipedia.com'],['github','https://www.github.com'],['gmail','mail.google.com'],['gpt','https://www.chatgpt.com'],['monkeytype','https://www.monkeytype.com']]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} Sir...")
                webbrowser.open(site[1])

#-----------------Opening Apps--------------------------------------------#
        if 'open notepad' in query:
            os.system(r'"C:\Users\it\AppData\Local\Microsoft\WindowsApps\notepad.exe"')

        elif 'open chrome' in query:
            os.system(r'"C:\Program Files\Google\Chrome\Application\chrome.exe"')

        elif 'open vs code' in query:
            os.system(r'"C:\Users\it\AppData\Local\Programs\Microsoft VS Code\code.exe"')

        elif 'open edge' in query:
            os.system(r'"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"')

        elif 'open spotify' in query:
            os.system(r'"C:\Users\it\AppData\Local\Microsoft\WindowsApps\Spotify.exe"')

        elif 'open teams' in query:
            os.system(r'"C:\Users\it\AppData\Local\Microsoft\WindowsApps\ms-teams.exe"')

        elif 'open cmd' in query:
            os.system(r'"C:\Windows\System32\cmd.exe"')

        elif 'open adobe reader' in query:
            os.system(r'"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe"')

        elif 'open camera' in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()

#-----------------IP Address--------------------------------------------#
        elif 'get ip address' in query:
            ip = get('https://api.ipify.org').text
            say(f"Sir Your IP Address is {ip}")
            print(f"Sir Your IP Address is {ip}")

#-----------------Wikipedia--------------------------------------------#
        elif "wikipedia" in query:
            say("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            say("According to Wikipedia")
            print("According to Wikipedia")
            say(results)
            print(results)

#-----------------Searching on Google--------------------------------------------#
        elif 'search on Google' in query:
            say("Sir, What should I search on Google...?")  
            print("Sir, What should I search on Google...?")  
            cm = takeCommand().lower()  
            if cm:  
                webbrowser.open(f"https://www.google.com/search?q={cm}")  

#-----------------Whatsapp--------------------------------------------#
        elif 'send message on Whatsapp' in query:
            kit.sendwhatmsg("+918882583399","This is Testing Protocol,",19,17)

#-----------------Playing Song--------------------------------------------#
        elif "play a song" in query:
            say("Which song would you like to play?")
            print("Which song would you like to play?")
            song_name = takeCommand().lower()  
            if song_name:
                kit.playonyt(song_name)  

        # elif 'send a email' in query:
        #     try:
        #         say("What should I send...?")
        #         # print("What should I send...?")
        #         content = takeCommand().lower()
        #         to = input("Enter the Email: ")
        #         sendEmail(to,content)
        #         say('The Email has been sended Sir...')
        #         print('The Email has been sended Sir...')

        #     except Exception as e:
        #         print(e)
        #         say("Sorry Sir, I am Unable to send the Email")
        #         # print("Sorry Sir, I am Unable to send the Email")

#-----------------Closing Apps--------------------------------------------#
        elif 'close notepad' in query:
            say('Okay Sir, Closing Notepad')
            os.system("taskkill /f /im notepad.exe")

        elif 'close cmd' in query:
            say('Okay Sir, Closing cmd')
            os.system("taskkill /f /im cmd.exe")

        elif 'close chrome' in query:
            say('Okay Sir, Closing Chrome')
            os.system("taskkill /f /im chrome.exe")

        elif 'close vs code' in query:
            say('Okay Sir, Closing VS Code')
            os.system("taskkill /f /im code.exe")

        elif 'close edge' in query:
            say('Okay Sir, Closing msedge')
            os.system("taskkill /f /im msedge.exe")

        elif 'close spotify' in query:
            say('Okay Sir, Closing Spotify')
            os.system("taskkill /f /im spotify.exe")
        
        elif 'close teams' in query:
            say('Okay Sir, Closing MS Teams')
            os.system("taskkill /f /im ms-teams.exe")

        elif 'close adobe reader' in query:
            say('Okay Sir, Closing Chrome')
            os.system("taskkill /f /im Acrobat.exe")

        elif 'stop alarm' in query:
            say("Okay Sir, Stopping Alarm")
            os.system("taskkill /f /im Microsoft.Media.Player.exe")

#-----------------Alarm--------------------------------------------#
        elif 'set alarm' in query:
            say("Sir, please tell me the time to set the alarm in HH:MM format.")
            alarm_time = input("Enter time: ")
            try:
                datetime.datetime.strptime(alarm_time, "%H:%M")
                set_alarm(alarm_time)
            except ValueError:
                say("Invalid time format. Please use HH:MM format.")      

#-----------------Joke--------------------------------------------#
        elif 'tell me a joke' in query:
            joke = pyjokes.get_joke()
            say(joke)

#-----------------OS Related--------------------------------------------#
        elif 'shut down the system' in query:
            say("Okay Sir, Shutting Down the System")
            os.system("shutdown /s /t 5")

        elif 'restart the system' in query:
            say("Okay Sir, Restarting the System")
            os.system("shutdown /r /t 5")

        elif 'sleep the system' in query:
            say("Okay Sir, Sleeping the System")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif 'switch window' in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")

#-----------------News--------------------------------------------#
        elif 'tell me news' in query:
            say("Please Wait Sir, Feteching the Latest News")
            news()

#--------------------Location--------------------------------------------#
        elif 'where i am' in query or 'where we are' in query:
            say("Wait Sir, Let me Check...")
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                url = 'https://get.geojs.io/v1/ip/geo'+ipAdd+'.json'
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()
                city = geo_data['city']
                country = geo_data['country']
                say(f'Sir I am not Sure, But i Think we are in {city} city of {country} country')
            except Exception as e:
                say('Sorry Sir, Due to Network issue I am not able to find where we Are...')
                pass

#-----------------Instagram--------------------------------------------#
        elif 'Instagram profile' in query or 'profile on Instagram' in query:
            say("Sir Please Enter the Name Correctly")
            name = input("Enter your Username: ")
            webbrowser.open(f"www.instagram.com/{name}")
            say(f"Sir here is the profile of the user {name}")
            time.sleep(5)
            say("Sir would you like to Download Profile Picture of this Account")
            condition = takeCommand().lower()
            if 'yes please' in condition:
                mod = instaloader.Instaloader()
                mod.download_profile(name, profile_pic_only=True)
                say("I am done Sir, Profile Picture is Saved in our Main Folder")
            else:
                pass

#-----------------Screenshot--------------------------------------------#
        elif 'take screenshot' in query or 'take a screenshot' in query:
            say("Sir,Please Tell me the name for this screenshot file")
            name = takeCommand().lower()
            say("Please Sir hold the screen for few seconds, I am screenshot")
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            say("I am Done Sir, the screenshot is saved in our main folder")

#-----------------Read PDF--------------------------------------------#
        elif 'read pdf' in query:
            pdf_reader()

#-----------------Hide Files--------------------------------------------#
        elif 'hide all files' in query or 'visible for everyone' in query:
            say('Sir, Please tell me if you want to hide this folder or make it visible for everyone')
            condition = takeCommand()
            if condition:  
                if 'hide' in condition:
                    os.system("attrib +h /s /d")
                    say("Sir, All the files in this folder are now hidden")
                elif 'visible' in condition:  
                    os.system("attrib -h /s /d")
                    say("Sir, All the files in this folder are now visible to everyone")
                elif 'leave it' in condition or 'leave for now' in condition:
                    say("Okay Sir")
            else:
                say("Sorry, I could not understand your command. Please try again.")

#-----------------Calculations--------------------------------------------#
        elif 'do some calculation' in query or 'can you calculate' in query:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                say('Say what you want to Calculate, Example 3 plus 3')
                print('Listening...')
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            my_string = r.recognize_google(audio)
            print(my_string)
            def get_operator_fn(op):
                return {
                    '+' : operator.add,
                    '-' : operator.sub,
                    'x' : operator.mul,
                    'divided' : operator.__truediv__,
                }[op]
            def eval_binary_expr(op1, oper, op2):
                op1,op2 = int(op1),int(op2)
                return get_operator_fn(oper)(op1, op2)
            say("Your Result is ")
            say(eval_binary_expr(*(my_string.split())))

#-----------------Greetings--------------------------------------------#
        elif 'hello' in query or 'hey' in query:
            say("Hello Sir , May I Help You...??")

        elif 'how are you' in query:
            say("I am Fine Sir, What about you")

        elif 'also good' in query or 'fine' in query:
            say("That's Good Sir")

        elif 'thank you' in query or "thanks" in query:
            say("It's My Please Sir...")
 
#-----------------Weather--------------------------------------------#
        elif 'tell the temperature' in query or "what is the temperature" in query:
            say("Sir Please tell the city, Example temperature in delhi")
            search = takeCommand()
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text,"html.parser")
            temp = data.find("div",class_="BNeawe").text
            say(f"Current {search} is {temp} ")

#-----------------Seach Results--------------------------------------------#
        elif 'Seach for ' in query:
            while True:
                how = takeCommand()
                say("Okay Sir, Seaching on Web")
                try:
                    if 'exit' in how or 'close' in how:
                        say('Okay Sir, Cancelling Search')
                    else:
                        max_results = 1
                        how_to = search_wikihow(how, max_results)
                        assert len(how_to) == 1
                        how_to[0].print()
                        say(how_to[0].summary)
                except Exception as e:
                    say("Sorry Sir, I am not able to find this")

#-----------------Battery Percent Check--------------------------------------------#
        elif 'how much power left' in query or 'how much power we have' in query or 'battery percentage' in query:
            battery = psutil.sensors_battery()
            percentage = battery.percent
            say(f"Sir our System have {percentage} Percent Battery left")
            if percentage>=75:
                say('We have enough Power to continue our work...')
            if percentage>=40 and percentage<=75:
                say("We don't have Enough Power to work, Please Connect to Charging")
            if percentage>=15 and percentage<=40:
                say("We don't have Enough Power to Work, Please Connect to Charger as soon as possible")
            if percentage<=15:
                say("We have very low Power left Sir, Please connect to Charger Immediately")

#-----------------Internet Speed Test--------------------------------------------#
        elif 'internet speed test' in query or 'test internet speed' in query:
            st = speedtest.Speedtest()
            dl = st.download() / 1_000_000
            up = st.upload() / 1_000_000
            say(f"Sir, We have {dl} Mbps Downloading Speed and {up} Mbps Uploading Speed")

#-----------------Message--------------------------------------------#
        # elif 'send message' in query:
            say("Sir, What Should I say...??")
            z = takeCommand()  
            account_sid = 'account_sid'
            account_token = 'account_token'
            client = Client(account_sid, account_token)
            phone_number = input("Enter the Phone Number to which you want to send the message: ")
            message = client.messages.create(
                body=z,  
                from_='phone_no',  
                to=phone_number  
            )
            print(message.sid)  
            say("Sir, Message has been sent")

#-------------------------------Calls--------------------------------------------#
        elif 'make call' in query:
            say("Sir, What Should I say...??")
            z = takeCommand()  
            account_sid = 'account_sid'
            account_token = 'account_token'
            client = Client(account_sid, account_token)
            phone_number = input("Enter the Phone Number to which you want to send the message: ")
            message = client.calls.create(
                twim='<Response><Say>This is the second testing message from Jarvis side..</Say></Response>',  
                from_='phone_number',  
                to=phone_number  
            )
            print(message.sid)  
            say("Sir, Message has been sent")

#-------------------------------Volume--------------------------------------------#
        elif 'volume up' in query:
            pyautogui.press("volumeup")
        elif 'volume down' in query:
            pyautogui.press("volumedown")
        elif 'volume mute' in query:
            pyautogui.press("volumemute")

#-----------------Closing--------------------------------------------#
        elif "you can sleep" in query:
            say("Thanks for using me Sir, have a Good Day")
            sys.exit()
        

if __name__ == '__main__':
    while True:
        permission = takeCommand()
        if permission:  
            if 'wake up' in permission:
                TaskExecution()
            elif 'goodbye' in permission:
                say("Thanks for using me Sir, have a Good Day..!!")
                sys.exit()
        else:
            say("Could not understand the command. Please try again.") 