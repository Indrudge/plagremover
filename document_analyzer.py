from pymongo import MongoClient
import ollama

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["plagir"]
documents_collection = db["documents"]
web_results_collection = db["web_results"]

def fetch_latest_document():
    """Fetch the latest document from MongoDB."""
    latest_doc = documents_collection.find_one(sort=[("_id", -1)])
    if latest_doc:
        return latest_doc["content"]
    return None

def extract_key_topics(text):
    """Use LLM (Mistral) to extract key topics from the text."""
    prompt = f"Analyze the following text and extract the key topics:\n{text}"
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    
    # Debugging Output
    print("🔍 Raw LLM Response:", response)

    return response['message']['content'].split("\n")

def process_document():
    """Process the latest document and store key topics in MongoDB."""
    text = fetch_latest_document()
    
    if not text:
        print("⚠️ Warning: No document found in database!")
        return
    
    print("🔍 Extracting key topics...")
    key_topics = extract_key_topics(text)

    if not key_topics:
        print("⚠️ Warning: No topics extracted.")
        return
    
    # Store in MongoDB
    web_results_collection.insert_one({"topics": key_topics})
    print("✅ Key topics stored in MongoDB:", key_topics)

if __name__ == "__main__":
    process_document()