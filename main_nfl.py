
import ssl
import sys
from pymongo import MongoClient
from oddSharkConsensus import oddSharkConensus
from sendMessage import send_message
from sendEmail import send_email

from caesarsLineCheckerNFL import caesarsLineCheckerNFL


import time

from datetime import datetime

now = datetime.now()

subject = "Baseball Odds for " + now.strftime("%d %b, %Y")
sender = "travis.chun13@gmail.com"
recipients = ["h.andrew.vo@gmail.com", "travis.chun13@gmail.com"]


EMAIL = "travis.chun13@gmail.com"
PASSWORD = sys.argv[1]
#Andrew
phone_number = "2145544438"
#Travis
phone_number2 = "9722077596"



message,arrGames = caesarsLineCheckerNFL()

#myClient = MongoClient("192.168.1.97", 27017)
#db = myClient["local"]
#collection = db["MLB"]

#collection.insert_many(arrGames)

#print(concatStr)
send_message(phone_number,message,EMAIL,PASSWORD)
send_message(phone_number2,message,EMAIL,PASSWORD)

send_email(subject, message, sender, recipients, PASSWORD)

