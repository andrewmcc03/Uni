from flask import Blueprint, request, make_response, jsonify
import jwt
import datetime
import bcrypt
import re # more input format validation

from globals import users, blacklist, secret_key
from decorators import jwt_required

# tokens taken from Postman in x-access-token header

auth_bp = Blueprint("auth_bp", __name__)

#########################################################################################################
# AUTH ENDPOINTS ########################################################################################
#########################################################################################################

#REGISTER
@auth_bp.route("/api/v1.0/register", methods=["POST"])
def register():
    # reg new user
    if not request.form:
        return make_response( jsonify( { "error" : "You must enter a valid username and password to register." } ), 400)

    username = request.form.get("username", "").strip()             # REQUIRED
    password = request.form.get("password", "")                     # REQUIRED
    email = request.form.get("email", "").strip() or None           # optional
    name = request.form.get("name", "") or username  # defaults to username as display name if none provided

    if not username or not re.fullmatch(r"[A-Za-z0-9_.-]{3,20}", username): # uname should be between 3-20 and use valid chars only (i.e., letters, numbers, underscores/full stops, etc.)
        return make_response( jsonify( { "error" : "Username must be 3–20 characters (letters, numbers, _, . or -)." } ), 400 )
    if not password or len(password) < 8 or len(password) > 24: # pw should be between 8-24 chars
        return make_response( jsonify( { "error" : "Password must be 8-24 characters." } ), 400 )
    if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email): # email format check validation
        return make_response( jsonify( { "error" : "Please enter a valid email address." } ), 400 )
    if not name.strip():
        return make_response( jsonify( { "error" : "Name cannot be an empty string." } ), 400 )
    # check if username already exists
    if users.find_one({"username": username}):
        return make_response( jsonify( { "error" : "Username is already registered. Please try again." } ), 409 )
    
    hashed_pw = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt()) # hash the pw
    # passed validation - insert new user to users collection
    result = users.insert_one({
        "name": name.strip(),
        "username": username,
        "password": hashed_pw,
        "email" : email,
        "admin": False,
        "createdAt": datetime.datetime.now( datetime.UTC )
    })
    return make_response( jsonify( { "message" : "Account created successfully. Welcome!",
                                     "userId" : str(result.inserted_id),
                                     "username" : username } ), 201 )

#LOGIN
@auth_bp.route("/api/v1.0/login", methods=["GET"])
def login():
    # in Postman: Basic Auth with valid account user and pw
    auth = request.authorization
    if not auth:
        return make_response( jsonify( { "error" : "Authentication required. Please enter a valid username and password." } ), 401 )
    user = users.find_one( { "username": auth.username } )
    if user is None:
        return make_response( jsonify( { "error" : "Bad username." } ), 401)
    if not bcrypt.checkpw( auth.password.encode("utf-8"), user["password"]):
        return make_response( jsonify( { "error" : "Bad password." } ), 401 )

    token = jwt.encode( {
        "user": auth.username,
        "admin": user.get("admin", False),
        "exp": datetime.datetime.now( datetime.UTC ) + datetime.timedelta( minutes=30 )
    }, secret_key, algorithm="HS256" )
    return make_response( jsonify( {"token": token} ), 200 )

#LOGOUT
@auth_bp.route("/api/v1.0/logout", methods=["GET"])
@jwt_required   # user authed
def logout():
    token = request.headers["x-access-token"]   # can assume user is authed if reaching logout stage, so can grab token from header
    blacklist.insert_one( {"token": token} )
    return make_response( jsonify( { "message" : "Logout successful. Goodbye!" } ), 200 )