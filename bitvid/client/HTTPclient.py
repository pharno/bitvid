import requests
import json

class HTTPClient:
    def __init__(self,baseurl):
        self.baseurl = baseurl
        self.authtoken = ""
        self.userid = -1

    def _request(self,op,url,data):
        headers = {
            "Content-Type": "application/json"
            #"token": self.authtoken
        }

        fullurl = self.baseurl+url
        print fullurl
        val = op(fullurl,data=json.dumps(data),headers=headers)

        return val

    def _post(self,url,data):
        val = self._request(requests.post,url,data)
        return val

    def authenticate(self,email,password):
        print "authenticating {email}:{password}".format(email=email,password=password)
        logindata = {
          "email" : email,
          "password" : password
        }
        authdata = self._post("/auth/",logindata)
        if authdata.status_code is not 200:
            return False;
        else:
            self.authtoken = authdata.json()["token"]
            print self.authtoken
            return True

    def register(self,email,password):
        print "registrating {email}:{password}".format(email=email,password=password)
        registerdata = {
          "email" : email,
          "password" : password
        }
        registerdata = self._post("/user/",registerdata)
        if registerdata.status_code is not 200:
            return False;
        else:
            self.userid = registerdata.json()["id"]
            print self.userid
            return True


client = HTTPClient("http://local.bitvid.tv:5000")

import random
import string

user = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))


email, password = user+"@local.bitvid.tvaaa","somepassword"

if not client.authenticate(email,password):
    client.register(email,password)

client.authenticate(email,password)
#myvideo = client.uploadVideo("/home/pharno/Downloads/Adam goes to Vidcon.mp4")

#print myvideo