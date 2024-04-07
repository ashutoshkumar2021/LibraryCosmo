from pymongo import MongoClient

# Replace with your MongoDB connection string
client = MongoClient("mongodb+srv://ashutoshkumarstudent1:yv9Npt2UBlVbqhn7@cluster0.rdsyeke.mongodb.net/")
db = client["students_collection"]

students_collection = db["students"]
