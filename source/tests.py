from coursework.py import *

readConfig()


# test for API data fetch for Covid
def testcovidDataTest:
    f = assert covidDataFetch != None
    return f
#test for Covid Data handling
def testcovidDataHandling:
    f = assert covidDataHandling(covidDataFetch()) != None
    return f
#test for weather API
def testweatherFetch:
    f = assert weatherFetch(city = "exeter", key = "e74f7af941e8c442774d418d9089b2f5") != None
    return f
#test for weather data handling
def testweatherDataHandling:
    f = assert weatherDataHandling(weatherFetch(city = "exeter", key = "e74f7af941e8c442774d418d9089b2f5")) != None
    return f
#test for news API
def newsDataFetch:
    f = assert newsDataFetch(countryCode = "gb",keyword = "Covid",key = "c4eaf87010e74ab8a6ba86f7a8bc4afe") != None
    return f
#test for news API handling
def testnewsDataHandling:
    f = assert newsDataHandling(newsDataFetch(countryCode = "gb",keyword = "Covid",key = "c4eaf87010e74ab8a6ba86f7a8bc4afe")) != None
    return f
#test to see if the notification get funxtion works
def createNotification:
    f = assert createNotification("title", "content") != None
    return f
