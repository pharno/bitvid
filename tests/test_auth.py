__author__ = 'pharno'

from BaseTest import BaseTest


class AuthTest(BaseTest):
    username = "testuser"
    email = "testmail@local.bitvid.tv"
    password = "testpassword"
    newpassword = "newtestpassword"

    def _setup(self):
        self.client.register(self.username, self.email, self.password)

    def test_authentication_correct(self):
        assert self.client.authenticate(self.username, self.password)

    def test_authentication_password_incorrect(self):
        assert "message" in self.client.authenticate(self.username, "wrongpassword").keys()

    def test_authentication_email_incorrect(self):

        assert u"message" in self.client.authenticate(
            "wrongname", self.password).keys()

    def test_totally_wrong_credentials(self):
        assert "message" in self.client.authenticate(
            "wrongname", "wrongpassword")

    def test_unregister(self):
        self.client.unregister(self.email, self.password)
        assert "message" in self.client.authenticate(self.username, "wrongpassword").keys()

    def test_update(self):
        self.client.changePassword(self.username, self.password, self.newpassword)
        assert self.client.authenticate(self.username, self.newpassword)
