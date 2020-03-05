from sqlalchemy import create_engine, delete, select, and_
from sqlalchemy.orm import sessionmaker

import models

from models import RawTextEntry, ProcessedTextEntry
from settings import DB_URI

# creates connection
engine = create_engine(DB_URI)

# creates shared session maker
Session = sessionmaker(bind=engine)

# makes sure all tables exist 
models.Base.metadata.create_all(engine)


def addObject(object_to_add):
    """
    Adds object to db

    :param: object to add
    """
    session = Session()
    session.add(object_to_add)
    session.commit()
    session.close()
    

def getRaw(time, text):
    """
    Finds raw text entry

    :param: timestamp of entry
    :param: raw text in entry
    :return: RawTextEntry object
    """

    session = Session()
    entry = session.execute(select([RawTextEntry]).where(and_((RawTextEntry.timeCreated == time), 
                                                        (RawTextEntry.rawText == text)))).first()
    session.close()
    return (entry)


def getProcessed(time, raw):
    """
    Finds proccessed text entry

    :param: timestamp of entry
    :param: proccessed text in entry
    :return: ProcessedTextEntry object
    """
    session = Session()
    entry = session.execute(select([ProcessedTextEntry]).where(and_((ProcessedTextEntry.timeProcessed == time),
                                                            (ProcessedTextEntry.raw == raw)))).first()
    session.close()
    return (entry)
