from flask import Blueprint, jsonify, request
from flask_httpauth import HTTPBasicAuth

from .authentication import auth
from .models import Student, User, db, Teacher
from .responses import make_response

studentAPI = Blueprint('studentAPI', __name__)


@studentAPI.route('/exam/student/<int:id>', methods = ['GET'])
@auth.login_required
def send_test(id):
    pass


@studentAPI.route('/submit/student/<int:id>', methods = ['POST'])
@auth.login_required
def submit_test(id):
    pass


@studentAPI.route('/result/student/', methods = ['GET'])
@studentAPI.route('/result/student/<int:id>', methods = ['GET'])
@auth.login_required
def get_result(id = -1):
    pass