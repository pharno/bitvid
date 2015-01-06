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
if __name__ == '__main__' and not application.config["WORKER"]:
    application.run(os.environ.get("HOST","127.0.0.1"))
else:
    os.system("celery -A bitvid.tasks worker -l debug")