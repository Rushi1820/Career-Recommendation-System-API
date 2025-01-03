from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

import model

# Replace these with your MongoDB connection details

mongo_uri = "mongodb+srv://kssrikumar180703:Pa55w0rd@cluster0.tehiwwb.mongodb.net/Skill_Edu"
mongo_db_name = "Skill_Edu"

# Create a MongoDB client and connect to your database
client = MongoClient(mongo_uri)
database: Database = client[mongo_db_name]


collection1: Collection = database["StudentDetails"]
collection2: Collection = database["AcademicInfo"]
collection3: Collection = database["CareerPaths"]
collection4: Collection = database["Overallperformance_semwise"]
collection5: Collection = database["SoftskillsMarks"]
collection6: Collection = database["SEM2"]
collection7: Collection = database["SEM3"]
collection8: Collection = database["SEM4"]
collection9: Collection = database["SEM5"]
collection10: Collection = database["SEM6"]
collection11: Collection = database["SEM7"]
collection12: Collection = database["SEM8"]
collection13: Collection = database["Questions"]
