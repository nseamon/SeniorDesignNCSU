import http.client
import json
import os
import sqlalchemy
import time
import unittest, urllib

from flask import Flask, request, Response
from flask_cors import CORS
from flask_testing import TestCase

import app
import db
import models

from models import User


# port and host for API during testing
PORT = 5000
HOST = 'localhost'

# used to limit timing related test errors
SLEEP_TIME = .005


class TestAuth(TestCase):
    """
    Class Tests authentication parts of API
    """

    def create_app(self):
        """
        Creates app for testing
        """
        app = Flask(__name__)
        CORS(app)
        return app

    def setUp(self):
        """
        Deletes and recreates new blank tables so that testing is indempodent
        """
        models.Base.metadata.drop_all(db.engine)
        models.Base.metadata.create_all(db.engine)

    def tearDown(self):
        """
        Clears database
        """
        models.Base.metadata.drop_all(db.engine)

    def test_createAccount_bad(self):
        """ 
        Test for user registration with bad parameters 
        """

        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(HOST, PORT)
        
        senddata = {
            "email": "bimal@gmail.com",
            "password": "123456789",
            "secret_code": "SeniorDesignS2020"
        }
        json_data = json.dumps(senddata)
        conn.request('POST', '/createAccount', json_data, headers)
        response = conn.getresponse()
        conn.close()

        self.assertTrue(response.status == 400)
        self.assertTrue(response.reason == 'BAD REQUEST')


    def test_createAccount(self):
        """ 
        Test for valid user registration 
        """

        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(HOST, PORT)
        senddata = {
                "email": "bimal@gmail.com",
                "username": "bimalcreatAccount1",
                "password": "123456789",
                "secret_code": "SeniorDesignS2020"
            }
        json_data = json.dumps(senddata)
        conn.request('POST', '/createAccount' , json_data, headers)
        response = conn.getresponse()
        conn.close()

        self.assertTrue(response.status == 200)
        self.assertTrue(response.reason == 'OK')


    def test_createAccount_with_already_registered_user(self):
        """
        Tests adding and existing user
        """

        #first registered
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(HOST, PORT)

        senddata = {
            "email": "bimal@gmail.com",
            "username": "bimalcreataccounterror1",
            "password": "123456789",
            "secret_code": "SeniorDesignS2020"
        }

        json_data = json.dumps(senddata)
        conn.request('POST', '/createAccount', json_data, headers)
        conn.close()

        # needed because the database takes time to update
        time.sleep(SLEEP_TIME)
        
        #2nd reg dup
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(HOST, PORT)

        senddata = {
            "email": "bimal@gmail.com",
            "username": "bimalcreataccounterror1",
            "password": "123456789",
            "secret_code": "SeniorDesignS2020"
        }

        json_data = json.dumps(senddata)

        conn.request('POST', '/createAccount', json_data, headers)
        response = conn.getresponse()
        conn.close()

        self.assertTrue(response.status == 401)
        self.assertTrue(response.reason == 'UNAUTHORIZED')

    def test_login_missing_info(self):
        """
        Tests login; password param missing
        """

        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(HOST, PORT)
        
        # login
        senddata = {
            "username": "bimalloginerrorNO1"
        }

        json_data = json.dumps(senddata)

        conn.request('POST', '/login', json_data, headers)
        response = conn.getresponse()
        conn.close()

        self.assertTrue(response.status == 400)
        self.assertTrue(response.reason == 'BAD REQUEST')


    def test_login_not_in_system(self):
        """
        Tests user not in database
        """

        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(HOST, PORT)
        
        # login
        senddata = {
            "username": "bimalloginerror1",
            "password": "123456789"
        }

        json_data = json.dumps(senddata)

        conn.request('POST', '/login', json_data, headers)
        response = conn.getresponse()
        conn.close()

        self.assertTrue(response.status == 404)
        self.assertTrue(response.reason == 'NOT FOUND')



    def test_login(self):
        """ 
        Tests valid registration and login
        """

        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(HOST, PORT)
        
        # register

        senddata = {
            "email": "bimal@gmail.com",
            "username": "bimallogin_1",
            "password": "123456789",
            "secret_code": "SeniorDesignS2020"
        }

        json_data = json.dumps(senddata)
        conn.request('POST', '/createAccount', json_data, headers)
        conn.close()

        # avoids timing errors
        time.sleep(SLEEP_TIME)
        
        #login
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(HOST, PORT)
        senddata = {
            "username": "bimallogin_1",
            "password": "123456789"
        }
        json_data = json.dumps(senddata)

        conn.request('POST', '/login', json_data, headers)
        response = conn.getresponse()
        conn.close()
 
        self.assertTrue(response.status == 200)
        self.assertTrue(response.reason == 'OK')




    def test_logout_error(self):
        """

        """

        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(HOST, PORT)

        #make user
        senddata = {
            "email": "bimal@gmail.com",
            "username": "bimallogouterror_1",
            "password": "123456789",
            "secret_code": "SeniorDesignS2020"
        }

        json_data = json.dumps(senddata)
        conn.request('POST', '/createAccount', json_data, headers)
        conn.close()

        #login
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(HOST, PORT)
        
        senddata = {
            "username": "bimallogouterror_1",
            "password": "123456789"
        }

        json_data = json.dumps(senddata)
        conn.request('POST', '/login', json_data, headers)
        conn.close()

        #logout
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(HOST, PORT)
        
        senddata = {
            "username": "bimallogouterror_"
        }

        json_data = json.dumps(senddata)
        conn.request('POST', '/logout', json_data, headers)
        response = conn.getresponse()
        conn.close()

        self.assertTrue(response.status == 404)
        self.assertTrue(response.reason == 'NOT FOUND')

    def test_logout(self):
        """
        Valid logout
        """

        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(HOST, PORT)
        
        #add user
        senddata = {
            "email": "bimal@gmail.com",
            "username": "bimallogout_1",
            "password": "123456789",
            "secret_code": "SeniorDesignS2020"
        }

        json_data = json.dumps(senddata)
        conn.request('POST', '/createAccount', json_data, headers)
        conn.close()

        # login
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(HOST, PORT)
        
        senddata = {
            "username": "bimallogout_1",
            "password": "123456789"
        }

        json_data = json.dumps(senddata)
        conn.request('POST', '/login', json_data, headers)
        conn.close()

        time.sleep(SLEEP_TIME)

        # logout
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(HOST, PORT)
        
        senddata = {
            "username": "bimallogout_1"
        }

        json_data = json.dumps(senddata)
        conn.request('POST', '/logout', json_data, headers)
        response = conn.getresponse()
        conn.close()

        self.assertTrue(response.status == 200)
        self.assertTrue(response.reason == 'OK')


if __name__ == '__main__':
    unittest.main()
