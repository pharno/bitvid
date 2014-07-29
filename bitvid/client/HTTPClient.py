import requests
import json


class HTTPClient:

    def __init__(self, baseurl, clientBase=requests):
        self.baseurl = baseurl
        self.authtoken = ""
        self.userid = -1
        self.request = clientBase

    def _json(self, response):
        if response.__class__.__name__ == "Response":  # flask test app
            return json.loads(response.data)
        else:
            return response.json()

    def _request(self, op, url, data):
        headers = {
            "Content-Type": "application/json"
            #            "token": self.authtoken
        }

        if self.authtoken:
            headers["token"] = self.authtoken

        fullurl = self.baseurl + url
        print fullurl
        val = op(fullurl, data=json.dumps(data), headers=headers)
        responsecode = None
        if val.__class__.__name__ == "Response":  # flask test app
            responsecode = val.status
        else:
            responsecode = val.status_code

        reason = requests.status_codes.codes[responsecode]
        if 400 <= responsecode < 500:
            http_error_msg = '%s Client Error: %s' % (responsecode, reason)
            raise Exception(http_error_msg)

        elif 500 <= responsecode < 600:
            http_error_msg = '%s Server Error: %s' % (self.status_code, reason)
            raise Exception(http_error_msg)

        return val

    def _post(self, url, data={}):
        val = self._request(self.request.post, url, data)
        return val

    def _get(self, url, data={}):
        val = self._request(self.request.get, url, data)
        return val

    def authenticate(self, email, password):
        print "authenticating {email}:{password}".format(email=email, password=password)
        logindata = {
            "email": email,
            "password": password
        }
        authdata = self._post("/auth/", logindata)
        print "authdata", self._json(authdata)
        if authdata.status_code is not 200:
            return False
        else:
            self.authtoken = self._json(authdata)["token"]
            print self.authtoken
            return True

    def register(self, email, password):
        print "registrating {email}:{password}".format(email=email, password=password)
        registerdata = {
            "email": email,
            "password": password
        }
        registerdata = self._post("/user/", registerdata)
        if registerdata.status_code is not 200:
            return False
        else:
            self.userid = self._json(registerdata)["id"]
            print self.userid
            return True

    def comment(self, title, content, video, parent=None):
        print "commenting: parent={parent} video={video} {title}:\n{content}".format(title=title, content=content, video=video, parent=parent)

        commentdata = {
            "title": title,
            "content": content,
            "parent": parent
        }

        returndata = self._post("/comment/", commentdata)

        print self._json(returndata)
        return self._json(returndata)["token"]

    def getComment(self, token):
        print "getting comment with token: " + token

        returndata = self._get("/comment/%s" % token)
        print "rawreturndata", returndata.data
        print self._json(returndata)
        return self._json(returndata)

    def _getVideoToken(self, title, description):
        print "getting Video Token: {title}\n{description}".format(title=title, description=description)

        videoTokenData = {
            "title": title,
            "description": description
        }

        returndata = self._post("/video/", videoTokenData)

        return self._json(returndata)["token"]
