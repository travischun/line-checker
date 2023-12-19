from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import datetime




consensusPercentageArr = []

def scoresandoddsConsensusCheck(year, URL, teamList, teamCodes): 
    datesArr = []
    teamsArr = []
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
    return formatConsensus(teamList,teamsArr,datesArr,year)

   

formattedConsensus = {}

def formatDate(date,year):
    #12/17 7:20PM
    fullDate = date.split(' ')
    fullDate[0] = fullDate[0] + '/' + year
    finishedDate = " ".join(fullDate)
    dateObject = datetime.datetime.strptime(finishedDate, "%m/%d/%Y %I:%M%p").strftime('%m%d%Y-%H:%M')
    return dateObject

def formatConsensus(teams,teamsArr,datesArr,year):
    y = 0
    print(teams)
    timestampArr = []
    for date in datesArr:
        timestampArr.append(formatDate(date,year))
    for x,team in enumerate(teamsArr):
        if x % 2 == 0:
            key = timestampArr[y] + '-' + teams[teamsArr[x]] + "vs" + teams[teamsArr[x + 1]]
            key = key.replace(" ", "")
            item = {"Away": {}, "Home": {}}
            item['gameTime'] = datesArr[y]
            y = y + 1
            item['Away']['Team'] = teams[teamsArr[x]]
            item['Away']['Consensus'] = consensusPercentageArr[x]
        else:
            item['Home']['Team'] = teams[teamsArr[x]]
            item['Home']['Consensus'] = consensusPercentageArr[x]
            formattedConsensus[key] = item 
    return formattedConsensus

    