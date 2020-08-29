import unittest

from sqlalchemy import Column, Integer, String
from sqlbatis import SQLBatis, Model


class User(Model):

    id = Column(Integer, primary_key=True)
    name = Column(String)
    full_name = Column(String)


db = SQLBatis('sqlite:///:memory:')
User._create_table_instance(db.metadata)


class BasicTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.metadata.create_all()

    @classmethod
    def tearDownClass(cls):
        # pass
        db.metadata.drop_all()
        # pass
