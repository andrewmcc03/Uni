from pymongo import MongoClient
import bcrypt
import subprocess # for cmd commands (for mongosh)
from pathlib import Path # for cmd commands (for mongosh)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.moviesDB      # select moviesDB database

movies = db.movies        # movies collection
users = db.users          # select users collection (in moviesDB)
blacklist = db.blacklist  # select blacklist collection

### WARNING - WIPES ALL COLLECTIONS IN moviesDB and re-generates & re-enters dataset

# pre-warn
warnConfirm = input(str("\n**RE-IMPORT WARNING**: This will drop all collections and re-import all data from the 'movies.json' dataset. Do you wish to continue [y/n]? "))
if warnConfirm != "y":
    print("\nExiting...\n")
    exit()


#########################################################################################################
#########################################################################################################
#########################################################################################################

### DROP COLLECTIONS BEFORE RE-ADDING (CLEAR ALL)
movies.drop()
users.drop()
blacklist.drop()


### create users
print("\nImporting pre-set users into moviesDB...")

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

for new_user in user_list:
      new_user["password"] = bcrypt.hashpw(new_user["password"], bcrypt.gensalt())
      users.insert_one(new_user)

print("\nFinished importing users into moviesDB.")


### mongosh import

BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR.parent / "movies.json"

print("\nImporting movies into moviesDB...")

command = [
    "mongoimport",
    "--db", "moviesDB",
    "--collection", "movies",
    "--file", str(JSON_FILE),
    "--jsonArray"
]

try:
    subprocess.run(command, check=True)

    print("\nSuccessfully imported movies into MongoDB!\n")

except subprocess.CalledProcessError as error:
    print(f"\nMongoDB import failed: {error}\n")

except FileNotFoundError:
    print("\nError: mongoimport could not be found. Check that MongoDB Database Tools are installed.\n")