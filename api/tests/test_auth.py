import http.client
import json
import os
import sqlalchemy
import sys
import time
import unittest, urllib

from flask import Flask, request, Response
from flask_cors import CORS
from flask_testing import TestCase

sys.path.append('..')

from app import application
import db
import models
import api

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
        return application 


    def setUp(self):
        """
        Deletes and recreates new blank tables so that testing is idempotent
        Creates a user and logs the user in to generate session token
        """
        self.app = self.create_app()
        self.client = self.app.test_client

        time.sleep(.01)
        models.Base.metadata.drop_all(db.engine)

        time.sleep(.01)
        models.Base.metadata.create_all(db.engine)


    def tearDown(self):
        """
        Clears database
        """
        models.Base.metadata.drop_all(db.engine)


    def post(self, endpoint, body):
        headers = {'Content-type': 'application/json'}
        return self.client().post(endpoint, headers=headers, data=body)
    

    def test_createAccount_bad(self):
        """ 
        Test for user registration with bad parameters 
        """

        body = {
            "email": "bimal@gmail.com",
            "password": "123456789",
            "secret_code": "SeniorDesignS2020"
        }

        response = self.post("createAccount", json.dumps(body))
        self.assertEqual(400, response.status_code)


    def test_createAccount(self):
        """ 
        Test for valid user registration 
        """

        body = {
                "email": "bimal@gmail.com",
                "username": "bimalcreatAccount1",
                "password": "123456789",
                "secret_code": "SeniorDesignS2020"
            }
        
        response = self.post("createAccount", json.dumps(body))
        self.assertEqual(200, response.status_code)


    def test_createAccount_with_already_registered_user(self):
        """
        Tests adding and existing user
        """

        #first registered
        body = {
            "email": "bimal@gmail.com",
            "username": "bimalcreataccounterror1",
            "password": "123456789",
            "secret_code": "SeniorDesignS2020"
        }

        response = self.post("createAccount", json.dumps(body))

        # needed because the database takes time to update
        time.sleep(SLEEP_TIME)
        
        #2nd reg dup
        senddata = {
            "email": "bimal@gmail.com",
            "username": "bimalcreataccounterror1",
            "password": "123456789",
            "secret_code": "SeniorDesignS2020"
        }

        response = self.post("createAccount", json.dumps(body))
        self.assertEqual(400, response.status_code)


    def test_login_missing_info(self):
        """
        Tests login; password param missing
        """
        
        # login
        body = {
            "username": "bimalloginerrorNO1"
        }

        response = self.post("login", json.dumps(body))

        self.assertEqual(400, response.status_code)


    def test_login_not_in_system(self):
        """
        Tests user not in database
        """

        # login
        body = {
            "username": "bimalloginerror1",
            "password": "123456789"
        }

        response = self.post("login", json.dumps(body))

        self.assertEqual(404, response.status_code)




    def test_login(self):
        """ 
        Tests valid registration and login
        """
       
        # register
        body = {
            "email": "bimal@gmail.com",
            "username": "bimallogin_1",
            "password": "123456789",
            "secret_code": "SeniorDesignS2020"
        }

        response = self.post("createAccount", json.dumps(body))

        # avoids timing errors
        time.sleep(SLEEP_TIME)
        
        #login
        body = {
            "username": "bimallogin_1",
            "password": "123456789"
        }

        response = self.post("login", json.dumps(body))
 
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.json['token'])



    def test_logout_error(self):
        """
        Logout error 
        """

        #make user
        body = {
            "email": "bimal@gmail.com",
            "username": "bimallogouterror_1",
            "password": "123456789",
            "secret_code": "SeniorDesignS2020"
        }

        self.post("createAccount", json.dumps(body))

        body = {
            "username": "bimallogouterror_1",
            "password": "123456789"
        }

        response = self.post("login", json.dumps(body))
       
        #logout
        body = {
            "username": "bimallogouterror_"
        }

        response = self.post("logout", json.dumps(body))
        self.assertEqual(404, response.status_code)


    def test_logout(self):
        """
        Valid logout
        """

        #add user
        body = {
            "email": "bimal@gmail.com",
            "username": "bimallogout_1",
            "password": "123456789",
            "secret_code": "SeniorDesignS2020"
        }

        self.post("createAccount", json.dumps(body))

        # login
        body = {
            "username": "bimallogout_1",
            "password": "123456789"
        }

        response = self.post("login", json.dumps(body))

        time.sleep(SLEEP_TIME)

        # logout
        body = {
            "username": "bimallogout_1"
        }

        response = self.post("logout", json.dumps(body))
        self.assertEqual(200, response.status_code)



if __name__ == '__main__':
    unittest.main()
