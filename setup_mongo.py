from pymongo import MongoClient

# Connect to MongoDB (Make sure MongoDB is running)
client = MongoClient("mongodb://localhost:27017/")

# Database Name
db = client["plagir"]

# List of required collections
collections = ["documents", "web_results", "plagrem" , "websave" , "plagiarism_reports" , "aigrnrel"]

# Create collections if they don't exist
for collection in collections:
    if collection not in db.list_collection_names():
        db.create_collection(collection)
        print(f"Collection '{collection}' created.")
    else:
        print(f"Collection '{collection}' already exists.")

print("✅ MongoDB setup complete.")