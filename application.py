__author__ = 'pharno'

import os

from bitvid.bitvid import app as application

print """Config:
Worker: {Worker}
Debug:  {Debug}

Env:""".format(
    Worker=repr(application.config["WORKER"]),
    Debug=repr(application.config["DEBUG"]))

for key,value in os.environ.items():
    print "{key} = {value}".format(key=key,value=value)

if application.config["WORKER"]:
    os.system("celery -A bitvid.tasks worker -l debug")

if __name__ == '__main__':
    application.run(os.environ.get("HOST","127.0.0.1"),int(os.environ.get("PORT",5000)))

