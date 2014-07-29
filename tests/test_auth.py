__author__ = 'pharno'

from nose.tools import assert_raises
from BaseTest import BaseTest

class AuthTest(BaseTest):
    email = "testmail@local.bitvid.tv"
    password = "testpassword"

    def _setup(self):
        self.client.register(self.email,self.password)

    def test_authentication_correct(self):
        assert self.client.authenticate(self.email,self.password)

    def test_authentication_password_incorrect(self):
        assert self.client.authenticate(self.email,"wrongpassword") == False

    def test_authentication_email_incorrect(self):
        assert self.client.authenticate("wrong@email.tv",self.password) == False

    def test_totally_wrong_credentials(self):
        assert self.client.authenticate("wrong@email.tv","wrongpassword") == False