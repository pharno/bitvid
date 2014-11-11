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


class NotFound(Exception):
    pass


class PermissionDenied(Exception):
    pass

errors = {
    "Exception": {
        "message": "Internal Server Error",
        "status": 500
    },
    "ValueError": {
        "status": 500
    },
    "NotFound": {
        "message": "Could not find the resource you're trying to access",
        "status": 404
    },
    "UserExistsException": {
        "message": "User with this name already exists",
        "status": 409
    },
    "UserNotFoundException": {
        "message": "user with given name not found",
        "status": 404
    },
    "IncorrectCredentialsException": {
        "message": "could not login with given name and password",
        "status": 401
    },
    "MethodNotAllowed": {
        "message": "Method not allowed",
        "status": 405
    },
    "LoginRequiredException": {
        "message": "You need to be logged in to access this resource",
        "status": 403
    },
    "ResourceNotFoundException": {
        "message": "Could not find the resource you're trying to access",
        "status": 404
    },
    "PermissionDenied": {
        "message": "You do not have permission to access this Resource",
        "status": 401
    }
}
