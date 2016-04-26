import unittest
from flask import current_app
from app.db import init_db, db_session, get_db_metadata
from app import create_app
import os
from config import get_env_config

class AppTest(unittest.TestCase):
    def setUp(self):
        os.environ['APP_SETTINGS'] == 'testing' or os.environ.update(APP_SETTINGS='testing')
        self.config_obj = get_env_config()
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = db_session()
        init_db()
        self.meta_db = get_db_metadata()
        self.client = self.app.test_client(use_cookies=True)


    def tearDown(self):
        db_session.remove()
        self.meta_db.drop_all()
        self.app_context.pop()
        if 'sqlite' in self.config_obj.db_path:
            os.remove(os.path.join(self.config_obj.BASE_DIR, self.config_obj.db_path))

class DBTest(unittest.TestCase):
    def setUp(self):
        os.environ['APP_SETTINGS'] == 'testing' or os.environ.update(APP_SETTINGS='testing')
        self.config_obj = get_env_config()
        self.db = db_session()
        init_db()
        self.meta_db = get_db_metadata()

    def tearDown(self):
        db_session.remove()
        self.meta_db.drop_all()
        if 'sqlite' in self.config_obj.db_path:
            os.remove(os.path.join(self.config_obj.BASE_DIR, self.config_obj.db_path))
