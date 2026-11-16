from pymongo import MongoClient
from bson import ObjectId
import datetime

secret_key = 'andrewsk'

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.moviesDB

movies = db.movies
users = db.users
blacklist = db.blacklist

BASE_URL = "http://localhost:4999/api/v1.0" # for shortening link refs

# format document - convert MongoDB ObjectIds and date/times into JSON values
def serialise_document(document):
    if isinstance(document, list):
        return [serialise_document(item) for item in document]
    if isinstance(document, dict):
        return {key: serialise_document(value) for key, value in document.items()}
    if isinstance(document, ObjectId):
        return str(document)
    if isinstance(document, datetime.datetime):
        return document.isoformat() + ("Z" if document.tzinfo is None else "")
    return document