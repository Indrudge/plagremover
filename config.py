import pymongo

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017/"  # Change if needed
DB_NAME = "plagir"

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
COLLECTIONS = {
    "documents": db["documents"],
    "analyzed_topics": db["analyzed_topics"],
    "web_references": db["web_references"],
    "plagiarism_results": db["plagiarism_results"],
    "rewritten_texts": db["rewritten_texts"]
}

# Plagiarism Threshold (Adjustable)
PLAGIARISM_THRESHOLD = 20  # Percentage to trigger rewriting

# LLM Model for Analysis & Rewriting
LLM_MODEL = "mistral"  # Ollama model to use

# Function to get a collection
def get_collection(name):
    return COLLECTIONS.get(name, None)