from flask import jsonify
from . import app


def make_response(code, message):
    """Creates an HTTP response
    Creates an HTTP response to be sent to client with status code as 'code'
    and data - message
    :param code: the http status code
    :param message: the main message to be sent to client
    :return: returns the HTTP response
    """
    if code == 400:
        return bad_request(message)
    elif code == 401:
        return unauthorized(message)
    elif code == 403:
        return forbidden(message)
    elif code == 500:
        return internal_server_handler(message)
    else:
        return ok(message)


@app.errorhandler(400)
def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


@app.errorhandler(401)
def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


@app.errorhandler(403)
def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


@app.errorhandler(500)
def internal_server_handler(message):
    response = jsonify({'error': 'server error', 'message': message})
    response.status_code = 500
    return response


def ok(message):
    response = jsonify(message)
    response.status_code = 200
    return response