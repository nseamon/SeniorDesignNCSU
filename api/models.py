import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean

from auth import generateSaltAndHash

# base class for Postgres models
Base = declarative_base()

class RawTextEntry(Base):
    """"
    Raw text entry model
    """
    
    __tablename__ = 'RawTextEntries'
    id = Column(Integer, primary_key=True, unique=True)
    rawText = Column(String)
    timeCreated = Column(String)
    source = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    emojis = Column(Boolean)
    processed = Column(Boolean)
    author = Column(String)

    def __init__(self, rawText, time, source, lat, lon, author=None):
        self.rawText = rawText
        self.timeCreated = time
        self.source = source
        self.latitude = lat
        self.longitude = lon
        self.author=author
        self.emojis=False
        self.processed=False


class ProcessedTextEntry(Base):
    """"
    Proccessed text entry model
    """
    
    __tablename__ = 'ProcessedTextEntries'
    id = Column(Integer, primary_key=True, unique=True)
    raw = Column(Integer)
    timeProcessed = Column(String)
    threatType = Column(String)

    def __init__(self, raw, time, threatType):
        self.raw = raw
        self.timeProcessed = time
        self.threatType = threatType


class User(Base):
    """"
    User model
    """

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String, unique=True)
    hashed_pw = Column(String)
    salt = Column(String)
    email = Column(String)
    forgot_password_token = Column(String)
    session_token = Column(String)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        salt, hashed_pw = generateSaltAndHash(password) 
        self.salt = salt
        self.hashed_pw = hashed_pw