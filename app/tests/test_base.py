import os
import sys
import unittest
import threading
import time

from selenium import webdriver
from selenium.webdriver.support.select import Select
from flask import current_app

from app.db import init_db, db_session, get_db_metadata, load_all, serialize_all
from config import get_env_config
from run import get_decorated_app
from app import create_app

DB_PICKLE_NAME = 'testing.db'

class AppTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ['APP_SETTINGS'] == 'testing' or os.environ.update(APP_SETTINGS='testing')
        cls.config_obj = get_env_config()
        cls.meta_db = get_db_metadata()
        init_db(seed_data=True, rebuild=True)
#        cls.backup_db = os.path.join(cls.config_obj.BASE_DIR, DB_PICKLE_NAME)
#        serialize_all(cls.backup_db)

    def setUp(self):
        self.app = get_decorated_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = db_session()
        #init_db()
        #load_all(self.backup_db)
        self.client = self.app.test_client(use_cookies=True)


    def tearDown(self):
        db_session.remove()
#        self.meta_db.drop_all()
        self.app_context.pop()
        if 'sqlite' in self.config_obj.SQLALCHEMY_DATABASE_URI:
            os.remove(os.path.join(self.config_obj.BASE_DIR, self.config_obj.db_path))

    @classmethod
    def tearDownClass(cls):
#        if os.path.exists(cls.backup_db):
#            os.remove(cls.backup_db)
        cls.meta_db.drop_all()

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
        if 'sqlite' in self.config_obj.SQLALCHEMY_DATABASE_URI:
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

            # suppress logging
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            # instead of rebuilding each time, take a snapshot of db and reload that
            cls.db = db_session()
            cls.meta_db = get_db_metadata()

            # need to find a way to make this work
            # serialize_all(DB_PICKLE_NAME, cls.meta_db)

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
            if 'sqlite' in cls.config_obj.SQLALCHEMY_DATABASE_URI:
                os.remove(os.path.join(cls.config_obj.BASE_DIR, cls.config_obj.db_path))

            cls.app_context.pop()

            # remove the db image file if it is present
            # backup_db = os.path.join(cls.config_obj.BASE_DIR, DB_PICKLE_NAME)
            # if os.path.exists(backup_db):
            #    os.remove(backup_db)

    def setUp(self):
        if not self.client:
            self.skipTest("Client not initialized")
        else:
            self.client.implicitly_wait(3)
            init_db(rebuild=True, seed_data=True)
            # load_all(DB_PICKLE_NAME, self.meta_db)

    def tearDown(self):
        """
        Tests if another client is defined.  If it is, destroy it
        :return: None
        """
        if hasattr(self, 'other_client'):
            try:
                self.other_client.close()
            except ConnectionRefusedError:
                pass

        self.go_to('auth/logout')
        db_session.remove()
        self.meta_db.drop_all()

    def go_to(self, address, other_client=None):
        client = other_client if other_client else self.client
        client.get('{}/{}'.format(self.server_url, address))

    def login(self, email, password, other_client=None):
        """
        :param email: the email for the login
        :param password: the password for the login
        :param other_client: if you want to perform login in another driver pass in a driver
        otherwise this uses self.client
        :return: None
        """
        client = other_client if other_client else self.client
        client.get('{}/{}'.format(self.server_url, 'auth/login'))
        client.find_element_by_id('email').send_keys(email)
        client.find_element_by_id('password').send_keys(password)
        client.find_element_by_xpath('//*[@type="submit"]').click()


    def create_item(self, title, composer, condition='Clean', other_client=None):
        client = other_client if other_client else self.client
        self.go_to('sheets/create?creating_item=1', client)
        client.find_element_by_id('title').send_keys(title)
        client.find_element_by_id('composer').send_keys(composer)
        client.find_element_by_xpath('//button[@type="submit"]').click()
        dd = Select(client.find_element_by_id('condition'))
        dd.select_by_visible_text(condition)
        client.find_element_by_xpath('//button[@type="submit"]').click()


    def register(self, e, n, p):
        self.go_to('auth/register')
        email = self.client.find_element_by_id('email')
        username = self.client.find_element_by_id('username')
        password = self.client.find_element_by_id('password')
        check_password = self.client.find_element_by_id('check_password')
        email.send_keys(e)
        username.send_keys(n)
        password.send_keys(p)
        check_password.send_keys(p)
        submit = self.client.find_element_by_xpath('//button[@type="submit"]')
        submit.click()
