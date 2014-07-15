
__author__ = 'pharno'


import os
import unittest
import subprocess
import sys
import signal
import time

from bitvid.client.HTTPClient import HTTPClient

class BaseTest(unittest.TestCase):

    def setUp(self):

        env = os.environ.copy()
        env["BITVID_ENV"] = "Test"
        self.server_proc = subprocess.Popen(
            [sys.executable, 'app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env)
        time.sleep(1)
        """self.db_fd, bitvid.app.config['DATABASE'] = tempfile.mkstemp()
                                bitvid.app.config['TESTING'] = True
                                self.app = bitvid.app.test_client()
                                bitvid.init_db()"""
        self.client = HTTPClient("http://local.bitvid.tv:5000")

        self._setup()

    def _setup(self):
        pass

    def tearDown(self):
        """        os.close(self.db_fd)
        os.unlink(bitvid.app.config['DATABASE'])"""
        os.kill(self.server_proc.pid, signal.SIGINT)
        self._teardown()

    def _teardown(self):
        pass


if __name__ == '__main__':
    unittest.main()