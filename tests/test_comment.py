
from BaseTest import BaseTest
from bitvid import errors


class AuthTest(BaseTest):
    username ="testuser"
    email = "testmail@local.bitvid.tv"
    password = "testpassword"

    firstTitle = "firstTitle"
    firstContent = "this is some content for the first comment"

    firstTitleChanged = "changedFirstTitle"
    firstContentChanged = "I changed the Content of this comment. yo"

    secondTitle = "secondTitle"
    secondContent = "this is some content for the second comment"

    def _setup(self):
        self.client.register(self.username, self.email, self.password)
        self.client.authenticate(self.username, self.password)

        self.videoToken = self.client._getVideoToken("titleforvideo", "descforvideo")["token"]

    def test_singleComment(self):
        assert self._send_and_get_comment(
            self.firstTitle, self.firstContent, self.videoToken)

    def _send_and_get_comment(self, title, content, videoToken):
        token = self.client.comment(title, content, videoToken)

        returndata = self.client.getComment(token["token"])
        assert returndata["title"] == title
        assert returndata["content"] == content
        assert returndata["author"] == self.username

        return True

    def test_getComment(self):
        assert self._send_and_get_comment(
            self.firstTitle, self.firstContent, self.videoToken)

    def test_multipleComments(self):
        assert self._send_and_get_comment(
            self.firstTitle, self.firstContent, self.videoToken)
        assert self._send_and_get_comment(
            self.secondTitle, self.secondContent, self.videoToken)

    def test_getCommentsForVideo(self):
        assert self._send_and_get_comment(
            self.firstTitle, self.firstContent, self.videoToken)
        assert self._send_and_get_comment(
            self.secondTitle, self.secondContent, self.videoToken)

        returndata = self.client.getCommentsForVideo(self.videoToken)

        assert len(returndata) == 2
        assert returndata[0]["title"] == self.firstTitle
        assert returndata[1]["title"] == self.secondTitle

    def test_deleteComment(self):
        token = self.client.comment(
            self.firstTitle, self.firstContent, self.videoToken)["token"]

        returndata = self.client.getComment(token)
        assert returndata["title"] == self.firstTitle
        assert returndata["content"] == self.firstContent
        assert returndata["author"] == self.username

        deletedata = self.client.deleteComment(token)

        assert deletedata["token"] == token

        returndata = self.client.getComment(token)
        print returndata
        assert returndata["message"] == errors.errors["NotFound"]["message"]

    def test_updateComement(self):
        token = self.client.comment(
            self.firstTitle, self.firstContent, self.videoToken)["token"]

        returndata = self.client.getComment(token)
        assert returndata["title"] == self.firstTitle
        assert returndata["content"] == self.firstContent
        assert returndata["author"] == self.username

        self.client.updateComment(
            token, self.firstTitleChanged, self.firstContentChanged)

        returndata = self.client.getComment(token)

        print "returndata update", returndata
        assert returndata["title"] == self.firstTitleChanged
        assert returndata["content"] == self.firstContentChanged
        assert returndata["author"] == self.username

    def test_commentUnauthorized(self):
        self.client.authtoken = None
        unauthData = self.client.comment(self.firstTitle, self.firstContent, self.videoToken)

        assert unauthData["message"] == errors.errors["LoginRequiredException"]["message"]

    def test_updateCommentUnauthorized(self):
        token = self.client.comment(
            self.firstTitle, self.firstContent, self.videoToken)["token"]

        returndata = self.client.getComment(token)
        assert returndata["title"] == self.firstTitle
        assert returndata["content"] == self.firstContent
        assert returndata["author"] == self.username

        self.client.authtoken = None

        returndata = self.client.updateComment(
            token, self.firstTitleChanged, self.firstContentChanged)


        assert returndata["message"] == errors.errors["LoginRequiredException"]["message"]


    def test_updateCommentWrongUser(self):
        token = self.client.comment(
            self.firstTitle, self.firstContent, self.videoToken)["token"]

        returndata = self.client.getComment(token)
        assert returndata["title"] == self.firstTitle
        assert returndata["content"] == self.firstContent
        assert returndata["author"] == self.username

        self.client.authtoken = None

        self.client.register("otheruser", "other"+self.email, self.password)
        self.client.authenticate("otheruser", self.password)

        returndata = self.client.updateComment(
            token, self.firstTitleChanged, self.firstContentChanged)


        assert returndata["message"] == errors.errors["PermissionDenied"]["message"]


    def test_deleteCommentUnauthorized(self):
        token = self.client.comment(
            self.firstTitle, self.firstContent, self.videoToken)["token"]

        returndata = self.client.getComment(token)
        assert returndata["title"] == self.firstTitle
        assert returndata["content"] == self.firstContent
        assert returndata["author"] == self.username

        self.client.authtoken = None

        deletedata = self.client.deleteComment(token)

        assert deletedata["message"] == errors.errors["LoginRequiredException"]["message"]

        returndata = self.client.getComment(token)

        assert returndata["title"] == self.firstTitle
        assert returndata["content"] == self.firstContent
        assert returndata["author"] == self.username

    def test_deleteCommentWrongUser(self):
        token = self.client.comment(
            self.firstTitle, self.firstContent, self.videoToken)["token"]

        returndata = self.client.getComment(token)
        assert returndata["title"] == self.firstTitle
        assert returndata["content"] == self.firstContent
        assert returndata["author"] == self.username

        self.client.register("otheruser", "other"+self.email, self.password)
        self.client.authenticate("otheruser", self.password)
        deletedata = self.client.deleteComment(token)

        print "deletedata:",deletedata
        assert deletedata["message"] == errors.errors["PermissionDenied"]["message"]

        returndata = self.client.getComment(token)

        assert returndata["title"] == self.firstTitle
        assert returndata["content"] == self.firstContent
        assert returndata["author"] == self.username