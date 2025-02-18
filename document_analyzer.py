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
    return latest_doc["content"] if latest_doc else None

def extract_key_topics(text):
    """Use LLM (Mistral) to extract key topics from the text."""
    prompt = f"Analyze the following text and extract the key topics:\n{text}"
    
    try:
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        key_topics = response.get("message", {}).get("content", "").split("\n")

        if not key_topics or key_topics == [""]:
            return None  # No valid topics extracted

        return key_topics
    except Exception as e:
        print(f"❌ Error during LLM processing: {e}")
        return None

def process_document():
    """Process the latest document and store key topics in MongoDB."""
    text = fetch_latest_document()
    
    if not text:
        return "⚠️ No document found in database!"

    print("🔍 Extracting key topics...")
    key_topics = extract_key_topics(text)

    if not key_topics:
        return "⚠️ No topics extracted."

    # Store in MongoDB
    web_results_collection.insert_one({"topics": key_topics})
    return f"✅ Key topics stored in MongoDB: {key_topics}"