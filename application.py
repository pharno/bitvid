__author__ = 'pharno'

import os

from bitvid.bitvid import app as application

if __name__ == '__main__' and not application.config["WORKER"]:
    application.run(os.environ.get("HOST","127.0.0.1"))
else:
    os.system("celery -A bitvid.tasks worker -l debug")