from flask import Blueprint, abort, jsonify, request
from flask_httpauth import HTTPBasicAuth

from .models import Student, User, db, Teacher
from .responses import make_response

authenticationAPI = Blueprint('authenticationAPI', __name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_token(token, password):
    """Verify token
    Takes the token and checks if token is valid by calling get_user(token)
    :param token: Token sent by client
    :param password: Unused variable
    :return: True if token is valid else False
    """
    user = User.get_user(token)
    if not user:
        return False
    return True


@authenticationAPI.route('/login', methods = ['POST'])
def login():
    """Authenticates a login requests
    Takes username and password from authentication header and verifies by looking
    for a user with input username and password hash.
    :Return:
        token containint the user id if authenticated successfullly
        else it provides the error message
    """
    try:
        username = request.authorization['username']
        password = request.authorization['password']
        user = User.query.filter_by(username = username).first()

        if user is None or not user.verify_password(password):
            return make_response(401, "Invalid credentials")

        token = user.generate_auth_token()
        return make_response(200, {'token': token.decode('ascii')})
    except Exception as e:
        return  make_response(400, e)


@authenticationAPI.route('/register', methods = ['POST'])
def new_user():
    """Registers new user
    Takes username, password and role and creates a new user if not already
    present in database
    Returns:
        A success message if registration was successful
        else it returns an error message
    """
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        role = request.json.get('role')

        if username is None or password is None or role is None:
            return make_response(400, "Empty username or password is not allowed")
        if role not in ['student', 'teacher']:
            return make_response(400, "Role should be either 'student' or 'teacher'")
        if User.query.filter_by(username = username).first() is not None:
            return make_response(400, "User exists")

        if role == 'student':
            user = Student(username = username)
        else:
            user = Teacher(username = username)
        user.hash_password(password)

        db.session.add(user)
        db.session.commit()
        return make_response(200, {'message': "User created successfully"})
    except Exception as e:
        return make_response(400, e)