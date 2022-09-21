import pymongo
from pymongo import MongoClient

class Database:
    connection = pymongo.MongoClient()

    @staticmethod
    def connect():
        try:
            conn = MongoClient('mongodb://localhost:27017/')
            print('Connected successfully!!!')
            mydb = conn['QuantumAPI']
            mycol = mydb['algorithm']
            return mycol
        except:
            print('Could not connect to MongoDB')
