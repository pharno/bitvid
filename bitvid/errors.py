
class UserExistsException(Exception):
    pass

class UserNotFoundException(Exception):
    pass

class IncorrectCredentialsException(Exception):
    pass

errors = {
    "Exception": {
        "message": "Internal Server Error",
        "status": 500
    },
    "NotFound": {
        "message": "Not Found",
        "status" : 404
    },
    "UserExistsException": {
        "message": "User with this email already exists",
        "status": 409
    },
    "UserNotFoundException": {
        "message": "user with given email not found",
        "status": 404
    },
    "IncorrectCredentialsException": {
        "message": "could not login with given email and password",
        "status": 401
    },
    "MethodNotAllowed": {
        "message": "Method not allowed",
        "status" : 405
    }
}