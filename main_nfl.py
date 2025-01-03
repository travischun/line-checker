
import ssl
import sys
from pymongo import MongoClient
from oddSharkConsensus import oddSharkConensus
from sendMessage import send_message
from sendEmail import send_email

from caesarsNFLApiLineChecker import formatDateTime
from consensusChecker import scoresandoddsConsensusCheck
from consensusScoresAPIChecker import scoresandoddsAPIConsensusCheck, formatDate
from mongoDB import setupDatabase, checkCollection, createCollection, printCollection, compareCollection
import time
import schedule
from datetime import datetime
from dateutil import tz
import unicodedata

testConsensusData = {'12182023-19:15-PhiladelphiaEaglesvsSeattleSeahawks': {'Away': {'Team': 'Philadelphia Eagles', 'Consensus': '67'}, 'Home': {'Team': 'Seattle Seahawks', 'Consensus': '33'}, 'gameTime': '12/18 7:15PM'},'12252023-15:30-NewYorkGiantsvsPhiladelphiaEagles': {'gameTime': 'Dec 25 3:30pm', 'Away': {'Team': 'New York Giants', 'Consensus': '50'}, 'Home': {'Team': 'Philadelphia Eagles', 'Consensus': '50'}}, '12252023-19:15-BaltimoreRavensvsSanFrancisco49ers': {'gameTime': 'Dec 25 7:15pm', 'Away': {'Team': 'Baltimore Ravens', 'Consensus': '65'}, 'Home': {'Team': 'San Francisco 49ers', 'Consensus': '35'}}}
testLineData = {'12182023-19:15-PhiladelphiaEaglesvsSeattleSeahawks': {'gameTime': 'Dec 18 7:15pm', 'Away': {'Team': 'Philadelphia Eagles', 'Line': '-4.5-110'}, 'Home': {'Team': 'Seattle Seahawks', 'Line': '+4.5-110'}},'12252023-15:30-NewYorkGiantsvsPhiladelphiaEagles': {'gameTime': 'Dec 25 3:30pm', 'Away': {'Team': 'New York Giants', 'Line': '+11.5-110'}, 'Home': {'Team': 'Philadelphia Eagles', 'Line': '-11.5-110'}}, '12252023-19:15-BaltimoreRavensvsSanFrancisco49ers': {'gameTime': 'Dec 25 7:15pm', 'Away': {'Team': 'Baltimore Ravens', 'Line': '+5.5-110'}, 'Home': {'Team': 'San Francisco 49ers', 'Line': '-5.5-110'}}}

year = "2024"
URL = "https://www.scoresandodds.com/nfl/consensus-picks"

teamCodes = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAC', 'KC', 'LAC', 'LA', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG', 'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WAS']

nfl_teams = {"DEN": "Denver Broncos","KC":"Kansas City Chiefs","BAL":"Baltimore Ravens","TEN":"Tennessee Titans","WAS":"Washington Commanders","ATL":"Atlanta Falcons","CAR":"Carolina Panthers","MIA":"Miami Dolphins","NO":"New Orleans Saints","HOU":"Houston Texans","SEA":"Seattle Seahawks","CIN":"Cincinnati Bengals","IND":"Indianapolis Colts","JAC":"Jacksonville Jaguars","SF":"San Francisco 49ers","CLE":"Cleveland Browns","MIN":"Minnesota Vikings","CHI":"Chicago Bears","NE":"New England Patriots","LV":"Las Vegas Raiders","DET":"Detroit Lions","TB":"Tampa Bay Buccaneers","PHI":"Philadelphia Eagles","NYJ":"New York Jets","ARI":"Arizona Cardinals","LA":"Los Angeles Rams","NYG":"New York Giants","BUF":"Buffalo Bills","DAL":"Dallas Cowboys","LAC":"Los Angeles Chargers","PIT":"Pittsburgh Steelers","GB":"Green Bay Packers"}



now = datetime.now()

subject = "NFL Odds for " + now.strftime("%d %b, %Y")
sender = "travis.chun13@gmail.com"
recipients = ["h.andrew.vo@gmail.com", "travis.chun13@gmail.com"]


EMAIL = "travis.chun13@gmail.com"
PASSWORD = sys.argv[1]
#Andrew
phone_number = "2145544438"
#Travis
phone_number2 = "9722077596"

def consolidateData(db, lineData, consensusData):
    for key in consensusData:
        print('Checking key: ' + key)
        exists = checkCollection(db,key)
        if exists:
            print('Checking for new changes to line/consensus')
            lineData[key]["_id"] = key
            lineData[key]["Away"]["Consensus"] = consensusData[key]["Away"]["Consensus"]
            lineData[key]["Home"]["Consensus"] = consensusData[key]["Home"]["Consensus"]

            compareCollection(db, key, lineData[key], now.strftime("%m/%d/%Y %I:%M %p"))
        else:
            lineData[key]["_id"] = key
            lineData[key]["Away"]["Consensus"] = consensusData[key]["Away"]["Consensus"]
            lineData[key]["Home"]["Consensus"] = consensusData[key]["Home"]["Consensus"]

            lineData[key]["Away"]["OpeningLine"] = lineData[key]["Away"]["Line"]
            lineData[key]["Home"]["OpeningLine"] = lineData[key]["Home"]["Line"]
            lineData[key]["LineMovement"] = [ {
                "time": now.strftime("%m/%d/%Y %I:%M %p"),
                "homeTeam": lineData[key]["Home"]["Team"],
                "homeLine": lineData[key]["Home"]["Line"],
                "awayTeam": lineData[key]["Away"]["Team"],
                "awayLine": lineData[key]["Away"]["Line"]
            }]
            # del lineData[key]["Home"]["Line"]
            # del lineData[key]["Away"]["Line"]

            createCollection(db, key, lineData[key])

    #printCollection(db,key)

def generateMessage(consensus):
    finalStr = ""
    print(consensus)
    for game in consensus:
        # print(game)
        formattedDate = formatDateTime(game['gameTime'],"date")
        formattedTime = formatDateTime(game['gameTime'],"time")
        
        string = "\n------------------------\n" + formattedDate + "\n" + formattedTime + "\n" + "Home: " + game["Home"]["Team"] + "\n" + "Line: " + game["Home"]["Line"] + "\n" + "Consensus: " + game["Home"]["Consensus"] + "%\n" + game["Away"]["Team"] + "\n" + "Line: " + game["Away"]["Line"] + "\nConsensus: " + game["Away"]["Consensus"] + "%\n"

        finalStr = finalStr + string

    return finalStr

    
def grabLinesAndConsensus():
    # message,arrGames = caesarsLineCheckerNFL()
    consensus = scoresandoddsAPIConsensusCheck(year, URL, nfl_teams, teamCodes)
    message = generateMessage(consensus)
    # print(consensus)
    # print(arrGames)
    
    # send_message(phone_number,message,EMAIL,PASSWORD)

    # db = setupDatabase('nfl2023')
    # consolidateData(db, arrGames,consensus)
    # print(message)
    return message

message = grabLinesAndConsensus()
print(message)
# send_message(phone_number,message,EMAIL,PASSWORD)
normalize_message = unicodedata.normalize("NFKD", message)
send_message(phone_number,normalize_message,EMAIL,PASSWORD)
send_message(phone_number2,normalize_message,EMAIL,PASSWORD)

# send_email(subject, message, sender, recipients, PASSWORD)
    

# send_message(phone_number,message,EMAIL,PASSWORD)
# send_message(phone_number2,message,EMAIL,PASSWORD)

# send_email(subject, message, sender, recipients, PASSWORD)


#myClient = MongoClient("192.168.1.97", 27017)
#db = myClient["local"]
#collection = db["MLB"]

#collection.insert_many(arrGames)

#print(concatStr)
