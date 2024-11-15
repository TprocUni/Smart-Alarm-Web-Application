from uk_covid19 import Cov19API
import requests
from flask import Markup

#covid data fetching
def covidDataFetch():
    #parameter defining location
    england_only = [
        'areaType=nation',
        'areaName=England']
    #parameter defining information we are requesting
    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeathsByDeathDate": "newDeathsByDeathDate",
        "cumDeathsByDeathDate": "cumDeathsByDeathDate"}
    #requesting data from API
    api = Cov19API(filters=england_only, structure=cases_and_deaths)
    #json ing the data so its usable
    data = api.get_json()
    return data["data"]

#covid data handling
def covidDataHandling(covidData):
    #variable definition, taken from the data aquired from covidDataFetch()
    today = covidData[0]
    yesterday = covidData[1]
    areaName = today["areaName"]
    yesterdayDeaths = yesterday["newDeathsByDeathDate"]
    newCases = today["newCasesByPublishDate"]
    cumulativeCases = today["cumCasesByPublishDate"]
    cumulativeDeaths = yesterday["cumDeathsByDeathDate"]
    #calculates highest deaths in one day from available data and compares it to todays death toll
    covidData.pop(0)
    highestDeaths = 0
    #checking all available data
    for i in covidData:
        if i["newDeathsByDeathDate"] == None:
            pass
        elif i["newDeathsByDeathDate"] > highestDeaths:
            highestDeaths = i["newDeathsByDeathDate"]
    difference = highestDeaths -  yesterdayDeaths
    #If the number of cases today is greater than previous records we must flip its sign otherwise it will be negative
    if difference <= 0:
        caseDifference = (f"Today had the highest number of deaths in the past month ({difference*-1}.)")
    else:
        caseDifference = (f"Today we had {difference} fewer cases than our max in the past month.")
    #formatting for string that will be passed to main function
    covidUpdateString = (f'''
Daily Covid-19 update:
In {areaName} there have been {newCases} new cases, bringing the total up to {cumulativeCases}.
Yesterday there was {yesterdayDeaths} deaths, bringing the total up to {cumulativeDeaths} deaths.
    ''')+caseDifference
    return (covidUpdateString)



#weather data fetching
def weatherFetch(city = "exeter", key = "e74f7af941e8c442774d418d9089b2f5"):
    #Allows for customizable API key and weather location.
    baseURL = "http://api.openweathermap.org/data/2.5/weather?q="
    city = str(city)
    key = str("&appid=" + key + "&units=metric")
    completeURL = baseURL + city + key
    #requests the data from the weather API, and stores it within weatherAPI
    weatherAPI = requests.get(completeURL)
    #Json's the data so we can use it for the weatherDataHandling() function.
    weather = weatherAPI.json()
    return (weather)

def weatherDataHandling(weatherData):
    #variable definition, taken from the data aquired from weatherFetch()
    location = weatherData["name"]
    weather = weatherData["weather"][0]["description"]
    windSpeed = weatherData["wind"]["speed"]
    temp = weatherData["main"]["temp"]
    tempMin = weatherData["main"]["temp_min"]
    tempMax = weatherData["main"]["temp_max"]
    #preperation for extra messages if weather is unexpected
    extra = ""
    #for lower temperatures
    if temp < 12:
        extra = ("You better bring an extra layer")
    elif temp > 25:
        extra = ("Its t-shirt weather")
    #for high winds (7+ on Beaufort scale)
    if windSpeed > 32:
        if extra != "":
            extra += (", there are also high winds so be prepared")
        else:
            ("There are high winds today")
    #checking if the word rain will appear in the string returned with weather
    if "rain" in weather.lower():
        if extra != "":
            extra += ("and there will be rain :(")
        else:
            ("It will rain")
    extra += "."
    #formatting for string that will be passed to main function
    weatherUpdateString = (f'''
Daily weather update:
Location: {location}
Weather: {weather}
Wind speed: {windSpeed}kmph
Temperature: {tempMin}° - {tempMax}°, averaging {temp}°
''')+extra
    return (weatherUpdateString)



#news data fetching
def newsDataFetch(countryCode = "gb",keyword = "Covid",key = "c4eaf87010e74ab8a6ba86f7a8bc4afe"):
    #Allows for customizable API key, country, and keyword (for search queries)
    url = ('http://newsapi.org/v2/top-headlines?'
           f'country={countryCode}&'
           f'q={keyword}&'
           'from=2020-12-01&'
           'sortBy=popularity&'
           f'apiKey={key}')
    #do I really have to tell you what this does (hint: same as before, and before that)
    news = requests.get(url).json()
    return (news["articles"])

#news data handling
def newsDataHandling(newsData):
    #basically this was written by an AI (me) and I wanna see if you notice me (aside from that it does the same as the others)
    source = newsData["source"]["name"]
    author = newsData["author"]
    title = newsData["title"]
    description = newsData["description"]
    URL = newsData["url"]
    URL2 = (f'<a href="{URL}">{title}</a>')
    #beep boop string formatting time
    newsString = Markup((f'''
{URL2}
{source}: {author}\n
{description}'''))
    return newsString
