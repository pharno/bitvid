
__author__ = 'pharno'


import os
os.environ["BITVID_ENV"] = "Test"

import unittest
import subprocess
import sys
import signal
import time
import tempfile
from bitvid import bitvid
from bitvid.shared import get_es, get_es_index

from bitvid.client.HTTPClient import BitvidClient

class BaseTest(unittest.TestCase):

    def setUp(self):
        """env = os.environ.copy()
        env["BITVID_ENV"] = "Test"
        self.server_proc = subprocess.Popen(
            [sys.executable, 'app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env)
        time.sleep(1)"""
        self.db_fd, self.db_filename = tempfile.mkstemp()
        bitvid.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://" #/"+self.db_filename
        bitvid.app.config['TESTING'] = True
        self.app = bitvid.app.test_client()
        bitvid.init_db()
        self.client = BitvidClient("http://local.bitvid.tv:5000",self.app)

        self._setup()

    def _setup(self):
        pass

    def tearDown(self):
        with bitvid.app.app_context():
            try:
                get_es().delete_index(get_es_index())
            except:
                pass

        os.close(self.db_fd)
        os.unlink(self.db_filename)
        bitvid.destroy_db()
        """os.kill(self.server_proc.pid, signal.SIGINT)
        self._teardown()"""

    def _teardown(self):
        pass


if __name__ == '__main__':
    unittest.main()