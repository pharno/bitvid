
from BaseTest import BaseTest
from bitvid import errors


class VideoTest(BaseTest):
    email = "testmail@local.bitvid.tv"
    password = "testpassword"

    firstTitle = "firstTitle"
    firstDescription = "this is the first video description"

    secondTitle = "secondTitle"
    secondDescription = "this is the second video description"

    videoFile = "./data/video/small.mp4"

    def _setup(self):
        self.client.register(self.email, self.password)
        self.client.authenticate(self.email, self.password)

        self.videoToken = self.client._getVideoToken(self.firstTitle,self.firstDescription)

    def test_uploadVideo(self):
        vid = open(self.videoFile, "r")
        vidret = self.client.uploadVideo(self.videoToken, vid)

        print vidret
        assert vidret["token"] == self.videoToken
        assert vidret["title"] == self.firstTitle
        assert vidret["description"] == self.firstDescription

    def test_updateVideoTitleAndDescription(self):
        update = self.client.updateVideo(self.videoToken, self.secondTitle, self.secondDescription)

        assert update["title"] == self.secondTitle
        assert update["description"] == self.secondDescription