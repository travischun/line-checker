
import ssl
import sys
from pymongo import MongoClient
from sendEmail import send_email
from caesarsLineChecker import caesarsLineChecker
from oddSharkConsensus import oddSharkConensus

import time

from datetime import datetime

now = datetime.now()

subject = "Baseball Odds for " + now.strftime("%d %b, %Y")
body = "This is the body of the text message"
sender = "travis.chun13@gmail.com"
recipients = ["h.andrew.vo@gmail.com", "travis.chun13@gmail.com"]


EMAIL = "travis.chun13@gmail.com"
PASSWORD = sys.argv[1]



#oddSharkConensus()
consensus = oddSharkConensus()
send_email(subject, body, sender, recipients, PASSWORD)
