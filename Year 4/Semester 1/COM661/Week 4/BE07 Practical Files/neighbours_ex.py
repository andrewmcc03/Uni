from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.bizDB
businesses = db.biz

#TESTING LINE for business in businesses.aggregate( [ { "$match" : { "town" : "Newry" } }, { "$limit" : 1 } ] ):
for business in businesses.aggregate( [ { "$sample" : { "size": 1 } } ] ):
    print("\nRandom business is " + business["name"] + " from " + business["town"] + "\n")

    for neighbour in businesses.aggregate( [
                { "$geoNear" : 
                    { "near" : { "type" : "Point", 
                                "coordinates" : business["location"]["coordinates"] },
                      "maxDistance": 50000,
                      "minDistance" : 1,
                      "distanceField" : "distance",
                      "spherical" : True
                    }
                },
                { "$project" : { "name" : 1, "town" : 1, "distance" : 1 } },
                { "$match": {
                    "town": {"$ne": business["town"]}
                }},
                { "$limit" : 1 }
            ]):
        distance_km = str(round(neighbour["distance"] / 1000))
        print(neighbour["name"] + " from " + neighbour["town"] + " is at a distance of " + distance_km + "km")