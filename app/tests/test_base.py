import os
import sys
import unittest
from selenium import webdriver
import threading

from flask import current_app
from app.db import init_db, db_session, get_db_metadata
from config import get_env_config
from run import get_decorated_app
from app import create_app

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

class SeleniumTest(unittest.TestCase):
    client = None


    @classmethod
    def setUpClass(cls):
        # start the driver
        try:
            cls.client = webdriver.Firefox()
        except:
            pass

        if cls.client:
            os.environ['APP_SETTINGS'] == 'testing' or os.environ.update(APP_SETTINGS='testing')
            cls.config_obj = get_env_config()
            cls.app = get_decorated_app()
            cls.app_context = cls.app.test_request_context()
            cls.app_context.push()

            # supress logging
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            cls.db = db_session()
            cls.meta_db = get_db_metadata()
            init_db(seed_data=True, rebuild=True)

            # the server url
            cls.host = 'localhost'
            cls.port = 5001
            cls.server_url = 'http://{}:{}'.format(cls.host, cls.port)

            threading.Thread(target=lambda: cls.app.run(port=cls.port)).start()

    @classmethod
    def tearDownClass(cls):

        if cls.client:
            cls.client.get("{}/{}".format(cls.server_url, 'testing/shutdown'))
            cls.client.close()

            db_session.remove()
            cls.meta_db.drop_all()
            if 'sqlite' in cls.config_obj.db_path:
                os.remove(os.path.join(cls.config_obj.BASE_DIR, cls.config_obj.db_path))
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest("Client not initialized")
        else:
            self.client.implicitly_wait(3)


    def tearDown(self):
        pass


