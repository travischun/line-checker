import requests
import csv
import time
import datetime
from dateutil import tz
teamNames = ['Atlanta Hawks', 'Boston Celtics', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Brooklyn Nets', 'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'San Antonio Spurs', 'Sacramento Kings', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards']


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
    #print(response.json())
    GamesArray = []

    payload = response.json()
    for index in payload:
        for nba in index["competitions"]:
            if nba["name"] == "NBA":
                for event in nba["events"]:
                    nbagame = False
                    for team in teamNames:
                        if team in event["name"]:
                            nbagame = True
                            break
                    if nbagame:
                        eventMap = {}
                        eventArr =[]
                        homeML = 0
                        awayML = 0
                        eventMap["Date"] = formatDateTime(event["startTime"],"date")
                        eventMap["Time"] = formatDateTime(event["startTime"],"time")
                        fileName = formatDateTime(event["startTime"],"file")
                        eventMap["EventName"] = event["name"].replace("|","")
                        for market in event["markets"]:
                            if market["name"] == "|Money Line|":
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
                            elif market["name"] == "|Spread|":
                                for selection in market["selections"]:
                                    if homeML < 0:
                                        eventMap["HomeSpread"] = market["line"]
                                        eventMap["AwaySpread"] = market["line"] * -1
                                    elif awayML < 0:
                                        eventMap["AwaySpread"] = market["line"]
                                        eventMap["HomeSpread"] = market["line"] * -1                                
                            elif market["name"] == "|Total Points|":
                                eventMap["Total"] = market["line"]
                        # print(eventMap)
                        GamesArray.append(eventMap)
    return GamesArray



