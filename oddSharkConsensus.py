from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

URL = "https://www.oddsshark.com/mlb/consensus-picks"

mlb_teams = ["Arizona Diamondbacks","Atlanta Braves","Baltimore Orioles","Boston Red Sox","Chicago White Sox","Chicago Cubs","Cincinnati Reds","Cleveland Guardians","Colorado Rockies","Detroit Tigers","Houston Astros","Kansas City Royals","Los Angeles Angels","Los Angeles Dodgers","Miami Marlins","Milwaukee Brewers","Minnesota Twins","New York Yankees","New York Mets","Oakland Athletics","Philadelphia Phillies","Pittsburgh Pirates","San Diego Padres","San Francisco Giants","Seattle Mariners","St. Louis Cardinals","Tampa Bay Rays","Texas Rangers","Toronto Blue Jays","Washington Nationals"]

def oddSharkConensus(): 
    
    driver = webdriver.Firefox()
    driver.get(URL)
    delay = 15
    # wait = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'mwc-app')))

    # for i in range(0,9): # here you will need to tune to see exactly how many scrolls you need
    #     driver.execute_script('window.scrollBy(0, 400)')
    #     time.sleep(1)


    html = driver.page_source
    page_soup = soup(html, "html.parser")
    job_elements = page_soup.find_all("div", class_="layout-content")
    # results = page_soup.find(id="app")
    # job_elements = results.find_all("div", class_="EventCard")

    arrTimes = []
    arrConsensus = []
    arrHomeTeams = []
    arrAwayTeams = []
    
    for job_element in job_elements:
    #     #print(job_element, end="\n"*2)
        # print(job_element)
        htmlGames = job_element.find_all("div", class_="pick-table-content")

        for game in htmlGames:
            # print(game)
            percentsHTML = game.find_all("td", class_="pick-spread-consensus")
            inConsensus = False
            for percent in percentsHTML:
                consensus = percent.find("span",class_="text-right").text
                consensusValue = int(consensus.split("%")[0])
                if consensusValue <= 37 or consensusValue >= 63:
                    arrConsensus.append(consensusValue)
                    inConsensus = True
            
            if inConsensus:                
                date = game.find("div", class_="pick-date").text
                arrTimes.append(date)
                
                teams = game.find('td', class_="pick-teams-desktop").text
                split = teams.split('VS')
                arrHomeTeams.append(split[1].strip())
                arrAwayTeams.append(split[0].strip())

    driver.quit()
    percentCount = 0
    concatStr = ""
    for x,time in enumerate(arrTimes):
        concatStr = '\n'.join([concatStr,"--------------", arrTimes[x], arrAwayTeams[x]  + " : " + str(arrConsensus[percentCount]) + "%"])
        percentCount = percentCount + 1
        concatStr = '\n'.join([concatStr,arrHomeTeams[x] + " : " + str(arrConsensus[percentCount]) + "%"])
        percentCount = percentCount + 1
    print(concatStr)