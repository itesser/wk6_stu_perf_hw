from base import Base
from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv


class MongoConn:
    def __init__(self):
        load_dotenv()
        self.__mongo_url = os.getenv("MONGO_URL")
        self.client = MongoClient(self.__mongo_url)
        self.db = self.client.db
        self.student_grades = self.db.student_grades
