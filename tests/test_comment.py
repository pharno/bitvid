
from BaseTest import BaseTest

class AuthTest(BaseTest):
    email = "testmail@local.bitvid.tv"
    password = "testpassword"

    firstTitle = "firstTitle"
    firstContent = "this is some content for the first comment"


    secondTitle = "secondTitle"
    secondContent = "this is some content for the second comment"


    def _setup(self):
        self.client.register(self.email,self.password)
        self.client.authenticate(self.email,self.password)

        self.videoToken = self.client._getVideoToken("title","desc")

    def test_singleComment(self):
        returndata = self.client.comment(self.firstTitle,self.firstContent,self.videoToken)
        assert returndata != None

    def test_multipleComments(self):
        returndata = self.client.comment(self.firstTitle,self.firstContent,self.videoToken)
        assert returndata != None

        returndata = self.client.comment(self.secondTitle,self.secondContent,self.videoToken)
        assert returndata != None

    def test_treeComments(self):
        returndata = self.client.comment(self.firstTitle,self.firstContent,self.videoToken)
        assert returndata != None

        returndata = self.client.comment(self.secondTitle,self.secondContent,self.videoToken, returndata)
        assert returndata != None