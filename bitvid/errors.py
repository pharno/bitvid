
class UserExistsException(Exception):
	pass


errors = {
	"UserExistsException" : {
		"message" : "User with this email already exists",
		"status"  : 409
	}
}