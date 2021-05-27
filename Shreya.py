import pyttsx3                      #pip install pyttsx3
import speech_recognition as sr     #pip install speechRecognition
import datetime
import wikipedia                    #pip install wikipedia
import webbrowser
import os
import smtplib                      #for gmail
import sys
import random
import googlesearch
import wolframalpha                 #for computational knowlegde
import geopy.geocoders              #For latitude and longitude of a location
import requests                     #To get json data with API request

#initalise recognizer
r = sr.Recognizer()

#initialise voice to speak
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)       	#Voice property.
engine.setProperty('rate', 142)				#Voice speaking speed

#data of people as dictionary where key is name and mobile number and email-id are attributes.
database = {                                                         #{ "name" : ["Mobile Number", "Email-ID"] }
    "rahul" : [7733988516, "ishreynish@gmail.com"]
    }

#initialise to find longitude and latitude of a location
geolocator = geopy.geocoders.Nominatim(user_agent="Shreya")

#actions through some functions
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    speak("Hello, I am Shreya. Your voice assistant.")

def takeCommand():
    #It takes microphone input from the user and returns string output
    while True:
        with sr.Microphone() as mic:
            print("Listening...")
            r.adjust_for_ambient_noise(mic)
            audio = r.listen(mic)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception:
            print("Say that again please...")
            continue
        return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('royalnishant272@gmail.com', '8432727820@')	#To login into your account.
    server.sendmail('You Email-ID', to, content)	        #To send mail
    server.quit()

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'how are you' in query:
            speak('I am fine. Thanks for asking. What can I do for you?')

        elif 'good bye shreya' in query:
            speak('Goodbye')
            speak('Take Care!')
            sys.exit()

        #time feature
        elif 'what time is it' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"The time is {strTime}")
            speak(f"The time is {strTime}")

        #music features
        elif 'play music' in query or 'change music' in query:
            music_dir = "D:\Music"
            songs = os.listdir(music_dir)
            n_songs = len(songs)
            n_num = random.randint(0,n_songs)
            os.startfile(os.path.join(music_dir, songs[n_num]))
                        
        #weather report
        elif 'weather report' in query:
            speak('Tell me location.')		#Asking for a particular location.
            place = takeCommand().lower()

            loc = geolocator.geocode(place)
            url = 'https://api.darksky.net/forecast/6b198356322c5b43f9037a87ba4f60a7/'+str(loc.latitude)+','+str(loc.longitude) #You have to register at darksky.net to avail the API
            json_data = requests.get(url).json()
            #engine.setProperty('rate', 120)

            t_temp = json_data['currently']['temperature']
            temp = round( (t_temp - 32) * 5/9, 2)
            print('Temperature is ', temp ,chr(176), ' Celcius.', sep='')
            speak('Temperature is '+str(temp)+' degree celcius.')

            t_humid = json_data['currently']['humidity']
            humid = str(t_humid*100) + '%'
            print('Humidity is '+humid)
            speak('Humidity is '+humid)

            dscrp_weather = json_data['currently']['summary']
            print('Weather condition is '+dscrp_weather)
            speak('Weather condition is '+dscrp_weather)

            summary_weather = json_data['hourly']['summary']
            print(summary_weather)
            speak(summary_weather)

        #e-mail feature
        elif 'compose an email' in query:
            speak('to whom')
            person = takeCommand().lower()
            if person == 'to all':
                try:
                    speak("What should I say to all?")
                    content = takeCommand().lower()
                    for key in database:					
                        to = database[key][1]
                        sendEmail(to, content)
                        speak("Email has been sent!")
                except Exception as e:
                    print(e)
                    speak("Sorry, I am not able to send this email")
            else:
                try:
                    speak("What should I say?")
                    content = takeCommand()
                    to = database[person][1]
                    sendEmail(to, content)
                    speak("Email has been sent!")
                except Exception as e:
                    print(e)
                    speak("Sorry, I am not able to send this email")

        #find phone no.
        elif 'find a phone number' in query:
            speak('tell me name of that person')
            person = takeCommand().lower()
            engine.setProperty('rate', 20)
            speak(database[person][0])				#Will pick up from the database

        #youtube
        elif 'open youtube' in query:
            webbrowser.open("https://youtube.com/")

        #google
        elif 'google search' in query:
            speak('about what')
            query = takeCommand().lower()
            url = googlesearch.search(query, stop=5, pause=2)
            speak(url)

        #wolframalpha
        elif 'i have a question' in query or "i have another question" in query:
            speak('Tell me, what is it?')
            question = takeCommand().lower()

            app_id = "WGLEKG-LRA3Y9JE5G"
            client = wolframalpha.Client(app_id)
            res = client.query(question)
            answer = next(res.results).text
            print(answer)
            engine.setProperty('rate', 120)
            speak(answer)
