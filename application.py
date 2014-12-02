__author__ = 'pharno'

import os

from bitvid.bitvid import app as application

if __name__ == '__main__':
    application.run(os.environ.get("HOST","127.0.0.1"))
