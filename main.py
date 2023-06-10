from urllib.request import Request, urlopen
import ssl
import smtplib
import sys
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}
carrier = "att"
phone_number = "9722077596"
EMAIL = "travis.chun13@gmail.com"
PASSWORD = sys.argv[1]

mlb_teams = ["Arizona Diamondbacks","Atlanta Braves","Baltimore Orioles","Boston Red Sox","Chicago White Sox","Chicago Cubs","Cincinnati Reds","Cleveland Guardians","Colorado Rockies","Detroit Tigers","Houston Astros","Kansas City Royals","Los Angeles Angels","Los Angeles Dodgers","Miami Marlins","Milwaukee Brewers","Minnesota Twins","New York Yankees","New York Mets","Oakland Athletics","Philadelphia Phillies","Pittsburgh Pirates","San Diego Padres","San Francisco Giants","Seattle Mariners","St. Louis Cardinals","Tampa Bay Rays","Texas Rangers","Toronto Blue Jays","Washington Nationals"]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

URL = "https://sportsbook.caesars.com/us/ma/bet/baseball"
driver = webdriver.Firefox()

driver.get(URL)
# time.sleep(10)
delay = 15
# wait1 = WebDriverWait(driver,15)
wait = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'mwc-app')))

for i in range(0,8): # here you will need to tune to see exactly how many scrolls you need
  driver.execute_script('window.scrollBy(0, 400)')
  time.sleep(1)


html = driver.page_source

# req = Request(URL , headers={'User-Agent': 'Mozilla/5.0'})

# page = urlopen(req, context=ctx).read()

page_soup = soup(html, "html.parser")
#print(html)
#print(page_soup)
# print(page_soup)
results = page_soup.find(id="app")
# print(results)
job_elements = results.find_all("div", class_="EventCard")
# print(job_elements)
arrNames = []
arrOdds = []
arrTimes = []
is_mlb_team = False

def send_message(phone_number, carrier, message):
    recipient = phone_number + CARRIERS[carrier]
    auth = (EMAIL, PASSWORD)
 
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
 
    server.sendmail(auth[0], recipient, message)



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

#print(arrOdds)
count = 0
timeCount = 0
# print(arrTimes)
concatStr = ""
for x,name in enumerate(arrNames):
    if count == 0:
        concatStr = '\n'.join([concatStr,"--------------", arrTimes[timeCount], arrNames[x]  + " : ", arrOdds[x]])
        print("--------------")
        print(arrTimes[timeCount])
        print(arrNames[x]  + " : ", arrOdds[x])
        count = count + 1
    else:
        concatStr = '\n'.join([concatStr,arrNames[x]  + " : ", arrOdds[x]])
        print(arrNames[x]  + " : ", arrOdds[x])
        count = 0
        timeCount = timeCount + 1

#print(concatStr)
send_message(phone_number, carrier, concatStr)
driver.quit()