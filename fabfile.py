__author__ = 'pharno'

from bitvid.bitvid import init_db as init_bitvid_db
from fabric.operations import local


def init_db():
    init_bitvid_db()


def reset():
    local("rm database.sqlite")
    local("curl -XDELETE http://localhost:9200/bitvid")
    init_db()

def pep8():
    local("autopep8 --aggressive --aggressive --in-place -r bitvid")
