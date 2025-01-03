import requests
import csv
import time
import datetime
from dateutil import tz
teamNames = ["Arizona Diamondbacks","Atlanta Braves","Baltimore Orioles","Boston Red Sox","Chicago White Sox","Chicago Cubs","Cincinnati Reds","Cleveland Guardians","Colorado Rockies","Detroit Tigers","Houston Astros","Kansas City Royals","Los Angeles Angels","Los Angeles Dodgers","Miami Marlins","Milwaukee Brewers","Minnesota Twins","New York Yankees","New York Mets","Oakland Athletics","Philadelphia Phillies","Pittsburgh Pirates","San Diego Padres","San Francisco Giants","Seattle Mariners","St. Louis Cardinals","Tampa Bay Rays","Texas Rangers","Toronto Blue Jays","Washington Nationals"]


headers = { 
    "user-agent": "MozillebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
}

def formatDateTime(date,selection):
    from_zone = tz.gettz("UTC")
    to_zone = tz.gettz("America/Chicago")
    dateObject = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    utc = dateObject.replace(tzinfo=from_zone)
    cst = utc.astimezone(to_zone)
    if selection == "date":
        return cst.strftime('%m/%d/%Y')
    elif selection == "time":
        return cst.strftime('%I:%M%p')
    elif selection == "file":
        return cst.strftime('%m_%d_%Y')
    else:
        return cst.strftime('%m/%d/%Y @ %I:%M%p')

def caesarsApiLineChecker(URL):
    fileName = ""
    response = requests.get(URL, headers=headers)
    print(response)
    GamesArray = []

    payload = response.json()
    # for index in payload:
    for mlb in payload["competitions"]:
        if mlb["name"] == "MLB":
            for event in mlb["events"]:
                mlbgame = False
                for team in teamNames:
                    if team in event["name"]:
                        mlbgame = True
                        break
                if mlbgame:
                    eventMap = {}
                    eventArr =[]
                    homeML = 0
                    awayML = 0
                    eventMap["Date"] = formatDateTime(event["startTime"],"date")
                    eventMap["Time"] = formatDateTime(event["startTime"],"time")
                    fileName = formatDateTime(event["startTime"],"file")
                    eventMap["EventName"] = event["name"].replace("|","")
                    liveGame = True
                    for market in event["markets"]:
                        if market["name"] == "|Money Line|":
                            liveGame = False
                            for selection in market["selections"]:
                                if selection["type"] == "home":
                                    eventMap["HomeTeam"] = selection["teamData"]["teamName"]
                                    homeML = selection["price"]["a"]
                                    if selection["price"]["a"] > 0:
                                        eventMap["HomeML"] = "+" + str(selection["price"]["a"])
                                    else:
                                        eventMap["HomeML"] = str(selection["price"]["a"])
                                elif selection["type"] == "away":
                                    eventMap["AwayTeam"] = selection["teamData"]["teamName"]
                                    awayML = selection["price"]["a"]
                                    if selection["price"]["a"] > 0:
                                        eventMap["AwayML"] = "+" + str(selection["price"]["a"])
                                    else:
                                        eventMap["AwayML"] = str(selection["price"]["a"])    
                    # print(eventMap)
                    if not liveGame:
                        GamesArray.append(eventMap)
    return GamesArray



