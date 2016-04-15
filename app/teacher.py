from flask import Blueprint, request

from . import app
from .models import db, Teacher, Test, User
from .authentication import auth
from .fileIO import create_json_file, remove_file
from .responses import make_response


teacherAPI = Blueprint('teacherAPI', __name__)


@teacherAPI.route('/list/teacher/<username>', methods=['GET'])
@auth.login_required
def get_test_by_teacher(username):
    """Lists teacher's tests
    Retrieves list of tests whose author is the teacher with id given in argument
    :param id: Teacher's id
    :return: ids of tests if teacher with given id exists
    """

    teacher = Teacher.query.filter_by(username=username).first()
    if teacher is None:
        return make_response(400, "Teacher does not exists")

    id_list = []
    for test in teacher.tests:
        id_list.append(test.id)

    return make_response(200, {'ids': id_list})


@teacherAPI.route('/exam/teacher/create', methods=['POST'])
@auth.login_required
def create_exam():
    """Creates a new test by teacher
    Takes token from authorization header and gets the teacher id from it.
    creates a new json file storing tests data and updates the database.
    :return: test id if test is created successfully else returns error message
    """

    user = User.get_user(auth.username())
    if user is None or not user.is_teacher():
        return make_response(401, "Only a teacher can create a test")

    test_id = Test.query.count() + 1
    try:
        create_json_file(test_id, app.config['TEST_PATH'], request.json)
    except Exception as e:
        return make_response(400, e)
    try:
        test = Test(author_id=user.id)
        db.session.add(test)
        db.session.commit()

        return make_response(200, {'id': test_id})
    except Exception as e:
        remove_file(test_id, app.config['TEST_PATH'])
        return make_response(400, e)