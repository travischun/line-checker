from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import datetime
import requests


headers = { 
    "user-agent": "MozillebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
}


consensusPercentageArr = []
linesArr = []
def scoresandoddsAPIConsensusCheck(year, URL, teamList, teamCodes): 
    datesArr = []
    teamsArr = []
    # driver = webdriver.Firefox()
    # driver.get(URL)
    # delay = 15
    # wait = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'page-content')))
    response = requests.get(URL, headers=headers)
    
    #print(response.text)

    page_soup = soup(response.text, "html.parser")
    results = page_soup.find_all("div", class_="consensus-table-spread--0")

    for dates in results:
        date = dates.find("div",class_="event-info")
        # print("-------- Date --------")
        # print(date.find("span").attrs["data-value"])
        # print("-----------------------")
        datesArr.append(date.find("span").attrs["data-value"].strip())

    for teams in results:
        #print(job_element, end="\n"*2)
        htmlCard = teams.find_all("span", class_="trend-graph-sides")

        for team in htmlCard:
            split = team.text.split(' ')
            if split[2] in teamCodes:
                teamsArr.append(split[2])
            if len(split) >= 11 and split[10] in teamCodes:
                teamsArr.append(split[10])

    for consensus in results:    
        percentage = consensus.find_all("span", class_="trend-graph-percentage")
        for x,percent in enumerate(percentage):
            if x < 1:
               split = percent.text.split(' ')
               consensusPercentageArr.append(split[1].split('%')[0])
               consensusPercentageArr.append(split[2].split('%')[0])
    
    for side in results:
        rightName = ""
        leftName = ""
        events = side.find_all("div", class_="event-header")
        for event in events:
            right = event.find_all("div", class_="right")
            for rteamNames in right:
                names = rteamNames.find_all("span", class_="team-name")
                for name in names:
                    rightName = name.text.lower()
            left = event.find_all("div", class_="left")
            for lteamNames in left:
                names = lteamNames.find_all("span", class_="team-name")
                for name in names:
                    leftName = name.text.lower()
        linesArr.append(getLines(leftName,rightName))

    # driver.quit()
    # return formatConsensus(teamList,teamsArr,datesArr,year,linesArr)
    return formatString(teamList,teamsArr,datesArr,year,linesArr)

def getLines(left, right):
    awayLine = ""
    homeLine = ""
    baseURL = "https://www.scoresandodds.com/nfl/"
    fullURL = baseURL + left + "-vs-" + right
    # print(fullURL.replace(" ", ""))
    response = requests.get(fullURL.replace(" ", ""), headers=headers)

    page_soup = soup(response.text, "html.parser")
    results = page_soup.find_all("section", class_="page-body")

    for oddsTables in results:
        oddsTable = oddsTables.find_all("table", class_="odds-table")
        for active in oddsTable:
            activeTable = active.find_all("tbody", class_="active")
            for tbody in activeTable:
                tablerow = tbody.find_all("tr")
                y = 0
                for items in tablerow:
                    if y == 0:
                        item = items.find_all("td",class_="game-odds")
                        i = 0
                        for casearsOdds in item:
                            if i == 3:
                                awayLines = casearsOdds.find_all("span", class_="data-value")
                                # print(awayLine)
                                j = 0
                                for line in awayLines:
                                    if j == 0:
                                        if '+' in line.text or '-' in line.text:
                                            awayLine = line.text
                            i = i + 1
                    elif y == 1:
                        item = items.find_all("td",class_="game-odds")
                        i = 0
                        for casearsOdds in item:
                            if i == 3:
                                homeLines = casearsOdds.find_all("span", class_="data-value")
                                j = 0
                                for line in homeLines:
                                    if '+' in line.text or '-' in line.text:
                                        homeLine = line.text
                            i = i + 1
                    y = y + 1
    outputDict = {
        "HomeTeam": left.capitalize(),
        "HomeLine": homeLine,
        "AwayTeam": right.capitalize(),
        "AwayLine": awayLine
    }
    return outputDict
    # print("Home")
    # print(left + " line: ")
    # print(homeLine)
    # print("Away")
    # print(right + " line: ")
    # print(awayLine)
    
    
                    
                

formattedConsensus = {}

def formatDate(date,year):
    # print(date)
    # fullDate = date.split(' ')
    # fullDate[0] = fullDate[0] + '/' + year
    # finishedDate = " ".join(fullDate)
    # print(finishedDate)
    # dateObject = datetime.datetime.strptime(finishedDate, "%m/%d/%Y %I:%M%p").strftime('%m%d%Y-%H:%M')
    dateObject = datetime.datetime.strptime(date,'%Y-%m-%dT%H:%M:%S%z').strftime('%m%d%Y-%H:%M')
    return dateObject

def formatConsensus(teams,teamsArr,datesArr,year,lines):
    y = 0
    # print(teams)
    timestampArr = []
    for date in datesArr:
        # print(date)
        timestampArr.append(formatDate(date,year))
    #print(timestampArr)
    #print(teamsArr)
    for x,team in enumerate(teamsArr):
        if x % 2 == 0:
            key = timestampArr[y] + '-' + teams[teamsArr[x]] + "vs" + teams[teamsArr[x + 1]]
            key = key.replace(" ", "")
            item = {"Away": {}, "Home": {}}
            item['gameTime'] = datesArr[y]
            item['Away']['Team'] = teams[teamsArr[x]]
            item['Away']['Consensus'] = consensusPercentageArr[x]
            item['Away']['Line'] = lines[y]["AwayLine"]
        else:
            item['Home']['Team'] = teams[teamsArr[x]]
            item['Home']['Consensus'] = consensusPercentageArr[x]
            formattedConsensus[key] = item 
            item['Home']['Line'] = lines[y]["HomeLine"]
            y = y + 1

    return formattedConsensus

def formatString(teams,teamsArr,datesArr,year,lines):
    finalArr =[]
    
    y = 0
    # print(teams)
    timestampArr = []
    for date in datesArr:
        # print(date)
        timestampArr.append(formatDate(date,year))
    print(timestampArr)
    print(teamsArr)
    for x,team in enumerate(teamsArr):
        if x % 2 == 0:
            key = timestampArr[y] + '-' + teams[teamsArr[x]] + "vs" + teams[teamsArr[x + 1]]
            key = key.replace(" ", "")
            gameDict = {"Away": {}, "Home": {}}
            gameDict['gameTime'] = datesArr[y]
            gameDict['Away']['Team'] = teams[teamsArr[x]]
            gameDict['Away']['Consensus'] = consensusPercentageArr[x]
            gameDict['Away']['Line'] = lines[y]["AwayLine"]
        else:
            gameDict['Home']['Team'] = teams[teamsArr[x]]
            gameDict['Home']['Consensus'] = consensusPercentageArr[x]
            gameDict['Home']['Line'] = lines[y]["HomeLine"]
            finalArr.append(gameDict)
            y = y + 1

    return finalArr


# teamCodes = ['ATL', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GS', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NO', 'NY', 'BKN', 'OKC', 'ORL', 'PHI', 'PHO', 'POR','SA', 'SAC', 'TOR', 'UTA', 'WAS']

# nba_teams = {'ATL': 'Atlanta Hawks', 'BOS': 'Boston Celtics', 'CHA': 'Charlotte Hornets', 'CHI': 'Chicago Bulls', 'CLE': 'Cleveland Cavaliers', 'DAL': 'Dallas Mavericks', 'DEN': 'Denver Nuggets', 'DET': 'Detroit Pistons', 'GS': 'Golden State Warriors', 'HOU': 'Houston Rockets', 'IND': 'Indiana Pacers', 'LAC': 'Los Angeles Clippers', 'LAL': 'Los Angeles Lakers', 'MEM': 'Memphis Grizzlies', 'MIA': 'Miami Heat', 'MIL': 'Milwaukee Bucks', 'MIN': 'Minnesota Timberwolves', 'NO': 'New Orleans Pelicans', 'NY': 'New York Knicks', 'BKN': 'Brooklyn Nets', 'OKC': 'Oklahoma City Thunder', 'ORL': 'Orlando Magic', 'PHI': 'Philadelphia 76ers', 'PHO': 'Phoenix Suns', 'POR': 'Portland Trail Blazers', 'SAC': 'Sacramento Kings', 'SA':'San Antonio Spurs','TOR': 'Toronto Raptors', 'UTA': 'Utah Jazz', 'WAS': 'Washington Wizards'}
# teamNames = ['Atlanta Hawks', 'Boston Celtics', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Brooklyn Nets', 'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'San Antonio Spurs', 'Sacramento Kings', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards']
# teamCodes = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC', 'LAC', 'LAR', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG', 'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WAS']

# nfl_teams = {"DEN": "Denver Broncos","KC":"Kansas City Chiefs","BAL":"Baltimore Ravens","TEN":"Tennessee Titans","WAS":"Washington Commanders","ATL":"Atlanta Falcons","CAR":"Carolina Panthers","MIA":"Miami Dolphins","NO":"New Orleans Saints","HOU":"Houston Texans","SEA":"Seattle Seahawks","CIN":"Cincinnati Bengals","IND":"Indianapolis Colts","JAX":"Jacksonville Jaguars","SF":"San Francisco 49ers","CLE":"Cleveland Browns","MIN":"Minnesota Vikings","CHI":"Chicago Bears","NE":"New England Patriots","LV":"Las Vegas Raiders","DET":"Detroit Lions","TB":"Tampa Bay Buccaneers","PHI":"Philadelphia Eagles","NYJ":"New York Jets","ARI":"Arizona Cardinals","LAR":"Los Angeles Rams","NYG":"New York Giants","BUF":"Buffalo Bills","DAL":"Dallas Cowboys","LAC":"Los Angeles Chargers","PIT":"Pittsburgh Steelers","GB":"Green Bay Packers"}

# result = scoresandoddsAPIConsensusCheck("2024","https://www.scoresandodds.com/nba/consensus-picks", nba_teams, teamCodes)
# result = scoresandoddsAPIConsensusCheck("2024","https://www.scoresandodds.com/nfl/consensus-picks", nfl_teams, teamCodes)

# print(result)