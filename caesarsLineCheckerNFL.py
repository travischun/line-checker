from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import datetime

URL = "https://sportsbook.caesars.com/us/ma/bet/americanfootball?id=007d7c61-07a7-4e18-bb40-15104b6eac92"

nfl_teams = ["Denver Broncos","Kansas City Chiefs","Baltimore Ravens","Tennessee Titans","Washington Commanders","Atlanta Falcons","Carolina Panthers","Miami Dolphins","New Orleans Saints","Houston Texans","Seattle Seahawks","Cincinnati Bengals","Indianapolis Colts","Jacksonville Jaguars","San Francisco 49ers","Cleveland Browns","Minnesota Vikings","Chicago Bears","New England Patriots","Las Vegas Raiders","Detroit Lions","Tampa Bay Buccaneers","Philadelphia Eagles","New York Jets","Arizona Cardinals","Los Angeles Rams","New York Giants","Buffalo Bills","Dallas Cowboys","Los Angeles Chargers","Pittsburgh Steelers","Green Bay Packers"]
year = "2023"

def formatDate(date):
    dateObject = datetime.datetime.strptime(date, "%b %d %Y %I:%M%p").strftime('%m%d%Y-%H:%M')
    return dateObject

def caesarsLineCheckerNFL(): 
    
    driver = webdriver.Firefox()
    driver.get(URL)
    delay = 15
    wait = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'mwc-app')))

    for i in range(0,9): # here you will need to tune to see exactly how many scrolls you need
        driver.execute_script('window.scrollBy(0, 400)')
        time.sleep(1)


    html = driver.page_source
    page_soup = soup(html, "html.parser")
    results = page_soup.find(id="app")
    job_elements = results.find_all("div", class_="EventCard")
    arrNames = []
    arrOdds = []
    arrTimes = []
    arrGames = {}
    
    for job_element in job_elements:
        #print(job_element, end="\n"*2)
        htmlNames = job_element.find_all("div", class_="teamLabel")

        y = 0
        for name in htmlNames:
            # print(name.text)
        #     print(name, end="\n"*2)
        #     # print(name.text)
            if name.text in nfl_teams:
                
                oddsHTML = job_element.find_all("div", class_="cui__market-button-wrapper")
                
                htmlTimes = job_element.find_all("div", class_="dateContainer")

                lockedHTML = job_element.find_all("div", class_="selectionContainer")

                skip = False
                
                for i in htmlTimes:
                    if (i.find("span", class_="liveClock")):
                        skip = True
                        continue
                for i in lockedHTML:
                    if (i.find("button", class_="disabled")):
                        skip = True
                        continue
                
                if (skip):
                    continue

                #print(oddsHTML)
                x = 0
                for times in htmlTimes:
                    if x <= 1 and y < 1:
                        #print(odds.text)
                        arrTimes.append(times.text)
                for odds in oddsHTML:
                    #print(y)
                    print(odds.text)
                    if x >= 2 and x <= 3 and y < 1:
                        #print(odds.text)
                        arrOdds.append(odds.text)
                    x = x + 1
                arrNames.append(name.text)
                y = y + 1

    count = 0
    timeCount = 0
    concatStr = ""
    gameRecord = {}
    # print(arrNames)
    # print(len(arrNames))
    # print(arrTimes)
    # print(len(arrTimes))
    # print(arrOdds)
    # print(len(arrOdds))
    for x,name in enumerate(arrNames):
        if count == 0:
            concatStr = '\n'.join([concatStr,"--------------", arrTimes[timeCount], arrNames[x]  + " : ", arrOdds[x]])
            print("--------------")
            print(arrTimes[timeCount])
            print(arrNames[x]  + " : ", arrOdds[x])
            timestamp = formatDate(arrTimes[timeCount].replace("|", year))
            key = timestamp + '-' + arrNames[x] + "vs" + arrNames[x + 1]
            key = key.replace(" ","")
            away = {
                "gameTime":arrTimes[timeCount].replace("| ", ""),
                "Away":
                {
                    "Team":arrNames[x],
                    "Line":arrOdds[x]
                }
                }
            gameRecord.update(away)
            count = count + 1
        else:
            concatStr = '\n'.join([concatStr,arrNames[x]  + " : ", arrOdds[x]])
            print(arrNames[x]  + " : ", arrOdds[x])
            home = {
                "Home":
                {
                    "Team":arrNames[x],
                    "Line":arrOdds[x]
                }
            }
            gameRecord.update(home)
            arrGames[key] = gameRecord
            gameRecord = {}
            count = 0
            timeCount = timeCount + 1
    driver.quit()
    return concatStr, arrGames

