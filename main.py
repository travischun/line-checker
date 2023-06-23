
import ssl
import sys
from pymongo import MongoClient
from sendMessage import send_message
from caesarsLineChecker import caesarsLineChecker

EMAIL = "travis.chun13@gmail.com"
PASSWORD = sys.argv[1]
#Andrew
phone_number = "2145544438"
#Travis
phone_number2 = "9722077596"



message,arrGames = caesarsLineChecker()

#myClient = MongoClient("localhost", 27017)
#db = myClient["local"]
#collection = db["MLB"]

#collection.insert_many(arrGames)

#print(concatStr)
send_message(phone_number,message,EMAIL,PASSWORD)
send_message(phone_number2,message,EMAIL,PASSWORD)