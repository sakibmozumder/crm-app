import pymongo


def collectionsFromMongo(collection_name):
    connection = pymongo.MongoClient(
        'mongodb://localhost:27017/')
    # Define DB Name
    dbname = connection['clientsdb']
    clientCol = dbname[collection_name]
    return clientCol
