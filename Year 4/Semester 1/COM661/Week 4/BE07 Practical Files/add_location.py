from pymongo import MongoClient
import random

locations = {
    "Coleraine" : [55.10653864221481, -6.703013870894064, 55.16083114339611, -6.640640630380869],
    "Banbridge" : [54.32805966474902, -6.29894073802459, 54.36914017698541, -6.238287009221747],
    "Belfast" : [54.556250355557616, -6.028115456708859, 54.641284967038544, -5.81672407568025],
    "Lisburn" : [54.493341788077785, -6.112005038731509, 54.53555188930533, -6.014228381824925],
    "Ballymena" : [54.83568393536063, -6.332311942061101, 54.88626160226742, -6.223396172342375],
    "Derry" : [54.98342225503688, -7.36866298220212, 55.036414352973814, -7.249238544803166],
    "Newry" : [54.15120498618891, -6.380223593570023, 54.20399608371601, -6.301172915614019],
    "Enniskillen" : [54.32563285593699, -7.677972259020914, 54.3681652508206, -7.585746468072241],
    "Omagh" : [54.58310436623075, -7.338966458054591, 54.61803538619165, -7.252314753372047],
    "Ballymoney" : [55.05519711336693, -6.5368047498203925, 55.08479180123714, -6.48359756273462]
}

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.bizDB
businesses = db.biz

for location in locations:
    for business in businesses.find( { "town" : location } ):
        rand_x = locations[location][0] + ( (locations[location][2] - locations[location][0]) * (random.randint(0,100) / 100) )
        rand_y = locations[location][1] + ( (locations[location][3] - locations[location][1]) * (random.randint(0,100) / 100) )
        businesses.update_one(
            { "_id" : business["_id"] },
            { "$set" : 
                { 
                    "location" : 
                        {
                            "type" : "Point",
                            "coordinates" : [rand_x, rand_y]
                        }

                }
            }
        )