
import ssl
import sys
from pymongo import MongoClient
from oddSharkConsensus import oddSharkConensus
from sendMessage import send_message
from sendEmail import send_email

from caesarsLineCheckerNFL import caesarsLineCheckerNFL
from consensusChecker import scoresandoddsConsensusCheck
from mongoDB import setupDatabase, checkCollection, createCollection,printCollection
import time

from datetime import datetime


testConsensusData = {'12182023-19:15-PhiladelphiaEaglesvsSeattleSeahawks': {'Away': {'Team': 'Philadelphia Eagles', 'Consensus': '67'}, 'Home': {'Team': 'Seattle Seahawks', 'Consensus': '33'}, 'gameTime': '12/18 7:15PM'},'12252023-15:30-NewYorkGiantsvsPhiladelphiaEagles': {'gameTime': 'Dec 25 3:30pm', 'Away': {'Team': 'New York Giants', 'Consensus': '50'}, 'Home': {'Team': 'Philadelphia Eagles', 'Consensus': '50'}}, '12252023-19:15-BaltimoreRavensvsSanFrancisco49ers': {'gameTime': 'Dec 25 7:15pm', 'Away': {'Team': 'Baltimore Ravens', 'Consensus': '75'}, 'Home': {'Team': 'San Francisco 49ers', 'Consensus': '25'}}}
testLineData = {'12182023-19:15-PhiladelphiaEaglesvsSeattleSeahawks': {'gameTime': 'Dec 18 7:15pm', 'Away': {'Team': 'Philadelphia Eagles', 'Line': '-3.5-110'}, 'Home': {'Team': 'Seattle Seahawks', 'Line': '+3.5-110'}},'12252023-15:30-NewYorkGiantsvsPhiladelphiaEagles': {'gameTime': 'Dec 25 3:30pm', 'Away': {'Team': 'New York Giants', 'Line': '+10.5-110'}, 'Home': {'Team': 'Philadelphia Eagles', 'Line': '-10.5-110'}}, '12252023-19:15-BaltimoreRavensvsSanFrancisco49ers': {'gameTime': 'Dec 25 7:15pm', 'Away': {'Team': 'Baltimore Ravens', 'Line': '+5.5-110'}, 'Home': {'Team': 'San Francisco 49ers', 'Line': '-5.5-110'}}}



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
            print('nothing to do')
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

    printCollection(db,key)
# message,arrGames = caesarsLineCheckerNFL()
# consensus = scoresandoddsConsensusCheck()
db = setupDatabase('nfl2023')
consolidateData(db, testLineData,testConsensusData)
# print(consensus)
# print(arrGames)



#myClient = MongoClient("192.168.1.97", 27017)
#db = myClient["local"]
#collection = db["MLB"]

#collection.insert_many(arrGames)

#print(concatStr)
# send_message(phone_number,message,EMAIL,PASSWORD)
# send_message(phone_number2,message,EMAIL,PASSWORD)

# send_email(subject, message, sender, recipients, PASSWORD)
