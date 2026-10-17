from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.bizDB
businesses = db.biz

pipeline = [
    { "$match" : { "town" : "Banbridge"} },
    { "$project" : {"town" : 1, "profit" : 1 } }
]

for business in businesses.aggregate(pipeline):
    print( business["town"], str(business['profit'][2]["gross"]) )


# db.biz.aggregate( [ 
#     { "$match" : { "town" : "Banbridge" } },
#     { "$project" : { "town" : 1, "profit" : 1, "num_employees" : 1 } },
#     { "$unwind" : "$profit" },
#     { "$match" : {
#         "num_employees" : { "$gte" : 0 },
#         "profit.gross" : { "$gte" : 0 }
#     }},
#     { "$sort" : { "profit.gross" : -1 } },
#     { "$skip" : 2 },
#     { "$limit" : 3 }
# ])

# db.biz.aggregate( [ 
#     { "$match" : { "town" : "Banbridge" } },
#     { "$project" : { "town" : 1, "profit" : 1, "num_employees" : 1 } }
# ])

# db.biz.aggregate( [ 
#     { "$match" : { "town" : "Banbridge" } },
#     { "$project" : { "town" : 1, "profit" : 1, "num_employees" : 1, "_id" : 0 } },
#     { "$unwind" : "$profit" },
#     { "$match" : {
#         "num_employees" : { "$gte" : 0 },
#         "profit.gross" : { "$gte" : 0 }
#     }},
#     { "$sort" : { "profit.gross" : -1 } },
#     { "$out"  : "profitable_big_biz" }
# ])

db.biz.aggregate( [
    { "$unwind" : "$profit" },
    { "$match" : {
        "num_employees" : { "$gte" : 0 },
        "profit.gross" : { "$gte" : 0 }
    }},
    # sorts by gross profit descending so highest earners come first
    { "$sort" : { "profit.gross" : -1 } },
    # groups by a composite key of town and year, picking the first (highest) business record
    { "$group" : {
        "_id" : {
            "town" : "$town",
            "year" : "$profit.year"
        },
        "total_num_biz_in_town_count" : { "$sum" : 1 },
        "most_profitable_biz_in_town" : { "$first" : "$name" },
        "total" : { "$first" : "$profit.gross" }
    }},
    # sorts results cleanly by town AND THEN by year
    { "$sort" : { "_id.town" : 1, "_id.year" : 1 } }
])
#COPY AND PASTE IN WITHOUT COMMENTS TO RUN