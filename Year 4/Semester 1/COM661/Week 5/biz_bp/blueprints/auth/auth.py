from flask import Blueprint, request, make_response, jsonify
import jwt
import datetime
import bcrypt
import globals
from decorators import jwt_required, admin_required

auth_bp = Blueprint("auth_bp", __name__)

blacklist = globals.db.blacklist
users = globals.db.users

#LOGIN
@auth_bp.route('/api/v1.0/login', methods=['GET'])
def login():
    auth = request.authorization
    #if auth and auth.password == 'password':
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
@auth_bp.route('/api/v1.0/logout', methods=['GET'])
@jwt_required   # user authed
def logout():
    token = request.headers['x-access-token']   # can assume user is authed if reaching logout stage, so can grab token from header
    blacklist.insert_one( { 'token' : token } )
    return make_response( jsonify( { 'message' : 'Logout successful. Goodbye!' } ), 200 )