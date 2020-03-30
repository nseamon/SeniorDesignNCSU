import http.client
import json
import os
import sqlalchemy
import sys 
import time
import unittest, urllib

from flask import Flask, request, Response
from flask_testing import TestCase

sys.path.append('..')

import app
import db
import models

from db import engine

# port and host for API during testing
PORT = 5000
HOST = 'localhost'

# used to limit timing related test errors
SLEEP_TIME = .005

class TestAPI(TestCase):
    """
    Class Tests API
    """ 

    TOKEN = None

    def create_app(self):
        """
        Creates app for testing
        """
        app = Flask(__name__)
        return app


    def addUser(self):   
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(HOST, PORT)
        
        data = {
            "username": "ndseamon",
            "email": "ndseamon@gmail.com",
            "password": "password",
            "secret_code": "SeniorDesignS2020"
        }

        json_data = json.dumps(data)
        conn.request('POST', '/createAccount', json_data, headers)
        conn.close()


    def login(self):
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(HOST, PORT)

        body = {
            "username": "ndseamon",
            "password": "password"
        }

        json_data = json.dumps(body)
        conn.request('POST', '/login', json_data, headers)
        response = conn.getresponse()

        token =  json.loads(response.read().decode('utf-8'))['token']
        conn.close()
        return token


    def setUp(self):
        """
        Deletes and recreates new blank tables so that testing is idempotent
        Creates a user and logs the user in to generate session token
        """
        time.sleep(.01)
        models.Base.metadata.drop_all(engine)

        time.sleep(.01)
        models.Base.metadata.create_all(engine)

        time.sleep(.01)
        self.addUser()

        time.sleep(.01)
        self.TOKEN = self.login()


    def request(self, body, endpoint, method):
        """
        Method used to cut down on duplicated code. Takes parameters to make request 
        and returns the http response. Includes Auth

        :param: body of request
        :param: string value of endpoint to use
        :param: http method used (ie POST)
        :return: http response object
        """
        headers = {'Content-type': 'application/json', 'Authorization': "Bearer " + self.TOKEN}
        conn = http.client.HTTPConnection(HOST, PORT)
        conn.request(method, endpoint, json.dumps(body), headers)
        response = conn.getresponse()
        conn.close()
        
        return response


    def requestWithQueryParams(self, endpoint, method, query_params=None):
        """
        Method used to cut down on duplicated code. Takes parameters to make request 
        and returns the http response. Includes Auth

        :param: body of request
        :param: string value of endpoint to use
        :param: query param (list of tuples)
        :return: http response object
        """
        if query_params:
            if method == "DELETE":
                endpoint = endpoint + "?" + query_params[0][0] + "=" + query_params[0][1]
            else:
                endpoint = endpoint + "?"
                for item in query_params:
                    endpoint = endpoint + item[0] + "=" + item[1] + "&"

        headers = {'Content-type': 'application/json', 'Authorization': "Bearer " + self.TOKEN}
        conn = http.client.HTTPConnection(HOST, PORT)
        conn.request(method, endpoint, headers=headers)
        response = conn.getresponse()
        conn.close()
        
        return response
    
    def getWithQueryParamsNoAuth(self, endpoint, query_params=None):
        """
        Method used to cut down on duplicated code. Takes parameters to make request 
        and returns the http response. Includes Auth

        :param: body of request
        :param: string value of endpoint to use
        :param: query param (list of tuples)
        :return: http response object
        """
        if query_params:
            endpoint = endpoint + "?"
            for item in query_params:
                endpoint = endpoint + item[0] + "=" + item[1] + "&"

        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(HOST, PORT)
        conn.request("GET", endpoint, headers=headers)
        response = conn.getresponse()
        conn.close()
        
        return response

    def requestNoAuth(self, body, endpoint, method):
        """
        Method used to cut down on duplicated code. Takes parameters to make request 
        and returns the http response. Does not include auth

        :param: body of request
        :param: string value of endpoint to use
        :param: http method used (ie POST)
        :return: http response object
        """
        headers = {'Content-type': 'application/json'}
        conn = http.client.HTTPConnection(HOST, PORT)
        conn.request(method, endpoint, json.dumps(body), headers=headers)
        response = conn.getresponse()
        conn.close()
        
        return response


"""
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
This section tests raw text entry posts, delete and get functions
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""
class TestRawPostAndGetRaw(TestAPI):
    
    VALID_RAW_BODY = {
        
        "raw_text": "I love Merck", 
        "time": "2020-26-02 15:34:00", 
        "source": "TWITTER",
        "lat": "56.3304",
        "lon": "130.3221",
        "author": "Donald Trump"
    }

    VALID_RAW_BODY_TWO = {
        "raw_text": "I hate Merck becuase they kill babies 😠", 
        "time": "2020-01-03 03:33:21", 
        "source": "TWITTER",
        "lat": "56.3304",
        "lon": "130.3221",
        "author": "Andrew Goncharov"
    }

    VALID_RAW_BODY_THREE = {
        "raw_text": "I hate Merck becuase they give babies autism with their vaccines 😠", 
        "time": "2020-01-03 03:33:21", 
        "source": "TWITTER",
        "lat": "26.39",
        "lon": "129.19",
        "author": "Nathan Seamon"
    }

    RETURN_BODY_TWO = {
        'author': 'Andrew Goncharov', 
        'emojis': False, 
        'id': 2, 
        'lat': 56.3304, 
        'lon': 130.3221, 
        'processed': False, 
        'raw_text': 'I hate Merck becuase they kill babies 😠',
        'source': 'TWITTER', 
        'time': '2020-01-03 03:33:21'
    }

    def testPostRawTextEntryValid(self):
        """ 
        Test valid raw text entry post 
        """
        response = self.request(self.VALID_RAW_BODY, "/rawTextEntry", "POST")
        self.assertEqual(json.loads(response.read().decode('utf-8')), "Raw entry successfully added")
        self.assertEqual(200, response.status)


    def testPostRawTextEntryDuplicate(self):
        """ 
        Test duplicate raw entry failure 
        """

        # first post
        response = self.request(self.VALID_RAW_BODY, "/rawTextEntry", "POST")
        
        # first post sanity check
        self.assertEqual(json.loads(response.read().decode('utf-8')), "Raw entry successfully added")
        self.assertEqual(200, response.status)
        
        # second post
        response = self.request(self.VALID_RAW_BODY, "/rawTextEntry", "POST")
        
        # second post failure verification
        self.assertEqual(json.loads(response.read().decode('utf-8')), "Text entry with time and text already exists")
        self.assertEqual(400, response.status)


    def testPostRawInvalidDatetime(self):
        """
        Tests raw text entry post with invlaid time
        """
        
        body = {
            "raw_text": "I love Merck", 
            "time": "2020-36-02 5:34:0", 
            "source": "TWITTER",
            "lat": "56.3304",
            "lon": "130.3221",
            "author": "Donald Trump"
        }

        response = self.request(body, "/rawTextEntry", "POST")
        
        self.assertEqual(json.loads(response.read().decode('utf-8')), "Invalid time format, must be YYYY-DD-MM HH:MM:SS")
        self.assertEqual(400, response.status)


    def testPostRawNoAuthor(self):
        """
        Tests valid raw text entry post with out author
        """
        
        body = {
            "raw_text": "I love Merck", 
            "time": "2020-26-02 15:34:00", 
            "source": "TWITTER",
            "lat": "56.3304",
            "lon": "130.3221",
        }

        response = self.request(body, "/rawTextEntry", "POST")
        
        self.assertEqual(json.loads(response.read().decode('utf-8')), "Raw entry successfully added")
        self.assertEqual(200, response.status)


    def testInvalidLatLon(self):
        """
        Tests invalid lats and lons
        """
        
        # missing lon
        body = {
            "raw_text": "I love Merck", 
            "time": "2020-26-02 15:34:00", 
            "source": "TWITTER",
            "lat": "56.3304",
        }

        response = self.request(body, "/rawTextEntry", "POST")
        
        self.assertEqual(json.loads(response.read().decode('utf-8')), "Missing parameter lon")
        self.assertEqual(400, response.status)

        # missing lat
        body = {
            "raw_text": "I love Merck", 
            "time": "2020-26-02 15:34:00", 
            "source": "TWITTER",
            "lon": "130.3221",
        }

        response = self.request(body, "/rawTextEntry", "POST")
        
        self.assertEqual(json.loads(response.read().decode('utf-8')), "Missing parameter lat")
        self.assertEqual(400, response.status)

        # out of range longitudue
        body = {
            "raw_text": "I love Merck", 
            "time": "2020-26-02 15:34:00", 
            "source": "TWITTER",
            "lon": "190.3221",
            "lat": "20"
        }

        response = self.request(body, "/rawTextEntry", "POST")
        
        self.assertEqual(json.loads(response.read().decode('utf-8')), "Longitude must be between -180 and 180")
        self.assertEqual(400, response.status)


        # out of range latitude
        body = {
            "raw_text": "I love Merck", 
            "time": "2020-26-02 15:34:00", 
            "source": "TWITTER",
            "lon": "160.3221",
            "lat": "200"
        }

        response = self.request(body, "/rawTextEntry", "POST")
        
        self.assertEqual(json.loads(response.read().decode('utf-8')), "Latitude must be between -90 and 90")
        self.assertEqual(400, response.status)


    def testPostRawInvalidSource(self):
        """
        Tests valid raw text entry post with invalid source
        """
        
        body = {
            "raw_text": "I love Merck", 
            "time": "2020-26-02 15:34:00", 
            "source": "The guy on the corner",
            "lat": "56.3304",
            "lon": "130.3221",
        }

        response = self.request(body, "/rawTextEntry", "POST")
        
        self.assertEqual(json.loads(response.read().decode('utf-8')), "Invalid source")
        self.assertEqual(400, response.status)


    def testPostRawMissingText(self):
        """
        Tests valid raw text entry post without raw text
        """
        
        body = {
            "time": "2020-26-02 15:34:00", 
            "source": "TWITTER",
            "lat": "56.3304",
            "lon": "130.3221",
        }

        response = self.request(body, "/rawTextEntry", "POST")
        
        self.assertEqual(json.loads(response.read().decode('utf-8')), "Missing parameter raw_text")
        self.assertEqual(400, response.status)


    def testPostNoBody(self):
        """
        Tests a post without a body
        """
        response = self.request(None, "/rawTextEntry", "POST")
        
        self.assertEqual(json.loads(response.read().decode('utf-8')), "Missing request body")
        self.assertEqual(400, response.status)


    def testPostNoAuth(self):
        """
        Tests a post without auth
        """
        response = self.requestNoAuth(self.VALID_RAW_BODY, "/rawTextEntry", "POST")
        
        self.assertEqual(json.loads(response.read().decode('utf-8')) ['message'], "Token is missing")
        self.assertEqual(401, response.status)
        

    def testGetRawText(self):
        """
        Tests a posting and retriving raw text entries
        """

        time.sleep(.005)
        #first post
        response = self.request(self.VALID_RAW_BODY, "/rawTextEntry", "POST")
        self.assertEqual(json.loads(response.read().decode('utf-8')), "Raw entry successfully added")
        self.assertEqual(200, response.status)

        time.sleep(.005)

        #second post
        response = self.request(self.VALID_RAW_BODY_TWO, "/rawTextEntry", "POST")
        self.assertEqual(json.loads(response.read().decode('utf-8')), "Raw entry successfully added")
        self.assertEqual(200, response.status)

        time.sleep(.005)

        #third post
        response = self.request(self.VALID_RAW_BODY_THREE, "/rawTextEntry", "POST")
        self.assertEqual(json.loads(response.read().decode('utf-8')), "Raw entry successfully added")
        self.assertEqual(200, response.status)
        
        time.sleep(.005)

        #test getting all
        response = self.requestWithQueryParams("/rawTextEntries", "GET")
        body = json.loads(response.read())

        self.assertEqual(200, response.status)
        self.assertEqual(3, len(body))
        self.assertEqual(self.RETURN_BODY_TWO, body[1])

        #test min
        response = self.requestWithQueryParams("/rawTextEntries","GET", query_params=[('min', '2')])
        body = json.loads(response.read())

        self.assertEqual(200, response.status)
        self.assertEqual(2, len(body))
        self.assertEqual(self.RETURN_BODY_TWO, body[0])

        #test max
        response = self.requestWithQueryParams("/rawTextEntries", "GET", query_params=[('max', '2')])
        body = json.loads(response.read())

        self.assertEqual(200, response.status)
        self.assertEqual(2, len(body))
        self.assertEqual(self.RETURN_BODY_TWO, body[1])

        #test max and min
        response = self.requestWithQueryParams("/rawTextEntries", "GET", query_params=[('max', '2'), ('min', '2')])
        body = json.loads(response.read())

        self.assertEqual(200, response.status)
        self.assertEqual(1, len(body))
        self.assertEqual(self.RETURN_BODY_TWO, body[0])

        #test getting invalid range
        response = self.requestWithQueryParams("/rawTextEntries", "GET", query_params=[("min", "3"), ("max", "1")])
        body = json.loads(response.read().decode('utf-8'))
        
        self.assertEqual(400, response.status)
        self.assertEqual(body, "Min must be less than max")



    def testGetRawTextNoAuth(self):
        """
        Tests get method without auth
        """

        #first post
        response = self.request(self.VALID_RAW_BODY, "/rawTextEntry", "POST")
        self.assertEqual(json.loads(response.read().decode('utf-8')), "Raw entry successfully added")
        self.assertEqual(200, response.status)

        time.sleep(.005)
        response = self.getWithQueryParamsNoAuth("/rawTextEntries")
        body = json.loads(response.read())

        self.assertEqual(401, response.status)


    def testDeleteRawText(self):
        """
        Tests a posting and retriving raw text entries
        """

        #first post
        self.request(self.VALID_RAW_BODY, "/rawTextEntry", "POST")
        time.sleep(.05)

        #second post
        self.request(self.VALID_RAW_BODY_TWO, "/rawTextEntry", "POST")
        time.sleep(.05)

        #third post
        self.request(self.VALID_RAW_BODY_THREE, "/rawTextEntry", "POST")
        time.sleep(.05)


        #delete 3
        self.requestWithQueryParams( "/deleteRawTextEntry", "DELETE", query_params=[("id", "3")])
        time.sleep(.05)

        #test getting all with 3 deleted
        response = self.requestWithQueryParams("/rawTextEntries", "GET")
        body = json.loads(response.read())

        self.assertEqual(200, response.status)
        self.assertEqual(2, len(body))
        self.assertEqual(self.RETURN_BODY_TWO, body[1])


        #delete 1
        self.requestWithQueryParams( "/deleteRawTextEntry", "DELETE", query_params=[("id", "1")])
        time.sleep(.05)

        #test getting all with 1 deleted
        response = self.requestWithQueryParams("/rawTextEntries", "GET")
        body = json.loads(response.read())

        self.assertEqual(200, response.status)
        self.assertEqual(1, len(body))
        self.assertEqual(self.RETURN_BODY_TWO, body[0])


        #delete 2
        self.requestWithQueryParams( "/deleteRawTextEntry", "DELETE", query_params=[("id", "2")])
        time.sleep(.05)

        #test getting all with 1 deleted
        response = self.requestWithQueryParams("/rawTextEntries", "GET")
        body = json.loads(response.read())

        self.assertEqual(200, response.status)
        self.assertEqual(0, len(body))

"""
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
This section tests instant processing 
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""
class TestInstantProcessing(TestAPI):
    
    RAW_TEXT_BODY_THREAT = {
           
        "raw_text": "I hate Merck becuase they kill babies 😠", 
        "time": "2020-01-03 03:33:21", 
        "source": "TWITTER",
        "lat": "47.1",
        "lon": "8.5",
        "author": "Andrew Goncharov"
    }

    RAW_TEXT_BODY_OUT_OF_RANGE = {
           
        "raw_text": "I hate Merck becuase they kill babies 😠", 
        "time": "2020-01-03 03:33:21", 
        "source": "TWITTER",
        "lat": "56.3304",
        "lon": "130.3221",
        "author": "Andrew Goncharov"
    }

    RAW_TEXT_BODY_NONTHREAT = {
           
        "raw_text": "I love Merck and their COVID-19 vaccine", 
        "time": "2020-01-03 03:33:21", 
        "source": "TWITTER",
        "lat": "47.1",
        "lon": "8.5",
        "author": "Andrew Goncharov"
    }


    OUT_OF_RANGE_RESP = { "message": "Not in range of a facility" }

    THREAT_RESPONSE_VALID = {
        'id': 1,
        'raw': {
            'author': 'Andrew Goncharov', 
            'lat': 47.1, 
            'lon': 8.5, 
            'raw_text': 
            'I hate Merck becuase they kill babies 😠', 
            'source': 'TWITTER', 
            'time': '2020-01-03 03:33:21'
            }, 
        'threat_type': 'NEGATIVE', 
        'time': '2020-05-03 20:50:47'
    }


    def testValidInstantProcessingOutOfRange(self):
        """
        Tests valid instant processing out of range
        """
        response = self.request(self.RAW_TEXT_BODY_OUT_OF_RANGE, "/instantProcessing", "POST")
        self.assertEqual(200, response.status)
        self.assertEqual(self.OUT_OF_RANGE_RESP, json.loads(response.read()))
    

    def testValidInstantProcessingThreat(self):
        """
        Tests valid instant processing of a threat
        """
        response = self.request(self.RAW_TEXT_BODY_THREAT, "/instantProcessing", "POST")
        self.assertEqual(200, response.status)

        body = json.loads(response.read())
        self.assertEqual(self.THREAT_RESPONSE_VALID['id'], body['id'])
        self.assertEqual(self.THREAT_RESPONSE_VALID['raw'], body['raw'])
        self.assertEqual(self.THREAT_RESPONSE_VALID['threat_type'], body['threat_type'])


    def testValidInstantProcessingNonThreat(self):
        """
        Tests valid instant processing of a nonthreat
        """
        response = self.request(self.RAW_TEXT_BODY_NONTHREAT, "/instantProcessing", "POST")
        self.assertEqual(200, response.status)

        self.assertEqual({'message': 'Nonnegative sentiment'}, json.loads(response.read()))


    def testInstantProcessingThreatNoAuth(self):
        """
        Tests instant processing with no auth
        """
        response = self.requestNoAuth(self.RAW_TEXT_BODY_THREAT, "/instantProcessing", "POST")
        self.assertEqual(401, response.status)


"""
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
This section tests the health status endpoint
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""
class TestHealthStatus(TestAPI):
    
    def testValidHealthStauts(self):
        """
        Tests valid instant processing of a nonthreat
        """
        response = self.requestWithQueryParams("/healthstatus",  "GET")
        self.assertEqual(200, response.status)
        self.assertEqual({"db_status": "Healthy"}, json.loads(response.read()))


    def testHealthStatusNoAuth(self):
        """
        Tests healthstatus with no auth
        """
        response = self.getWithQueryParamsNoAuth( "/healthstatus")
        self.assertEqual(401, response.status)


"""
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
This section tests processed text entry posts, delete and get functions
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""
class TestProccessedEntries(TestAPI):
    
    VALID_RAW_BODY_TWO = {  
        "raw_text": "I love Merck", 
        "time": "2020-26-02 15:34:00", 
        "source": "TWITTER",
        "lat": "56.3304",
        "lon": "130.3221",
        "author": "Donald Trump"
    }

    VALID_RAW_BODY_ONE = {
        "raw_text": "I hate Merck becuase they kill babies 😠", 
        "time": "2020-01-03 03:33:21", 
        "source": "TWITTER",
        "lat": "56.3304",
        "lon": "130.3221",
        "author": "Andrew Goncharov"
    }

    VALID_RAW_BODY_THREE = {
        "raw_text": "I hate Merck becuase they give babies autism with their vaccines 😠", 
        "time": "2020-01-03 03:33:21", 
        "source": "TWITTER",
        "lat": "26.39",
        "lon": "129.19",
        "author": "Nathan Seamon"
    }

    VALID_PROCESSED_BODY_ONE_RESPONSE = {
        'id': 1,
        'raw': {
            'author': 'Andrew Goncharov', 
            'lat': 56.3304, 
            'lon': 130.3221, 
            'raw_text': 
            'I hate Merck becuase they kill babies 😠', 
            'source': 'TWITTER', 
            'time': '2020-01-03 03:33:21'
            }, 
        'threat_type': 'NEGATIVE', 
        'time': '2020-05-03 20:50:47'
    }

    VALID_PROCESSED_BODY_ONE_POST = {
        'time': '2020-05-03 20:50:47',
        'raw': 1,
        'threat_type': 'NEGATIVE'
    }

    VALID_PROCESSED_BODY_TWO_POST = {
        'time': '2020-04-03 10:03:02',
        'raw': 2,
        'threat_type': 'NEGATIVE'
    }

    VALID_PROCESSED_BODY_THREE_POST = {
        'time': '2020-02-04 11:03:02',
        'raw': 3,
        'threat_type': 'NEGATIVE'
    }


    def testPostProcessedTextEntryValid(self):
        """ 
        Test valid processed text entry post 
        """
        self.request(self.VALID_RAW_BODY_ONE, "/rawTextEntry", "POST")

        response = self.request(self.VALID_PROCESSED_BODY_ONE_POST, "/processedTextEntry", "POST")
        resp_body = json.loads(response.read().decode('utf-8'))
        
        self.assertEqual('Processed entry successfully added', resp_body)
        self.assertEqual(200, response.status)


    def testPostProcessedTextEntryBadSource(self):
        """ 
        Test invalid processed text entry post. Missing source
        """
        response = self.request(self.VALID_PROCESSED_BODY_ONE_POST, "/processedTextEntry", "POST")
        resp_body = json.loads(response.read().decode('utf-8'))
        
        self.assertEqual('Source ID does not exist', resp_body)
        self.assertEqual(400, response.status)

    
    def testGetProcessedTextEntryValid(self):
        """ 
        Test get processed text entry  
        """
        self.request(self.VALID_RAW_BODY_ONE, "/rawTextEntry", "POST")
        self.request(self.VALID_RAW_BODY_TWO, "/rawTextEntry", "POST")
        self.request(self.VALID_RAW_BODY_THREE, "/rawTextEntry", "POST")
        self.request(self.VALID_PROCESSED_BODY_ONE_POST, "/processedTextEntry", "POST")
        self.request(self.VALID_PROCESSED_BODY_TWO_POST, "/processedTextEntry", "POST")
        self.request(self.VALID_PROCESSED_BODY_THREE_POST, "/processedTextEntry", "POST")
        

        #test getting all
        response = self.requestWithQueryParams("/processedTextEntries", "GET")
        body = json.loads(response.read())
        
        self.assertEqual(200, response.status)
        self.assertEqual(3, len(body))
        self.assertEqual(self.VALID_PROCESSED_BODY_ONE_RESPONSE, body[0])

        #test max
        response = self.requestWithQueryParams("/processedTextEntries", "GET", query_params=[("max", "2")])
        body = json.loads(response.read())
        
        self.assertEqual(200, response.status)
        self.assertEqual(2, len(body))
        self.assertEqual(body[1]['id'], 2)

        #test getting min
        response = self.requestWithQueryParams("/processedTextEntries", "GET", query_params=[("min", "2")])
        body = json.loads(response.read())
        
        self.assertEqual(200, response.status)
        self.assertEqual(2, len(body))
        self.assertEqual(body[0]['id'], 2)

        #test getting min and max
        response = self.requestWithQueryParams("/processedTextEntries", "GET", query_params=[("min", "2"), ("max", "2")])
        body = json.loads(response.read())
        
        self.assertEqual(200, response.status)
        self.assertEqual(1, len(body))
        self.assertEqual(body[0]['id'], 2)

        #test getting invalid range
        response = self.requestWithQueryParams("/processedTextEntries", "GET", query_params=[("min", "3"), ("max", "1")])
        body = json.loads(response.read().decode('utf-8'))
        
        self.assertEqual(400, response.status)
        self.assertEqual(body, "Min must be less than max")



    def testDeleteProcessedTextEntry(self):
        """ 
        Test get processed text entry  
        """
        self.request(self.VALID_RAW_BODY_ONE, "/rawTextEntry", "POST")
        self.request(self.VALID_RAW_BODY_TWO, "/rawTextEntry", "POST")
        self.request(self.VALID_RAW_BODY_THREE, "/rawTextEntry", "POST")
        self.request(self.VALID_PROCESSED_BODY_ONE_POST, "/processedTextEntry", "POST")
        self.request(self.VALID_PROCESSED_BODY_TWO_POST, "/processedTextEntry", "POST")
        self.request(self.VALID_PROCESSED_BODY_THREE_POST, "/processedTextEntry", "POST")

        # delete two
        self.requestWithQueryParams( "/deleteRawTextEntry", "DELETE", query_params=[("id", "2")])
        time.sleep(.05)

        #test getting all with 2 deleted
        response = self.requestWithQueryParams("/rawTextEntries", "GET")
        body = json.loads(response.read())

        self.assertEqual(200, response.status)
        self.assertEqual(2, len(body))
        self.assertEqual(3, body[1]['id'])




if __name__ == '__main__':
    unittest.main()
