from pymongo import MongoClient
import pymongo

def setupDatabase(dbname):
    print('Setting up database ' + dbname)
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

def compareCollection(db, collectionName, newData, timestamp):
    cursor = db[collectionName].find({})
    change = False
    query  = { "_id": collectionName }
    for collection in cursor:
        if newData["Away"]["Line"] != collection["Away"]["Line"] and newData["Home"]["Line"] != collection["Home"]["Line"]:
            print('New Line Movement')
            collection["Away"]["Line"] = newData["Away"]["Line"]
            collection["Home"]["Line"] = newData["Home"]["Line"]
            collection['LineMovement'].append({
                "time": timestamp,
                "homeTeam": collection["Home"]["Team"],
                "homeLine": collection["Home"]["Line"],
                "awayTeam": collection["Away"]["Team"],
                "awayLine": collection["Away"]["Line"]
            })
            change = True
        if newData["Away"]["Consensus"] != collection["Away"]["Consensus"] and newData["Home"]["Consensus"] != collection["Home"]["Consensus"]:
            print('New Consensus Data')
            collection["Away"]["Consensus"] = newData["Away"]["Consensus"]
            collection["Home"]["Consensus"] = newData["Home"]["Consensus"]
            change = True
        if change == True:
            db[collectionName].update_one(query, {"$set": collection})
        else:
            print('No changes for ' + collectionName + ' at ' + timestamp)
    # dbnames = db.list_database_names()
    # if dbname in dbnames:
    #     print(dbname + " already exists")
    # else:
    #     print("Creating new DB with name: " + dbname)
    #     collection = db[dbname]

