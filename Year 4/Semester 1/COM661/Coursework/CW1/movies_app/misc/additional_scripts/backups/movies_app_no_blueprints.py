from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient
from bson import ObjectId
import jwt
import datetime
from functools import wraps
import bcrypt
from bson.errors import InvalidId # for validation
from decorators import jwt_required, admin_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'andrewsk'

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.moviesDB
movies = db.movies
users = db.users
blacklist = db.blacklist

@app.route('/api/v1.0/movies', methods=['GET'])
def show_all_movies():
    # pagination
    page_num, page_size = 1, 10
    if request.args.get("pn"):
        page_num = int(request.args.get("pn"))
    if request.args.get("ps"):
        page_size = int(request.args.get("ps"))
    page_start = page_size * (page_num - 1)

    data_to_return = []
    for movie in movies.find().skip(page_start).limit(page_size):
        movie["_id"] = str(movie["_id"])
        for review in movie["reviews"]:
            review["_id"] = str(review["_id"])
        data_to_return.append(movie)
    # check if collection is empty and return 404 if so
    if data_to_return == []:
        return make_response( jsonify( { "error" : "No movies found in database." } ), 404 )
    return make_response( jsonify( data_to_return ), 200 )

@app.route('/api/v1.0/movies/<string:id>', methods=['GET'])
#@jwt_required   # user authed
def show_one_movie(id):
    try:
        ObjectId(id)
    except InvalidId:
        return make_response( jsonify( { "error" : "Invalid movie ID." } ), 404 )
    # passed validation
    movie = movies.find_one({'_id' : ObjectId(id)})
    if movie is not None:
        movie['_id'] = str(movie['_id'])
        for review in movie['reviews']:
            review["_id"] = str(review["_id"])
        return make_response( jsonify( movie ), 200 )
    else:
        return make_response( jsonify( { "error" : "Invalid movie ID." } ), 404 )


@app.route('/api/v1.0/movies', methods=['POST'])
@jwt_required   # user authed
def add_movie():
    required_fields = ["title", "releaseYear", "genres"]
    # checks all required fields - quicker using "if all()" than long if statement for each field 
    if all(request.form.get(field) for field in required_fields):
        new_movie = {
            "title": request.form["title"],
            "releaseYear": int(request.form["releaseYear"]),
            "genres": [g.strip() for g in request.form["genres"].split(",")],
            "averageRating": float(0.0),
            "ratingCount": int(0),
            "ratings": [],
            "tags": [t.strip() for t in request.form.get("tags", "").split(",") if t.strip()],
            "externalIds": {
                "imdbId": request.form.get("imdbId", ""),
                "tmdbId": int(request.form["tmdbId"]) if request.form.get("tmdbId") else None
            },
            "reviews": []
        }
        new_movie_id = movies.insert_one(new_movie)
        new_movie_link = "http://localhost:4999/api/v1.0/movies/" \
            + str(new_movie_id.inserted_id)
        return make_response( jsonify( { "url": new_movie_link } ), 201 )
    else:
        return make_response( jsonify( { "error": "Missing required form data (Title, Release Year or Genres)." } ), 400 )

@app.route('/api/v1.0/movies/<string:id>', methods=['PUT'])
@jwt_required   # user authed
def edit_movie(id):
    if "name" in request.form and "town" in request.form and "rating" in request.form:
        result = movies.update_one({"_id" : ObjectId(id)}, {
            "$set" : {
                "name" : request.form["name"],
                "town" : request.form["town"],
                "rating" : request.form["rating"]
            }
        })
        if result.matched_count == 1:
            edited_movie_link = "http://localhost:4999/api/v1.0/movies/" + id
            return make_response( jsonify( { "url" : edited_movie_link } ), 200 )
        else:
            return make_response( jsonify( { "error" : "Invalid movie ID." } ), 404 )
    else:
        return make_response( jsonify( { "error" : "Missing form data." } ), 400 )

@app.route('/api/v1.0/movies/<string:id>', methods=['DELETE'])
@jwt_required   # user authed
@admin_required # admin authed
def delete_movie(id):
    result = movies.delete_one({"_id" : ObjectId(id)})
    if result.deleted_count == 1:
        return make_response( jsonify( {} ), 204 )
    else:
        return make_response( jsonify( { "error" : "Invalid movie ID." } ), 404 )


@app.route('/api/v1.0/movies/<string:id>/reviews', methods=['POST'])
@jwt_required   # user authed
def add_new_review(id):
    new_review = {
        "_id" : ObjectId(),
        "username" : request.form["username"],
        "comment" : request.form["comment"],
        "stars" : request.form["stars"]
    }
    result = movies.update_one({"_id" : ObjectId(id)}, {
        "$push" : { "reviews" : new_review}
    })
    if result.matched_count == 1:
        new_review_link = "http://localhost:4999/api/v1.0/movies/" \
            + id + "/reviews/" + str(new_review["_id"])
        return make_response( jsonify( {"url" : new_review_link} ), 201 )
    else:
        return make_response( jsonify( { "error" : "Invalid movie ID." } ), 404 )

@app.route('/api/v1.0/movies/<string:id>/reviews', methods=['GET'])
def fetch_all_reviews(id):
    try:
        ObjectId(id)
    except InvalidId:
        return make_response( jsonify( { "error" : "Invalid movie ID." } ), 404 )
    # passed validation
    data_to_return = []
    movie = movies.find_one({"_id" : ObjectId(id)}, {"reviews" : 1, "_id" : 0})
    for review in movie["reviews"]:
        review["_id"] = str(review["_id"])
        data_to_return.append(review)

    return make_response( jsonify( data_to_return ), 200 )

@app.route('/api/v1.0/movies/<string:m_id>/reviews/<string:r_id>', methods=['GET'])
def fetch_one_review(m_id, r_id):
    try:
        ObjectId(m_id)
    except InvalidId:
        return make_response( jsonify( { "error" : "Invalid movie ID." } ), 404 )
    try:
        ObjectId(r_id)
    except InvalidId:
        return make_response( jsonify( { "error" : "Invalid review ID." } ), 404 )
    # passed validation
    movie = movies.find_one({"reviews._id" : ObjectId(r_id)}, {
        "_id" : 0, "reviews.$" : 1
    })
    if movie is None:
        return make_response( jsonify( { "error" : "Invalid movie ID or review ID." } ), 404 )
    movie["reviews"][0]["_id"] = str(movie["reviews"][0]["_id"])
    
    return make_response( jsonify( movie["reviews"][0] ), 200 )

@app.route('/api/v1.0/movies/<string:m_id>/reviews/<string:r_id>', methods=['PUT'])
@jwt_required   # user authed
def edit_review(m_id, r_id):
    try:
        ObjectId(m_id)
    except InvalidId:
        return make_response( jsonify( { "error" : "Invalid movie ID." } ), 404 )
    try:
        ObjectId(r_id)
    except InvalidId:
        return make_response( jsonify( { "error" : "Invalid review ID." } ), 404 )
    # passed validation
    edited_review = {
        "reviews.$.username" : request.form["username"],
        "reviews.$.comment" : request.form["comment"],
        "reviews.$.stars" : request.form["stars"]
    }
    # extra 'result' param as need to validate matched_count
    result = movies.update_one({
        "_id" : ObjectId(m_id),
        "reviews._id" : ObjectId(r_id)
    }, {
        "$set" : edited_review
    })
    if result.matched_count == 0:
        return make_response( jsonify( { "error" : "Movie or Review not found." } ), 404)
    
    edited_review_url = "http://localhost:4999/api/v1.0/movies/" \
        + m_id + "/reviews/" + r_id
    return make_response( jsonify( { "url" : edited_review_url } ), 200 )

@app.route('/api/v1.0/movies/<string:m_id>/reviews/<string:r_id>', methods=['DELETE'])
@jwt_required   # user authed
@admin_required # admin authed
def delete_review(m_id, r_id):
    try:
        ObjectId(m_id)
    except InvalidId:
        return make_response( jsonify( { "error" : "Invalid movie ID." } ), 404 )
    try:
        ObjectId(r_id)
    except InvalidId:
        return make_response( jsonify( { "error" : "Invalid review ID." } ), 404 )
    # passed validation
    movies.update_one({
        "_id" : ObjectId(m_id)
    }, {
        "$pull" : {"reviews" : {"_id" : ObjectId(r_id)}}
    })
    
    return make_response( jsonify( {} ), 204 )


#LOGIN
@app.route('/api/v1.0/login', methods=['GET'])
def login():
    auth = request.authorization
    if auth:
        user = users.find_one( { 'username' : auth.username } )
        if user is not None:
            if bcrypt.checkpw( bytes( auth.password, 'UTF-8' ), user['password'] ):
                token = jwt.encode( {
                    'user' : auth.username,
                    'admin' : user['admin'],
                    'exp' : datetime.datetime.now( datetime.UTC ) + datetime.timedelta( minutes=30 )
                }, globals.secret_key, algorithm='HS256' )
                return make_response( jsonify( { 'token' : token } ), 200 )
            else:
                return make_response( jsonify( { 'message' : 'Bad password.' } ), 401 )
        else:
            return make_response( jsonify( { 'message' : 'Bad username.' } ), 401 )
    return make_response( jsonify( { 'message' : 'Authentication required.' } ), 401 )

#LOGOUT
@app.route('/api/v1.0/logout', methods=['GET'])
@jwt_required   # user authed
def logout():
    token = request.headers['x-access-token']   # can assume user is authed if reaching logout stage, so can grab token from header
    blacklist.insert_one( { 'token' : token } )
    return make_response( jsonify( { 'message' : 'Logout successful. Goodbye!' } ), 200 )


if __name__ == "__main__":
    app.run(debug = True, port=4999)