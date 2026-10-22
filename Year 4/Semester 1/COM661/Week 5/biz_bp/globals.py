from pymongo import MongoClient

secret_key = 'andrewsk'

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.bizDB