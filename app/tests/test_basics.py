import unittest
from flask import current_app
from app.db import init_db, db_session
from app import create_app

class BasicsTestCase(unittest.TestCase)
    def setUp(selfself):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = db_session()


    def tearDown(self):
        db_session.remove()
        db_session.drop_all()
        sel