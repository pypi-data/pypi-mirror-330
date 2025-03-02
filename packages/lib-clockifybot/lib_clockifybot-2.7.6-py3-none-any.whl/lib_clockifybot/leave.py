import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.orm import sessionmaker, declarative_base

from .database import create_database_if_not_exists
from .log import add_log

load_dotenv(os.getenv("CLOCKIFY_ENV"))

LEAVE_URL = os.getenv("DATABASE_URL_LEAVE")
engine = create_engine(LEAVE_URL)
BaseLeave = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Leave(BaseLeave):
    __tablename__ = "leave"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String)
    username = Column(String)
    coolname = Column(String)
    clockify_id = Column(String)
    workday = Column(String)
    hours = Column(String)
    status = Column(String)
    mode = Column(String)
    request_id = Column(Numeric)

    def __repr__(self):
        return f"User('{self.username}') - RoutineLeave('{self.workday}'))"


def init_leave_db(bot):
    create_database_if_not_exists(LEAVE_URL, bot)
    try:
        BaseLeave.metadata.create_all(engine)
    except Exception as e:
        add_log(f"Error creating Leave table: {e}")


def leave_type_text(mode):
    match mode:
        case "partremote":
            t = "Part-time Remote"
        case "partvac":
            t = "Part-time Absence"
        case "fullremote":
            t = "Full-time Remote"
        case "fullvac":
            t = "Full-time Absence"
        case _:
            t = "UNKNOWN"
    return t
