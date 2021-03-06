import os
import sys

import sqlalchemy
from sqlalchemy import BOOLEAN
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

if not os.path.exists("data/"):
    os.mkdir("data/")

try:
    engine = create_engine("sqlite:///data/matches.db")
    connection = engine.connect()
    Base = declarative_base()

    class Match(Base):
        __tablename__ = "matches"
        id = Column(Integer, primary_key=True)
        puuid = Column(String)
        match_elo = Column(Integer)
        match_id = Column(String)
        match_length = Column(String)
        match_map = Column(String)
        match_mmr_change = Column(String)
        match_rounds = Column(Integer)
        match_start = Column(String)

        def __repr__(self):
            return f"id='{self.id}', puuid='{self.puuid}', match_id='{self.match_id}'"

    class User(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True)
        puuid = Column(String)
        tracked = Column(BOOLEAN)

        def __repr__(self):
            return f"id='{self.id}', puuid='{self.puuid}', tracked='{self.tracked}'"

    Base.metadata.create_all(engine)

    @event.listens_for(Base.metadata, "after_create")
    def receive_after_create(target, connection, tables, **kw):
        """listen for the 'after_create' event"""
        logger.info("A table was created" if tables else "No table was created")
        print("A table was created" if tables else "No table was created")

    def open_session() -> sqlalchemy.orm.Session:
        """
        :return: new active session
        """
        return sessionmaker(bind=engine)()

except:
    print("An exception while connecting to the DB has occurred")
    sys.exit()
