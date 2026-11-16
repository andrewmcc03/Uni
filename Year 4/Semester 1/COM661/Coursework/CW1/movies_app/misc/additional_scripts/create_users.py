from pymongo import MongoClient
import bcrypt

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.moviesDB  # select moviesDB database
users = db.users      # select users collection (in moviesDB)

user_list = [
          {
            "name" : "Andrew",
            "username" : "andrew",  
            "password" : b"andrewpw",
            "email" : "andrew@email.com",
            "admin" : True
          },
          {
            "name" : "Standard User",
            "username" : "standarduser",  
            "password" : b"standardpw",
            "email" : "standarduser@email.com",
            "admin" : False
          },
          {
            "name" : "Alternate User",
            "username" : "altuser",  
            "password" : b"alternatepw",
            "email" : "alternateuser@email.com",
            "admin" : False
          }
       ]

#DROP COLLECTION BEFORE RE-ADDING (CLEAR ALL)
#users.drop()

for new_user in user_list:
      new_user["password"] = bcrypt.hashpw(new_user["password"], bcrypt.gensalt())
      users.insert_one(new_user)
