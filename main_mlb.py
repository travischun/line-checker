
import ssl
import sys
from pymongo import MongoClient
from oddSharkConsensus import oddSharkConensus
from sendMessage import send_message
from sendEmail import send_email

from caesarsLineCheckerGeneric import caesarsLineCheckerGeneric
from consensusChecker import scoresandoddsConsensusCheck
from caesarsMLBApiLineChecker import caesarsApiLineChecker
from mongoDB import setupDatabase, checkCollection, createCollection, printCollection, compareCollection
import time
import schedule
from datetime import datetime


testConsensusData = {'12182023-19:15-PhiladelphiaEaglesvsSeattleSeahawks': {'Away': {'Team': 'Philadelphia Eagles', 'Consensus': '67'}, 'Home': {'Team': 'Seattle Seahawks', 'Consensus': '33'}, 'gameTime': '12/18 7:15PM'},'12252023-15:30-NewYorkGiantsvsPhiladelphiaEagles': {'gameTime': 'Dec 25 3:30pm', 'Away': {'Team': 'New York Giants', 'Consensus': '50'}, 'Home': {'Team': 'Philadelphia Eagles', 'Consensus': '50'}}, '12252023-19:15-BaltimoreRavensvsSanFrancisco49ers': {'gameTime': 'Dec 25 7:15pm', 'Away': {'Team': 'Baltimore Ravens', 'Consensus': '65'}, 'Home': {'Team': 'San Francisco 49ers', 'Consensus': '35'}}}
testLineData = {'12182023-19:15-PhiladelphiaEaglesvsSeattleSeahawks': {'gameTime': 'Dec 18 7:15pm', 'Away': {'Team': 'Philadelphia Eagles', 'Line': '-4.5-110'}, 'Home': {'Team': 'Seattle Seahawks', 'Line': '+4.5-110'}},'12252023-15:30-NewYorkGiantsvsPhiladelphiaEagles': {'gameTime': 'Dec 25 3:30pm', 'Away': {'Team': 'New York Giants', 'Line': '+11.5-110'}, 'Home': {'Team': 'Philadelphia Eagles', 'Line': '-11.5-110'}}, '12252023-19:15-BaltimoreRavensvsSanFrancisco49ers': {'gameTime': 'Dec 25 7:15pm', 'Away': {'Team': 'Baltimore Ravens', 'Line': '+5.5-110'}, 'Home': {'Team': 'San Francisco 49ers', 'Line': '-5.5-110'}}}

year = "2024"
Consensus_URL = "https://www.scoresandodds.com/nba/consensus-picks"
Caesars_URL = "https://sportsbook.caesars.com/us/ma/bet/basketball?id=5806c896-4eec-4de1-874f-afed93114b8c"

teamCodes = ['ATL', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GS', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NO', 'NY', 'BKN', 'OKC', 'ORL', 'PHI', 'PHO', 'POR','SA', 'SAC', 'TOR', 'UTA', 'WAS']

nba_teams = {'ATL': 'Atlanta Hawks', 'BOS': 'Boston Celtics', 'CHA': 'Charlotte Hornets', 'CHI': 'Chicago Bulls', 'CLE': 'Cleveland Cavaliers', 'DAL': 'Dallas Mavericks', 'DEN': 'Denver Nuggets', 'DET': 'Detroit Pistons', 'GS': 'Golden State Warriors', 'HOU': 'Houston Rockets', 'IND': 'Indiana Pacers', 'LAC': 'Los Angeles Clippers', 'LAL': 'Los Angeles Lakers', 'MEM': 'Memphis Grizzlies', 'MIA': 'Miami Heat', 'MIL': 'Milwaukee Bucks', 'MIN': 'Minnesota Timberwolves', 'NO': 'New Orleans Pelicans', 'NY': 'New York Knicks', 'BKN': 'Brooklyn Nets', 'OKC': 'Oklahoma City Thunder', 'ORL': 'Orlando Magic', 'PHI': 'Philadelphia 76ers', 'PHO': 'Phoenix Suns', 'POR': 'Portland Trail Blazers', 'SAC': 'Sacramento Kings', 'SA':'San Antonio Spurs','TOR': 'Toronto Raptors', 'UTA': 'Utah Jazz', 'WAS': 'Washington Wizards'}
teamNames = ['Atlanta Hawks', 'Boston Celtics', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Brooklyn Nets', 'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'San Antonio Spurs', 'Sacramento Kings', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards']

API_URL = "https://api.americanwagering.com/regions/us/locations/ma/brands/czr/sb/v3/sports/baseball/events/highlights?competitionId=04f90892-3afa-4e84-acce-5b89f151063d"

now = datetime.now()

subject = "NBA Odds for " + now.strftime("%d %b, %Y")
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
def grabLinesAndConsensus():
    #message,arrGames = caesarsLineCheckerGeneric(Caesars_URL, teamNames, year)
    gamesArray = caesarsApiLineChecker(API_URL)
    #consensus = scoresandoddsConsensusCheck(year, Consensus_URL, nba_teams, teamCodes)

    print(gamesArray)
    # print(arrGames)
    
    
    #send_message(phone_number,message,EMAIL,PASSWORD)

    # db = setupDatabase('nba2023')
    # consolidateData(db, arrGames,consensus)

    return gamesArray

def formatMessage(messageArr):
    print('hello')
    concat_string = ""
    for game in messageArr:
        concat_string = '\n'.join([concat_string,"--------------", game["Date"] + " " + game["Time"], game["EventName"],game["HomeTeam"] + " : " + str(game["HomeML"]),game["AwayTeam"] + " : " + str(game["AwayML"])])
    return concat_string
messageArr = grabLinesAndConsensus()
send_message(phone_number,formatMessage(messageArr),EMAIL,PASSWORD)
send_message(phone_number2,formatMessage(messageArr),EMAIL,PASSWORD)





# send_message(phone_number,message,EMAIL,PASSWORD)
# send_message(phone_number2,message,EMAIL,PASSWORD)

# send_email(subject, message, sender, recipients, PASSWORD)
    

# send_message(phone_number,message,EMAIL,PASSWORD)
# send_message(phone_number2,message,EMAIL,PASSWORD)

# send_email(subject, message, sender, recipients, PASSWORD)


#myClient = MongoClient("192.168.1.97", 27017)
#db = myClient["local"]
#collection = db["MLB"]

#collection.insert_many(arrGames)

#print(concatStr)
