from pymongo import MongoClient
import pymongo

def setupDatabase(dbname):
    myClient = MongoClient("192.168.1.97", 27017)
    db = myClient[dbname]
    
    return db

def createCollection(db,collectionName,data):
    print('Creating Collection: ' + collectionName)
    collection = db[collectionName]
    collection.insert_one(data)
    

def checkCollection(db, collectionName):
    print(db.list_collection_names())
    try:
        db.validate_collection(collectionName)  # Try to validate a collection
        print('This collection exists')
        return True
    except pymongo.errors.OperationFailure:  # If the collection doesn't exist
        print("This collection doesn't exist")
        return False

def printCollection(db, collectionName):
    cursor = db[collectionName].find({})
    for find in cursor:
        print(find)



    # dbnames = db.list_database_names()
    # if dbname in dbnames:
    #     print(dbname + " already exists")
    # else:
    #     print("Creating new DB with name: " + dbname)
    #     collection = db[dbname]

