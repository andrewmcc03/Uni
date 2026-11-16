from flask import Flask, request, jsonify, make_response, g
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson import ObjectId
from bson.errors import InvalidId
import jwt
import datetime
from functools import wraps
import bcrypt
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('MOVIES_SECRET_KEY', 'change-this-development-secret')

client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://127.0.0.1:27017'))
db = client.moviesDB
movies = db.movies
users = db.users
blacklist = db.blacklist

BASE_URL = 'http://localhost:4999/api/v1.0'


# AUTHENTICATION DECORATORS
# Tokens are sent from Postman in the x-access-token header.
def jwt_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return make_response(jsonify({'error': 'Token is missing.'}), 401)
        try:
            if blacklist.find_one({'token': token}):
                return make_response(jsonify({'error': 'Token has been logged out.'}), 401)
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            g.current_user = payload['user']
            g.current_admin = payload.get('admin', False)
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({'error': 'Token has expired.'}), 401)
        except (jwt.InvalidTokenError, KeyError):
            return make_response(jsonify({'error': 'Token is invalid.'}), 401)
        return function(*args, **kwargs)
    return wrapper


def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not getattr(g, 'current_admin', False):
            return make_response(jsonify({'error': 'Administrator access required.'}), 403)
        return function(*args, **kwargs)
    return wrapper


def serialise_document(document):
    """Convert MongoDB ObjectIds and datetimes into JSON-friendly values."""
    if isinstance(document, list):
        return [serialise_document(item) for item in document]
    if isinstance(document, dict):
        return {key: serialise_document(value) for key, value in document.items()}
    if isinstance(document, ObjectId):
        return str(document)
    if isinstance(document, datetime.datetime):
        return document.isoformat() + ('Z' if document.tzinfo is None else '')
    return document


# MOVIES
@app.route('/api/v1.0/movies', methods=['GET'])
def show_all_movies():
    # Pagination: /movies?pn=1&ps=10
    try:
        page_num = max(1, int(request.args.get('pn', 1)))
        page_size = min(100, max(1, int(request.args.get('ps', 10))))
    except ValueError:
        return make_response(jsonify({'error': 'Page number and page size must be whole numbers.'}), 400)

    # Optional filters: q, genre, year, minYear, maxYear, minRating, maxRating
    query = {}
    if request.args.get('q'):
        query['title'] = {'$regex': request.args['q'], '$options': 'i'}
    if request.args.get('genre'):
        query['genres'] = {'$regex': '^' + request.args['genre'] + '$', '$options': 'i'}
    try:
        if request.args.get('year'):
            query['releaseYear'] = int(request.args['year'])
        elif request.args.get('minYear') or request.args.get('maxYear'):
            query['releaseYear'] = {}
            if request.args.get('minYear'):
                query['releaseYear']['$gte'] = int(request.args['minYear'])
            if request.args.get('maxYear'):
                query['releaseYear']['$lte'] = int(request.args['maxYear'])
        if request.args.get('minRating') or request.args.get('maxRating'):
            query['averageRating'] = {}
            if request.args.get('minRating'):
                query['averageRating']['$gte'] = float(request.args['minRating'])
            if request.args.get('maxRating'):
                query['averageRating']['$lte'] = float(request.args['maxRating'])
    except ValueError:
        return make_response(jsonify({'error': 'Year and rating filters must be valid numbers.'}), 400)

    sort_fields = {
        'title': 'title',
        'year': 'releaseYear',
        'rating': 'averageRating',
        'grossProfits': 'grossProfits',
        'reviewCount': 'reviewCount'
    }
    sort_by = request.args.get('sortBy', 'title')
    sort_order = DESCENDING if request.args.get('order', 'asc').lower() == 'desc' else ASCENDING
    if sort_by not in sort_fields:
        return make_response(jsonify({'error': 'sortBy must be title, year, rating, grossProfits or reviewCount.'}), 400)

    total_movies = movies.count_documents(query)
    data_to_return = [serialise_document(movie) for movie in movies.find(query)
                      .sort(sort_fields[sort_by], sort_order)
                      .skip((page_num - 1) * page_size).limit(page_size)]

    return make_response(jsonify({
        'page': page_num,
        'pageSize': page_size,
        'totalMovies': total_movies,
        'totalPages': (total_movies + page_size - 1) // page_size,
        'movies': data_to_return
    }), 200)


@app.route('/api/v1.0/movies/<string:id>', methods=['GET'])
def show_one_movie(id):
    try:
        movie_id = ObjectId(id)
    except InvalidId:
        return make_response(jsonify({'error': 'Invalid movie ID.'}), 400)
    movie = movies.find_one({'_id': movie_id})
    if movie is None:
        return make_response(jsonify({'error': 'Movie not found.'}), 404)
    return make_response(jsonify(serialise_document(movie)), 200)


@app.route('/api/v1.0/movies', methods=['POST'])
@jwt_required
def add_movie():
    required_fields = ['title', 'releaseYear', 'genres']
    if not all(request.form.get(field, '').strip() for field in required_fields):
        return make_response(jsonify({'error': 'Title, releaseYear and genres are required.'}), 400)
    try:
        release_year = int(request.form['releaseYear'])
        gross_profits = float(request.form.get('grossProfits', 0))
    except ValueError:
        return make_response(jsonify({'error': 'releaseYear must be a whole number and grossProfits must be numeric.'}), 400)
    if release_year < 1888 or gross_profits < 0:
        return make_response(jsonify({'error': 'Enter a valid release year and non-negative grossProfits value.'}), 400)

    genres = [genre.strip() for genre in request.form['genres'].split(',') if genre.strip()]
    if not genres:
        return make_response(jsonify({'error': 'At least one genre is required.'}), 400)

    tmdb_id = request.form.get('tmdbId')
    if tmdb_id:
        try:
            tmdb_id = int(tmdb_id)
        except ValueError:
            return make_response(jsonify({'error': 'tmdbId must be a whole number.'}), 400)

    new_movie = {
        'title': request.form['title'].strip(),
        'releaseYear': release_year,
        'genres': genres,
        'grossProfits': gross_profits,
        'averageRating': 0.0,
        'ratingCount': 0,
        'weightedRating': 0.0,
        'reviewCount': 0,
        'tagCount': 0,
        'reviews': [],
        'tags': [],
        'externalIds': {
            'imdbId': request.form.get('imdbId', '').strip() or None,
            'tmdbId': tmdb_id
        }
    }
    result = movies.insert_one(new_movie)
    new_movie_link = BASE_URL + '/movies/' + str(result.inserted_id)
    return make_response(jsonify({'url': new_movie_link}), 201)


@app.route('/api/v1.0/movies/<string:id>', methods=['PUT', 'PATCH'])
@jwt_required
def edit_movie(id):
    try:
        movie_id = ObjectId(id)
    except InvalidId:
        return make_response(jsonify({'error': 'Invalid movie ID.'}), 400)

    # Partial updates are accepted; submit only the fields to change.
    allowed_fields = ['title', 'releaseYear', 'genres', 'grossProfits', 'imdbId', 'tmdbId']
    updates = {}
    for field in allowed_fields:
        if field not in request.form:
            continue
        value = request.form[field]
        if field == 'title':
            value = value.strip()
            if not value:
                return make_response(jsonify({'error': 'Title cannot be empty.'}), 400)
        elif field == 'releaseYear':
            try:
                value = int(value)
            except ValueError:
                return make_response(jsonify({'error': 'releaseYear must be a whole number.'}), 400)
            if value < 1888:
                return make_response(jsonify({'error': 'Enter a valid releaseYear.'}), 400)
        elif field == 'grossProfits':
            try:
                value = float(value)
            except ValueError:
                return make_response(jsonify({'error': 'grossProfits must be numeric.'}), 400)
            if value < 0:
                return make_response(jsonify({'error': 'grossProfits cannot be negative.'}), 400)
        elif field == 'genres':
            value = [genre.strip() for genre in value.split(',') if genre.strip()]
            if not value:
                return make_response(jsonify({'error': 'At least one genre is required.'}), 400)
        elif field == 'tmdbId':
            try:
                value = int(value) if value.strip() else None
            except ValueError:
                return make_response(jsonify({'error': 'tmdbId must be a whole number.'}), 400)
        elif field == 'imdbId':
            value = value.strip() or None

        if field in ['imdbId', 'tmdbId']:
            updates['externalIds.' + field] = value
        else:
            updates[field] = value

    if not updates:
        return make_response(jsonify({'error': 'No recognised movie fields were supplied.'}), 400)
    result = movies.update_one({'_id': movie_id}, {'$set': updates})
    if result.matched_count == 0:
        return make_response(jsonify({'error': 'Movie not found.'}), 404)
    return make_response(jsonify({'url': BASE_URL + '/movies/' + id}), 200)


@app.route('/api/v1.0/movies/<string:id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_movie(id):
    try:
        movie_id = ObjectId(id)
    except InvalidId:
        return make_response(jsonify({'error': 'Invalid movie ID.'}), 400)
    result = movies.delete_one({'_id': movie_id})
    if result.deleted_count == 1:
        return make_response('', 204)
    return make_response(jsonify({'error': 'Movie not found.'}), 404)


# REVIEWS (embedded in each movie)
@app.route('/api/v1.0/movies/<string:id>/reviews', methods=['GET'])
def fetch_all_reviews(id):
    try:
        movie_id = ObjectId(id)
    except InvalidId:
        return make_response(jsonify({'error': 'Invalid movie ID.'}), 400)
    movie = movies.find_one({'_id': movie_id}, {'reviews': 1})
    if movie is None:
        return make_response(jsonify({'error': 'Movie not found.'}), 404)
    return make_response(jsonify(serialise_document(movie.get('reviews', []))), 200)


@app.route('/api/v1.0/movies/<string:m_id>/reviews/<string:r_id>', methods=['GET'])
def fetch_one_review(m_id, r_id):
    try:
        movie_id = ObjectId(m_id)
        review_id = ObjectId(r_id)
    except InvalidId:
        return make_response(jsonify({'error': 'Invalid movie or review ID.'}), 400)
    movie = movies.find_one({'_id': movie_id, 'reviews._id': review_id}, {'reviews.$': 1})
    if movie is None:
        return make_response(jsonify({'error': 'Movie or review not found.'}), 404)
    return make_response(jsonify(serialise_document(movie['reviews'][0])), 200)


@app.route('/api/v1.0/movies/<string:id>/reviews', methods=['POST'])
@jwt_required
def add_new_review(id):
    try:
        movie_id = ObjectId(id)
    except InvalidId:
        return make_response(jsonify({'error': 'Invalid movie ID.'}), 400)
    comment = request.form.get('comment', '').strip()
    if not comment or not request.form.get('rating'):
        return make_response(jsonify({'error': 'comment and rating are required.'}), 400)
    try:
        rating = float(request.form['rating'])
    except ValueError:
        return make_response(jsonify({'error': 'rating must be numeric.'}), 400)
    if rating < 1 or rating > 5:
        return make_response(jsonify({'error': 'rating must be between 1 and 5.'}), 400)

    new_review = {
        '_id': ObjectId(),
        'name': g.current_user,
        'username': g.current_user,
        'comment': comment,
        'rating': rating,
        'date': datetime.datetime.now(datetime.timezone.utc)
    }
    result = movies.update_one({'_id': movie_id}, {'$push': {'reviews': new_review}})
    if result.matched_count == 0:
        return make_response(jsonify({'error': 'Movie not found.'}), 404)

    # Keep the movie's review statistics in step with its embedded reviews.
    movies.update_one({'_id': movie_id}, [{'$set': {
        'reviewCount': {'$size': '$reviews'},
        'ratingCount': {'$size': '$reviews'},
        'averageRating': {'$round': [{'$avg': '$reviews.rating'}, 2]},
        'weightedRating': {'$round': [{'$divide': [{'$add': [{'$multiply': [{'$avg': '$reviews.rating'}, {'$size': '$reviews'}]}, 70]}, {'$add': [{'$size': '$reviews'}, 20]}]}, 2]}
    }}])
    link = BASE_URL + '/movies/' + id + '/reviews/' + str(new_review['_id'])
    return make_response(jsonify({'url': link}), 201)


@app.route('/api/v1.0/movies/<string:m_id>/reviews/<string:r_id>', methods=['PUT', 'PATCH'])
@jwt_required
def edit_review(m_id, r_id):
    try:
        movie_id = ObjectId(m_id)
        review_id = ObjectId(r_id)
    except InvalidId:
        return make_response(jsonify({'error': 'Invalid movie or review ID.'}), 400)

    movie = movies.find_one({'_id': movie_id, 'reviews._id': review_id}, {'reviews.$': 1})
    if movie is None:
        return make_response(jsonify({'error': 'Movie or review not found.'}), 404)
    review = movie['reviews'][0]
    if review.get('username') != g.current_user and not g.current_admin:
        return make_response(jsonify({'error': 'You can only edit your own reviews.'}), 403)

    updates = {}
    if 'comment' in request.form:
        comment = request.form['comment'].strip()
        if not comment:
            return make_response(jsonify({'error': 'comment cannot be empty.'}), 400)
        updates['reviews.$.comment'] = comment
    if 'rating' in request.form:
        try:
            rating = float(request.form['rating'])
        except ValueError:
            return make_response(jsonify({'error': 'rating must be numeric.'}), 400)
        if rating < 1 or rating > 5:
            return make_response(jsonify({'error': 'rating must be between 1 and 5.'}), 400)
        updates['reviews.$.rating'] = rating
    if not updates:
        return make_response(jsonify({'error': 'Supply comment and/or rating to update.'}), 400)

    movies.update_one({'_id': movie_id, 'reviews._id': review_id}, {'$set': updates})
    movies.update_one({'_id': movie_id}, [{'$set': {
        'reviewCount': {'$size': '$reviews'},
        'ratingCount': {'$size': '$reviews'},
        'averageRating': {'$round': [{'$avg': '$reviews.rating'}, 2]},
        'weightedRating': {'$round': [{'$divide': [{'$add': [{'$multiply': [{'$avg': '$reviews.rating'}, {'$size': '$reviews'}]}, 70]}, {'$add': [{'$size': '$reviews'}, 20]}]}, 2]}
    }}])
    return make_response(jsonify({'url': BASE_URL + '/movies/' + m_id + '/reviews/' + r_id}), 200)


@app.route('/api/v1.0/movies/<string:m_id>/reviews/<string:r_id>', methods=['DELETE'])
@jwt_required
def delete_review(m_id, r_id):
    try:
        movie_id = ObjectId(m_id)
        review_id = ObjectId(r_id)
    except InvalidId:
        return make_response(jsonify({'error': 'Invalid movie or review ID.'}), 400)

    movie = movies.find_one({'_id': movie_id, 'reviews._id': review_id}, {'reviews.$': 1})
    if movie is None:
        return make_response(jsonify({'error': 'Movie or review not found.'}), 404)
    review = movie['reviews'][0]
    if review.get('username') != g.current_user and not g.current_admin:
        return make_response(jsonify({'error': 'You can only delete your own reviews.'}), 403)

    movies.update_one({'_id': movie_id}, {'$pull': {'reviews': {'_id': review_id}}})
    movies.update_one({'_id': movie_id}, [{'$set': {
        'reviewCount': {'$size': '$reviews'},
        'ratingCount': {'$size': '$reviews'},
        'averageRating': {'$ifNull': [{'$round': [{'$avg': '$reviews.rating'}, 2]}, 0]},
        'weightedRating': {'$round': [{'$divide': [{'$add': [{'$multiply': [{'$ifNull': [{'$avg': '$reviews.rating'}, 0]}, {'$size': '$reviews'}]}, 70]}, {'$add': [{'$size': '$reviews'}, 20]}]}, 2]}
    }}])
    return make_response('', 204)


# TAGS (also embedded in each movie)
@app.route('/api/v1.0/movies/<string:id>/tags', methods=['GET'])
def fetch_movie_tags(id):
    try:
        movie_id = ObjectId(id)
    except InvalidId:
        return make_response(jsonify({'error': 'Invalid movie ID.'}), 400)
    movie = movies.find_one({'_id': movie_id}, {'tags': 1})
    if movie is None:
        return make_response(jsonify({'error': 'Movie not found.'}), 404)
    return make_response(jsonify(serialise_document(movie.get('tags', []))), 200)


@app.route('/api/v1.0/movies/<string:id>/tags', methods=['POST'])
@jwt_required
def add_movie_tag(id):
    try:
        movie_id = ObjectId(id)
    except InvalidId:
        return make_response(jsonify({'error': 'Invalid movie ID.'}), 400)
    tag_text = request.form.get('tag', '').strip()
    if not tag_text:
        return make_response(jsonify({'error': 'tag is required.'}), 400)
    new_tag = {
        '_id': ObjectId(),
        'tag': tag_text,
        'username': g.current_user,
        'date': datetime.datetime.now(datetime.timezone.utc)
    }
    result = movies.update_one({'_id': movie_id}, {'$push': {'tags': new_tag}})
    if result.matched_count == 0:
        return make_response(jsonify({'error': 'Movie not found.'}), 404)
    movies.update_one({'_id': movie_id}, [{'$set': {'tagCount': {'$size': '$tags'}}}])
    return make_response(jsonify({'url': BASE_URL + '/movies/' + id + '/tags/' + str(new_tag['_id'])}), 201)


@app.route('/api/v1.0/movies/<string:m_id>/tags/<string:t_id>', methods=['DELETE'])
@jwt_required
def delete_movie_tag(m_id, t_id):
    try:
        movie_id = ObjectId(m_id)
        tag_id = ObjectId(t_id)
    except InvalidId:
        return make_response(jsonify({'error': 'Invalid movie or tag ID.'}), 400)
    movie = movies.find_one({'_id': movie_id, 'tags._id': tag_id}, {'tags.$': 1})
    if movie is None:
        return make_response(jsonify({'error': 'Movie or tag not found.'}), 404)
    tag = movie['tags'][0]
    if tag.get('username') and tag.get('username') != g.current_user and not g.current_admin:
        return make_response(jsonify({'error': 'You can only delete your own tags.'}), 403)
    movies.update_one({'_id': movie_id}, {'$pull': {'tags': {'_id': tag_id}}})
    movies.update_one({'_id': movie_id}, [{'$set': {'tagCount': {'$size': '$tags'}}}])
    return make_response('', 204)


# DATASET-SPECIFIC QUERIES / AGGREGATIONS
@app.route('/api/v1.0/stats/overview', methods=['GET'])
def movie_overview():
    result = list(movies.aggregate([
        {'$group': {
            '_id': None,
            'movieCount': {'$sum': 1},
            'averageMovieRating': {'$avg': '$averageRating'},
            'averageGrossProfits': {'$avg': '$grossProfits'},
            'totalReviews': {'$sum': '$reviewCount'},
            'totalTags': {'$sum': '$tagCount'}
        }},
        {'$project': {'_id': 0, 'movieCount': 1,
                      'averageMovieRating': {'$round': ['$averageMovieRating', 2]},
                      'averageGrossProfits': {'$round': ['$averageGrossProfits', 2]},
                      'totalReviews': 1, 'totalTags': 1}}
    ]))
    if not result:
        return make_response(jsonify({'message': 'No movies found.'}), 404)
    return make_response(jsonify(serialise_document(result[0])), 200)


@app.route('/api/v1.0/stats/genres', methods=['GET'])
def genre_statistics():
    result = list(movies.aggregate([
        {'$unwind': '$genres'},
        {'$group': {'_id': '$genres', 'movieCount': {'$sum': 1},
                    'averageRating': {'$avg': '$averageRating'},
                    'totalReviews': {'$sum': '$reviewCount'}}},
        {'$sort': {'movieCount': -1, '_id': 1}},
        {'$project': {'_id': 0, 'genre': '$_id', 'movieCount': 1,
                      'averageRating': {'$round': ['$averageRating', 2]}, 'totalReviews': 1}}
    ]))
    return make_response(jsonify(serialise_document(result)), 200)


@app.route('/api/v1.0/movies/top-rated', methods=['GET'])
def top_rated_movies():
    try:
        limit = min(50, max(1, int(request.args.get('limit', 10))))
        minimum_reviews = max(0, int(request.args.get('minReviews', 5)))
    except ValueError:
        return make_response(jsonify({'error': 'limit and minReviews must be whole numbers.'}), 400)
    result = movies.find({'reviewCount': {'$gte': minimum_reviews}}).sort(
        [('weightedRating', DESCENDING), ('reviewCount', DESCENDING)]).limit(limit)
    return make_response(jsonify([serialise_document(movie) for movie in result]), 200)


# LOGIN / LOGOUT
@app.route('/api/v1.0/login', methods=['GET'])
def login():
    # In Postman, configure Basic Auth with the account's username and password.
    auth = request.authorization
    if not auth:
        return make_response(jsonify({'error': 'Authentication required. Use Basic Auth.'}), 401)
    user = users.find_one({'username': auth.username})
    if user is None:
        return make_response(jsonify({'error': 'Bad username.'}), 401)
    if not bcrypt.checkpw(auth.password.encode('utf-8'), user['password']):
        return make_response(jsonify({'error': 'Bad password.'}), 401)

    token = jwt.encode({
        'user': auth.username,
        'admin': user.get('admin', False),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return make_response(jsonify({'token': token}), 200)


@app.route('/api/v1.0/logout', methods=['GET'])
@jwt_required
def logout():
    token = request.headers.get('x-access-token')
    blacklist.insert_one({'token': token})
    return make_response(jsonify({'message': 'Logout successful.'}), 200)


if __name__ == '__main__':
    app.run(debug=True, port=4999)