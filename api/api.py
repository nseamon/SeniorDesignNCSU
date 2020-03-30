import datetime
import json
import jwt
import re

from flask import request, json, Response, make_response
from functools import wraps
from sqlalchemy import select, and_
from vaderSentiment import vaderSentiment

import db

from auth import validatePassword
from geoProximity import inRangeOfMerckFacility
from kwFilter import filterText
from models import RawTextEntry, ProcessedTextEntry, User
from settings import SOURCES, JWT_SECRET, CREATE_ACCOUNT_CODE


def buildResponse(body, status):
    """
    Returns a flask response object with type JSON
    :param: body of response
    :param: status of response
    :return: response object
    """
    return Response(response=body, status=status, mimetype='application/json')


def postRawTextEntry(instant=False):
    """
    POST new raw text entry to the database 

    :param: instant processing option that returns None on success
    :return: response object
    """

    req = request.json

    # missing body 
    if not req:
        return buildResponse(json.dumps("Missing request body"), 400)
    
    keys = req.keys()

    # error checking
    if 'raw_text' not in keys:
        return buildResponse(json.dumps("Missing parameter raw_text"), 400)
    elif 'source' not in keys:
        return buildResponse(json.dumps("Missing parameter source"), 400)
    elif 'lat' not in keys:
        return buildResponse(json.dumps("Missing parameter lat"), 400)
    elif 'lon' not in keys:
        return buildResponse(json.dumps("Missing parameter lon"), 400)

    if req['source'] not in SOURCES:
        return buildResponse(json.dumps("Invalid source"), 400)

    # TAKE THIS FLAT EARTHERS
    if (float(req['lat']) > 90) or (float(req['lat'])< -90):
         return buildResponse(json.dumps("Latitude must be between -90 and 90"), 400)

    if (float(req['lon']) > 180) or (float(req['lon']) < -180):
         return buildResponse(json.dumps("Longitude must be between -180 and 180"), 400)

    # if no time is provided, use current time
    if 'time' not in keys:
        time = datetime.datetime.now().strftime("%Y-%d-%m %H:%M:%S")
   
    # checks that time is in format YYYY-DD-MM HH:MM:SS   
    else:
        time = req['time']
        regex = re.compile("^([2])\d\d\d-(3[0-1]|[0-2][0-9])-([0-2][0-9]|3[0-1]) ([0][0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$")
        if not regex.match(time):
            return buildResponse(json.dumps("Invalid time format, must be YYYY-DD-MM HH:MM:SS"), 400)

    author = None
    if 'author' in keys:
        author = req['author']

    if db.getRaw(time, req['raw_text']):
          return buildResponse(json.dumps("Text entry with time and text already exists"), 400)

    # add raw entry to the db
    rawEntry = RawTextEntry(req['raw_text'], time, req['source'], req['lat'], req['lon'], author)
    db.addObject(rawEntry)

    # return none for instant processing mode
    if instant:
        return None

    return buildResponse(json.dumps("Raw entry successfully added"), 200)


def getRawText():
    """
    GET a list of raw text entries. Returns all raw text 
    entries when no query params are used. Select IDs can be chosen using either or both of 
    the query params ('min' and 'max')

    :return: response object
    """
    
    # start db session
    session = db.Session()

    args = request.args
    rawEntries = None

    # if both min and max are specified
    if 'min' in args.keys() and 'max' in args.keys():
        
        start = args.get('min')
        end = args.get('max')
        
        # invalid range. end db session and return error
        if start > end:
            session.close()
            return buildResponse(json.dumps("Min must be less than max"), 400)
        
        rawEntries = session.execute(select([RawTextEntry]).where(and_((RawTextEntry.id <= end), 
                                    (RawTextEntry.id >= start))))
    
    # just min specified
    elif 'min' in args.keys():
         start = args.get('min')
         rawEntries = session.execute(select([RawTextEntry]).where( RawTextEntry.id >= start))
   
    # just max specified
    elif 'max' in args.keys():
        end = args.get('max')
        rawEntries = session.execute(select([RawTextEntry]).where( RawTextEntry.id <= end))
    
    # no specified range, return all
    else:
        rawEntries = session.execute(select([RawTextEntry]))

    # close db session
    session.close()

    # make list to return
    entries = []

    for entry in rawEntries:
        
        # add json entry to list
        entries.append({
            'id': entry.id,
            'raw_text': entry.rawText,
            'time': entry.timeCreated,
            'source': entry.source,
            'lat' : entry.latitude,
            'lon': entry.longitude,
            'author': entry.author,
            'emojis': entry.emojis,
            'processed': entry.processed,
            'author': entry.author
        })

    return buildResponse(body=json.dumps(entries), status=200)


def postProcessedTextEntry():
    """
    Posts a proccessed text entry

    :return: response object 
    """

    req = request.json

    if not req:
        return buildResponse(json.dumps("Missing request body"), 400)
    
    keys = req.keys()

    #error checking
    if 'raw' not in keys:
        return buildResponse(json.dumps("Missing parameter raw"), 400)
    elif 'threat_type' not in keys:
        return buildResponse(json.dumps("Missing parameter source"), 400)
    
    # confirm raw entry id is valid
    session = db.Session()
    if not session.execute(select([RawTextEntry]).where( RawTextEntry.id == req['raw'])).first():
         session.close()
         return buildResponse(json.dumps("Source ID does not exist"), 400)
    session.close()

   
   # if no time provided, use current time
    if 'time' not in keys:
        time = datetime.datetime.now().strftime("%Y-%d-%m %H:%M:%S")
   
    # confirm time in format YYYY-DD-MM HH:MM:SS
    else:
        time = req['time']
        regex = re.compile("^([2])\d\d\d-(3[0-1]|[0-2][0-9])-([0-2][0-9]|3[0-1]) ([0][0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$")
        if not regex.match(time):
            return buildResponse(json.dumps("Invalid time format, must be YYYY-DD-MM HH:MM:SS"), 400)

    processedText = ProcessedTextEntry(req['raw'], time, req['threat_type'])
    db.addObject(processedText)

    return buildResponse(json.dumps("Processed entry successfully added"), 200)


def getProcessedText():
    """
    GET endpoint returning a json object with a list of processed text entries. Returns all raw text 
    entries when no query params are used. Select IDs can be chosen using either or both of 
    the query params ('min' and 'max')
    
    :return: response object
    """

    session = db.Session()
    args = request.args

    pEntries = None

    # if both min and max are specified
    if 'min' in args.keys() and 'max' in args.keys():
        start = args.get('min')
        end = args.get('max')

        # invalid range
        if start > end:
            session.close()
            return buildResponse(json.dumps("Min must be less than max"), 400)
            
        pEntries = session.execute(select([ProcessedTextEntry]).where(and_((ProcessedTextEntry.id <= end), (ProcessedTextEntry.id >= start))))
    
    # only min specified
    elif 'min' in args.keys():
         start = args.get('min')
         pEntries = session.execute(select([ProcessedTextEntry]).where( ProcessedTextEntry.id >= start))
    
    # only max specified 
    elif 'max' in args.keys():
        end = args.get('max')
        pEntries = session.execute(select([ProcessedTextEntry]).where( ProcessedTextEntry.id <= end))
    
    # none specified, return all
    else:
        pEntries = session.execute(select([ProcessedTextEntry]))

    session.close()
    entries= []

    # populate list to return
    for entry in pEntries:

        # get raw entry by id
        session = db.Session()
        raw = session.execute(select([RawTextEntry]).where( RawTextEntry.id == entry.raw)).first()
        session.close()
        
        if not raw:
            continue

        # add json entry to list
        entries.append({
            'id': entry.id,
            'threat_type': entry.threatType,
            'time': entry.timeProcessed,
            'raw': {
                'raw_text': raw.rawText,
                'time': raw.timeCreated,
                'source': raw.source,
                'lat' : raw.latitude,
                'lon': raw.longitude,
                'author': raw.author,
            }
        })

    return buildResponse(body=json.dumps(entries), status=200)



def deleteProcessedText():
    """
    Deletes processed text entry specified by id, and the raw entry from which the 
    processed entry was taken. 

    Returns success if sql command works (so including an atepmt to delete a missing item)

    :return: response object
    """

    args = request.args
    if 'id' not in args.keys():
        return buildResponse(body=json.dumps({"message": "no id specified"}), status=400)
   
   
    # find the raw entry id 
    session = db.Session()
    raw_id = session.execute(select([ProcessedTextEntry]).where( ProcessedTextEntry.id == args['id'])).first()['raw']

    # deletes processed entry
    session.delete(session.query(ProcessedTextEntry).filter(ProcessedTextEntry.id ==  args['id']).first())

    #deletes the raw entry for the processed entry specified
    session.delete(session.query(RawTextEntry).filter(RawTextEntry.id == raw_id).first())

    # close session
    session.commit()
    session.close()

    return buildResponse(body=json.dumps({"message": "Success"}), status=200)


def deleteRawText():
    """
    Deletes raw text entry
    Returns success if sql command works (so including an attepmt to delete a missing item)

    :return: response object
    """

    args = request.args

    #check to see if item is specified 
    if 'id' not in args.keys():
        return buildResponse(body=json.dumps({"message": "no id specified"}), status=400)
    
    # delete specified object
    session = db.Session()
    session.delete(session.query(RawTextEntry).filter(RawTextEntry.id == args['id']).first())
    session.commit()
    session.close()
    return buildResponse(body=json.dumps({"message": "Success"}), status=200)


def instantProcessing():
    """
    POST endpoint used for instant processing. User provides a raw entry, which is added to the raw db table.
    Next the raw text is analyzed with AWS comprehend. If the entry has a negative sentimate it is added to the
    processed entry table, and returned from the API. If the sentimate is not negative, null is returned with a 
    status of 200

    :return:  response object
    """

    # validates entry and adds it to db
    response = postRawTextEntry(instant=True)
    
    # this means there was an error adding the raw entry
    if response:
        
        # we return the error
        return response
    
    raw_entry = db.getRaw(request.json['time'], request.json['raw_text'])

    if not filterText(request.json['raw_text']):
        return buildResponse(body=json.dumps({"message": "Not related to Merck or its interests"}), status=200)

    analyzer = vaderSentiment.SentimentIntensityAnalyzer()
    sentiment =  analyzer.polarity_scores(request.json['raw_text'])

    neg = False
    
    if sentiment['neg'] > 0.5:
        neg = True
    elif sentiment['pos'] < 0.1 and sentiment['neg'] > 0.3:
        neg = True
   
    # if sentiment is neutral or positive we dont want to waste
    # finite db space
    if not neg:
        return buildResponse(body=json.dumps({"message": "Nonnegative sentiment"}), status=200)

    # check to see if the threat is in the range of a Merck Facility 
    if not inRangeOfMerckFacility(raw_entry[4], raw_entry[5]):
        return buildResponse(body=json.dumps({"message": "Not in range of a facility"}), status=200)
    
    time = datetime.datetime.now().strftime("%Y-%d-%m %H:%M:%S")

    # added processed entry 
    processed_entry = ProcessedTextEntry(int(raw_entry[0]), time, 'NEGATIVE')
    db.addObject(processed_entry)

    # pull entry we just added to db as sanity check
    processed_entry = db.getProcessed(time, raw_entry[0])

    # create json response body
    resp = json.dumps({
        'id': processed_entry[0],
        'threat_type': processed_entry.threatType, 
        'time': time,
        'raw': {
            'raw_text': raw_entry[1],
            'time': raw_entry[2],
            'source': raw_entry[3],
            'lat' : raw_entry[4],
            'lon': raw_entry[5],
            'author': raw_entry[8]
        }    
    })   

    return(buildResponse(body=resp, status=200))


def getSources():
    """
    Returns valid source strings

    :return: response object
    """
    return(buildResponse(body=json.dumps(SOURCES), status=200))


def createAccount():
    """
    POST endpoint to create a new user. Some of the code was taken from my personal 
    website's code in order to complete it on time for our iteration 1 deadline

    https://github.com/physics31415/CarServiceHistoryAPI/blob/master/auth.py

    :return: response object
    """

    req = request.json

    if not req:
        return buildResponse(json.dumps("Missing request body"), 400)
    
    keys = req.keys()

    #error checking
    if 'email' not in keys:
        return buildResponse(json.dumps("Missing parameter email"), 400)
    elif 'username' not in keys:
        return buildResponse(json.dumps("Missing parameter username"), 400)
    elif 'password' not in keys:
        return buildResponse(json.dumps("Missing parameter password"), 400)
    elif 'secret_code' not in keys:
        return buildResponse(json.dumps("Missing parameter secret_code"), 400)
    
    # incorrect secrete code to create an account 
    if req['secret_code'].strip() != CREATE_ACCOUNT_CODE:
        return buildResponse(json.dumps("Wrong secret_code"), 401)
    
    # check for duplicate usernames 
    session = db.Session() 
    users = session.query(User)
    for user in users:
        if user.username == req['username']:
            session.close()
            return buildResponse("Username already registered", 401)
    session.close()

    user = User(req['username'], req['email'], req['password'])
    db.addObject(user)
    
    return buildResponse(json.dumps("User was added successfully"), 200)


def login():
    """
    This POST endpoint handles user logins and returns a JWT on success
    Some parts of this are taken from my person site.

    https://github.com/physics31415/CarServiceHistoryAPI/blob/master/auth.py

    :return: response object with JWT or error
    """

    req = request.json
    keys = req.keys()

    #error checking
    if 'username' not in keys:
        return buildResponse(json.dumps("Missing parameter username"), 400)
    elif 'password' not in keys:
        return buildResponse(json.dumps("Missing parameter password"), 400)

    password = req['password']
    username = req['username']

    session = db.Session()
    users = session.query(User)

    user = None
    for usr in users:
        if usr.username == req['username']:
            user = usr

    if not user:
        session.close()
        return buildResponse(json.dumps("Username not found in system"), 404)

    salt = user.salt
    stored_pw = user.hashed_pw

    # validate's user provided password
    if validatePassword(password, salt, stored_pw):
        token = jwt.encode({'username': username, 'exp': (datetime.datetime.utcnow() + datetime.timedelta(minutes=120))}, JWT_SECRET)
        user.session_token = token.decode('utf-8')
        session.commit()
        session.close()
        return buildResponse(json.dumps({'token': token.decode('utf-8')}), 200)
    else:
        session.close()
        return buildResponse("User password incorrect", 401)


def logout():
    """
    This POST endpoint handles user logins and returns a JWT on success

    :return: response object
    """

    req = request.json
    keys = req.keys()

    #error checking
    if 'username' not in keys:
        return buildResponse(json.dumps("Missing parameter username"), 400)

    username = req['username']

    session = db.Session()
    users = session.query(User)

    # validate username
    user = None
    for usr in users:
        if usr.username == username:
            user = usr

    if not user:
        session.close()
        return buildResponse(json.dumps("Username not found in system"), 404)

    # valid username
    else:
        # remove their session token
        user.session_token = ""
        session.commit()
        session.close

    return buildResponse(json.dumps("User successfully logged out"), 200)

 
def requires_auth(f):
    """
    Wrapper function the requires a JWT bearer token for all endpoints using it.
    It returns an error back to the user if there is a problem on authentication.
    If a user's credentials checkout the main function call continues normally. 
    Some of the code borrowed from my personal website

    https://github.com/physics31415/CarServiceHistoryAPI/blob/master/auth.py

    :return: response object with error or a function call
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        jwt_token = request.headers.get('authorization', None)

        # this means JWT is invalid, return the correct error response
        if not jwt_token:
            return buildResponse(body=json.dumps({'message': 'Token is missing'}), status=401)

        # removes 'bearer:' from token
        jwt_token = jwt_token[7:]

        # if we have a token
        if jwt_token:
            try:
                token = jwt.decode(jwt_token, JWT_SECRET)
                username = token ['username']

                # confirm session token
                session = db.Session()
                users = session.query(User)
                user = None
                for usr in users:
                    if usr.username == username:
                        user = usr
                session.close()

                #means it is valid
                if jwt_token == user.session_token:
                    return f(*args, **kwargs)

                # session token doesnt match user provided token
                else:
                    return buildResponse(body=json.dumps({'message': 'Token is not in use'}), status=400)
                session = db.Session()
   
            # mangaled/invalid jwt
            except (jwt.DecodeError):
                return buildResponse(body=json.dumps({'message': 'Token is invalid'}), status=400)
            
            # jwt timed out
            except (jwt.ExpiredSignatureError):
                return buildResponse(body=json.dumps({'message': 'Token is expired'}), status=401)

    return wrapper

