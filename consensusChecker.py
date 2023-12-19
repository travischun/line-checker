from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import datetime

year = "2023"
URL = "https://www.scoresandodds.com/nfl/consensus-picks"

teamCodes = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC', 'LAC', 'LAR', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG', 'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WAS']

nfl_teams = {"DEN": "Denver Broncos","KC":"Kansas City Chiefs","BAL":"Baltimore Ravens","TEN":"Tennessee Titans","WAS":"Washington Commanders","ATL":"Atlanta Falcons","CAR":"Carolina Panthers","MIA":"Miami Dolphins","NO":"New Orleans Saints","HOU":"Houston Texans","SEA":"Seattle Seahawks","CIN":"Cincinnati Bengals","IND":"Indianapolis Colts","JAX":"Jacksonville Jaguars","SF":"San Francisco 49ers","CLE":"Cleveland Browns","MIN":"Minnesota Vikings","CHI":"Chicago Bears","NE":"New England Patriots","LV":"Las Vegas Raiders","DET":"Detroit Lions","TB":"Tampa Bay Buccaneers","PHI":"Philadelphia Eagles","NYJ":"New York Jets","ARI":"Arizona Cardinals","LAR":"Los Angeles Rams","NYG":"New York Giants","BUF":"Buffalo Bills","DAL":"Dallas Cowboys","LAC":"Los Angeles Chargers","PIT":"Pittsburgh Steelers","GB":"Green Bay Packers"}

datesArr = []
teamsArr = []
consensusPercentageArr = []

def scoresandoddsConsensusCheck(): 
    
    driver = webdriver.Firefox()
    driver.get(URL)
    delay = 15
    wait = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'page-content')))

    html = driver.page_source
    page_soup = soup(html, "html.parser")
    results = page_soup.find_all("div", class_="consensus-table-spread--0")

    for dates in results:
        date = dates.find("div",class_="event-info")
        datesArr.append(date.text.strip())

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
    
    driver.quit()
    return formatConsensus()

   

formattedConsensus = {}

def formatDate(date):
    #12/17 7:20PM
    fullDate = date.split(' ')
    fullDate[0] = fullDate[0] + '/' + year
    finishedDate = " ".join(fullDate)
    dateObject = datetime.datetime.strptime(finishedDate, "%m/%d/%Y %I:%M%p").strftime('%m%d%Y-%H:%M')
    return dateObject

def formatConsensus():
    y = 0
    
    timestampArr = []
    for date in datesArr:
        timestampArr.append(formatDate(date))
    for x,team in enumerate(teamsArr):
        if x % 2 == 0:
            key = timestampArr[y] + '-' + nfl_teams[teamsArr[x]] + "vs" + nfl_teams[teamsArr[x + 1]]
            key = key.replace(" ", "")
            item = {"Away": {}, "Home": {}}
            item['gameTime'] = datesArr[y]
            y = y + 1
            item['Away']['Team'] = nfl_teams[teamsArr[x]]
            item['Away']['Consensus'] = consensusPercentageArr[x]
        else:
            item['Home']['Team'] = nfl_teams[teamsArr[x]]
            item['Home']['Consensus'] = consensusPercentageArr[x]
            formattedConsensus[key] = item 
    return formattedConsensus

    