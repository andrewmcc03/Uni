from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.bizDB
businesses = db.biz

# outputting name and number of employees of all businesses in Belfast
pipeline = [
    { "$match" : { "town" : "Belfast" } },
    { "$project" : {"town" : 1, "name" : 1, "num_employees" : 1, "profit" : 1 } }
]

for business in businesses.aggregate(pipeline):
    print( business["town"] + "  |  ", business["name"] + "  |  ", str(business["num_employees"]) + "  |  ", str(business['profit'][2]["gross"]) )
