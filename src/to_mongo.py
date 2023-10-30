from base import Base
from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv


class ToMongo(Base):
    def __init__(self):
        Base.__init__(self)
        load_dotenv()
        self.__mongo_url = os.getenv("MONGO_URL")
        self.client = MongoClient(self.__mongo_url)
        self.db = self.client.db
        self.student_grades = self.db.student_grades
        # self.data.set_index("id", inplace=True)

    def upload_data(self):
        data_size = self.data.memory_usage().sum()
        if data_size < 16000000:
            self.upload_all()
        else:
            self.upload_1x1()

    def upload_all(self):
        self.student_grades.insert_many(self.data.to_dict(orient="records"))
        print("All uploaded, in bulk")

    def upload_1x1(self):
        for i in self.student_grades.index:
            self.student_grades.insert_one(self.data.loc[i].to_dict())
        print("All uploaded, one by one")

    def drop_collection(self, coll_name: str = "student_grades"):
        self.db.drop_collection(coll_name)


if __name__ == "__main__":
    d = ToMongo()
    print("Successful Connection!")
    d.drop_collection()
    print("Old collections removed!")
    print(d.data.head())
    d.upload_data()
