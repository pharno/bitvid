
class UserExistsException(Exception):
	pass


errors = {
	"Exception" : {
		"message" : "Internal Server Error",
		"status"  : 500
	},
	"UserExistsException" : {
		"message" : "User with this email already exists",
		"status"  : 409
	}
}