from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

URL = "https://sportsbook.caesars.com/us/ma/bet/baseball"

mlb_teams = ["Arizona Diamondbacks","Atlanta Braves","Baltimore Orioles","Boston Red Sox","Chicago White Sox","Chicago Cubs","Cincinnati Reds","Cleveland Guardians","Colorado Rockies","Detroit Tigers","Houston Astros","Kansas City Royals","Los Angeles Angels","Los Angeles Dodgers","Miami Marlins","Milwaukee Brewers","Minnesota Twins","New York Yankees","New York Mets","Oakland Athletics","Philadelphia Phillies","Pittsburgh Pirates","San Diego Padres","San Francisco Giants","Seattle Mariners","St. Louis Cardinals","Tampa Bay Rays","Texas Rangers","Toronto Blue Jays","Washington Nationals"]

def caesarsLineChecker(): 
    
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
    arrGames = []
    
    for job_element in job_elements:
        #print(job_element, end="\n"*2)
        htmlNames = job_element.find_all("div", class_="teamLabel")

        y = 0
        for name in htmlNames:
            # print(name.text)
        #     print(name, end="\n"*2)
        #     # print(name.text)
            if name.text in mlb_teams:
                
                oddsHTML = job_element.find_all("div", class_="oddsView")
                
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
                    if x <= 1 and y < 1:
                        #print(odds.text)
                        arrOdds.append(odds.text)
                        x = x + 1
                arrNames.append(name.text)
                y = y + 1

    count = 0
    timeCount = 0
    concatStr = ""
    gameRecord = {}
    print('names')
    print(len(arrNames))
    print('times')
    print(len(arrTimes))
    print('odds')
    print(len(arrOdds))
    for x,name in enumerate(arrNames):
        if count == 0:
            concatStr = '\n'.join([concatStr,"--------------", arrTimes[timeCount], arrNames[x]  + " : ", arrOdds[x]])
            print("--------------")
            print(arrTimes[timeCount])
            print(arrNames[x]  + " : ", arrOdds[x])
            away = {
                "gameTime":arrTimes[timeCount].replace("| ", ""),
                "Away":
                {
                    "Team":arrNames[x],
                    "OpeningLine":arrOdds[x]
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
                    "OpeningLine":arrOdds[x]
                }
            }
            gameRecord.update(home)
            arrGames.append(gameRecord)
            gameRecord = {}
            count = 0
            timeCount = timeCount + 1
    driver.quit()
    return concatStr, arrGames
    