from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from sqlalchemy import ForeignKey

from . import db, app


class User(db.Model):
    """User model
    Parent class for Student and Teacher stores basic user information common
    to both teacher and student
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, nullable=False)
    password_hash = db.Column(db.String(64))

    type = db.Column(db.String(7))
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'User'
    }
    def hash_password(self, password):
        """Creates hash of password
        :param password: input password
        :return: hash of password
        """
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        """
        takes password and verifies if hash of it is same with hash stored in db
        :param password: input password
        :return: True if it same else False
        """
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self):
        """Creates a token
        When a user is successfully verfied, auth token is created and id is dumped in it.
        :return: authorization token
        """
        token = Serializer(app.config['SECRET_KEY'], app.config['TOKEN_EXPIRATION_TIME'])
        return token.dumps({'id': self.id})

    @staticmethod
    def get_user(token):
        """Gets user from token
        :param token: input token
        :return: A User if token is valid, else error message is returned.
        """
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            print("expired token")
            return None
        except BadSignature:
            print("bad signature")
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return '<User %r>' % (self.username)


class Student(User):
    """Student's model
    :attribute results: All the result objects of a student
    """
    results = db.relationship('TestResult', backref='student', lazy='dynamic')
    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }
    def __repr__(self):
        return '<Student %r>' % (self.username)


class Teacher(User):
    """Teacher's model
    :attribute results: All the tests authored by a teacher
    """
    tests = db.relationship('Test', backref='author', lazy='dynamic')
    __mapper_args__ = {
        'polymorphic_identity': 'teacher'
    }
    def __repr__(self):
        return '<Teacher %r>' % (self.username)


class Test(db.Model):
    """Test's model
    :attribute results: All te results of a test
    :attribute author_id: Teacher's id who created the test
    """
    id = db.Column(db.Integer, primary_key=True)

    results = db.relationship('TestResult', backref='test', lazy='dynamic')
    author_id = db.Column(db.Integer, ForeignKey(Teacher.id), nullable=False)
    def __repr__(self):
        return '<Test_id: %r>' % (self.id)


class TestResult(db.Model):
    """TestResult's model
    :attribute test_id: id of test whose result it is
    :attribute student_id: id of student whose result it is
    """
    id = db.Column(db.Integer, primary_key=True)

    test_id = db.Column(db.Integer, ForeignKey(Test.id), nullable=False)
    student_id = db.Column(db.Integer, ForeignKey(Student.id), nullable=False)

    # below are the metrics which are stored
    marks = db.Column(db.Integer)

    def __repr__(self):
        return '<TestResult_id: %r>' % (self.id)