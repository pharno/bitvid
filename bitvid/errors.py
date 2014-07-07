
class UserExistsException(Exception):
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
    }
}