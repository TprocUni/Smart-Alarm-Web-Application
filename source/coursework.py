#Smart alarm webpage, author: Ted Proctor, Webpage template by the big man himself MATT COLLINSON

from time_conversions import *
import time
import sched
import pyttsx3
from API_phile import *
from flask import render_template
from flask import Flask
from flask import request
import requests
import logging
import json

#imports private data from config.json file
def readConfig():
    #defines global variabeles for use for sensitive information accross the code
    global loggingPath, weatherLocation, weatherKey, newsLocation, newsKeyTerm, newsKey, IMGPath
    with open("config.json") as configdata:
        data = json.load(configdata)
    #converts to a data structure
    loggingPath = data["loggingPath"]
    weatherLocation = data["weatherLocation"]
    weatherKey = data["weatherKey"]
    newsLocation = data["newsLocation"]
    newsKeyTerm = data["newsKeyTerm"]
    newsKey = data["newsKey"]
    IMGPath = data["IMGPath"]
#imports private data from config.json file
readConfig()


#logging data
#this formats the data that is written to the txt file
FORMAT = "%(levelname)s,%(asctime)s,%(message)s"
logging.basicConfig(filename = loggingPath, level = logging.DEBUG,format = FORMAT)
#each of these display a message associated with a threat level.
logging.debug("...")
logging.info("minor issue")
logging.warning("issue")
logging.error("major issue, likely program shutdown")



#array assignment fundamental to the coding project
announcements = []
notifications = []
allNotifications = []
lastLabel = "hello there"

app = Flask(__name__)
engine = pyttsx3.init()
s = sched.scheduler(time.time, time.sleep)



# this function will take a ready-made string and put it into a format that can be uploaded to the site
def createNotification (title, content):
    notificationDict = {"title" : title, "content" : content}
    return notificationDict


#function to remove notifications from the list
def delNotification():
    #This function checks if the user closed a notification and removes it from the list if they did
    #Finds name of closed notification
    closedNotification = request.args.get("notif")
    #Resets counter
    for notification in notifications:
        if notification["title"] == closedNotification:
             notifications.remove(notification)
        else:
            pass

#funtion to add notifications to the notification hotbar
def generateNotification():
    newNotifications = []
    #these command generate a notification for weather and a covid update
    weatherNotificationContent = createNotification("Weather notification", weatherDataHandling(weatherFetch(weatherLocation, weatherKey)))
    covidNotificationContent = createNotification("Covid notification", covidDataHandling(covidDataFetch()))
    newNotifications.append(weatherNotificationContent)
    newNotifications.append(covidNotificationContent)
    #iterating through each article to put it into a notification format, and adding it to the newNotifications array
    newsData = newsDataFetch(newsLocation,newsKeyTerm,newsKey)
    for i in range(len(newsData)):
        h = createNotification((f"Newsflash {i+1}"),newsDataHandling(newsData[i]))
        newNotifications.append(h)
    newNewNotifications = newNotifications
    for i in newNotifications:
        for j in allNotifications:
            if i["title"] == j["title"]:
                newNewNotifications.remove(i)
    for i in newNewNotifications:
        notifications.append(i)
        allNotifications.append(i)
    #if this content has already been used - dont add


#function to collect data about user input for alarms
def generateAlarm():
    global alarmTime, alarmLabel, alarmNews, alarmWeather
    alarmTime = request.args.get("alarm")
    alarmLabel = request.args.get("two")
    alarmNews = request.args.get("news")
    alarmWeather = request.args.get("weather")
    #for later use for this data
    lastLabel = alarmLabel

#prepares alarm data to be presented on the webpage
def displayAlarm():
    #opens the .json file we need to read form
    f = open("Announcements.json","r")
    for line in f:
        #ensures the line has content so no errors occur
        if line != "":
            i = json.loads(line)
            #setting variables and values
            alarmTemplate = {}
            alarmTime = i["alarmTime"]
            alarmLabel = i["alarmLabel"]
            alarmTemplate["title"]  = i["alarmLabel"]
            alarmNews = i["alarmNews"]
            alarmWeather = i["alarmWeather"]
            #string formatting
            str1 = (f"Time set: {alarmTime}\n")
            #set of logic staements to determine which out of news and weather (or both) are added onto the end of the announcement
            if alarmNews == "news" and alarmWeather == "weather":
                str1 += "News and weather notifications enabled"
            elif alarmNews == "news":
                str1 += "News notifications enabled"
            elif alarmWeather == "weather":
                str1 += "Weather notifications enabled"
            else:
                pass
            #formatting the final string so its more readable
            alarmTemplate["content"] = str1
            presence = False
            #ensuring its not a repeat announcement
            for i in announcements:
                if i["content"] == alarmTemplate["content"]:
                    presence = True
            if presence == False:
                announcements.append(alarmTemplate)
    f.close()

#function to save each alarm to a database
def saveAlarm():
    #opening the .json file we want to write to
    with open("Announcements.json", "a") as f:
        #creating a dictionary with all the necessary information
        newAlarm = {}
        newAlarm["alarmTime"] = alarmTime
        newAlarm["alarmLabel"] = alarmLabel
        newAlarm["alarmNews"] = alarmNews
        newAlarm["alarmWeather"] = alarmWeather
        lastLabel = alarmLabel
        #'dumps' the dictionary in the database
        json.dump(newAlarm,f)
        #newline so data is nicely formatted
        f.write("\n")

def scheduler():
    displayAlarm()
    #convert alarm_time to a delay
    alarm_hhmm = alarmTime[-5:-3] + ':' + alarmTime[-2:]
    delay = hhmm_to_seconds(alarm_hhmm) - hhmm_to_seconds(current_time_hhmm())
    passOnLabel = alarmLabel
    passOnNews = alarmNews
    passOnWeather = alarmWeather
    s.enter(delay, 1, lambda: announce(passOnLabel,passOnNews,passOnWeather))




#allows the user to remove alarms from their list of alarms
def delAlarm():
    #opens the announcements.json file to take its data then close it
    f = open("Announcements.json","r")
    data = f.readlines()
    f.close()
    #fetching whether a cross has been clicked
    closedAlarm = request.args.get("alarm_item")
    #removes the crossed item if it exists in announcements
    for i in announcements:
        if i["title"] == closedAlarm:
            announcements.remove(i)
    #reformats the announcements.json file
    f = open("Announcements.json","w")
    for i in data:
        line = json.loads(i)
        if line["alarmLabel"] != closedAlarm and i.strip("\n") != "\n":
            f.write(i)
    f.close()


#tts the announcement
def announce(announcement,news,weather):
    mainString = announcementStructured(announcement,news,weather)
    #checks if its time to tts
    try:
        engine.endLoop()
    except:
        pass
    #formatting mainString
    print(type(mainString))
    print("2", mainString)
    mainString = (str(mainString)).replace("\n", "")
    #tts process
    engine.say(mainString)
    engine.runAndWait()

#requests certain data from the webpage
def getFromPage(targetData):
     return request.args.get(targetData)

#used to modify the mainString so that it includes weather and news data if needs be.
def announcementStructured(announcement,news,weather):
    mainString = "".join(announcement)
    #fetching weather and news data
    weatherData = weatherDataHandling(weatherFetch(weatherLocation, weatherKey))
    newsData = newsDataFetch(newsLocation,newsKeyTerm,newsKey)[0]["title"]
    #checking which out of news, weather or both must be added onto the end of mainString
    if news == "news" and weather == "weather":
        mainString += (". ", str(weatherData))
        mainString += (". ", str(newsData))
    elif news == "news":
        mainString += (". ",str(newsData))
    elif weather == "weather":
        mainString = (". ",str(weatherData))
    else:
        pass
    #string manipulation
    mainString = str(mainString).replace("\n", "")
    return mainString




@app.route('/')
@app.route("/index")
#main function
def render():
    global lastLabel
    lastLabel = "hello there"
    generateAlarm()
    displayAlarm()
    generateNotification()
    s.run(blocking=False)
    if alarmTime != None:
        saveAlarm()
        scheduler()
    delAlarm()
    delNotification()

    #sends the data to the screen every 60 seconds with an updated frame
    return render_template('index.html', title='Smart Alarm', notifications=notifications, alarms = announcements, image = IMGPath)

#runs the code
if __name__ == '__main__':
    app.run()
