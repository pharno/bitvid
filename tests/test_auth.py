__author__ = 'pharno'

from BaseTest import BaseTest

class AuthTest(BaseTest):
    email = "testmail@local.bitvid.tv"
    password = "testpassword"

    def _setup(self):
        self.client.register(self.email,self.password)

    def test_something(self):
        self.client.authenticate(self.email,self.password)