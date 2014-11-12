__author__ = 'pharno'

import os

from bitvid.bitvid import app
if __name__ == '__main__':
    app.run(os.environ.get("HOST","127.0.0.1"))
