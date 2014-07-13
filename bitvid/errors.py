class LoginRequiredException(Exception):
    pass

class UserExistsException(Exception):
    pass

class UserNotFoundException(Exception):
    pass

class IncorrectCredentialsException(Exception):
    pass

class ResourceNotFoundException(Exception):
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
    },
    "LoginRequiredException": {
        "message": "You need to be logged in to access this resource",
        "status": 403
    },
    "ResourceNotFoundException": {
        "message": "Could not find the resource you're trying to access",
        "status": 404
    }
}