import nltk
import ollama
from pymongo import MongoClient
from nltk.tokenize import sent_tokenize
from datetime import datetime

# Ensure NLTK resources are available

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["plagir"]
aigenrel_collection = db["aigenrel"]  

def analyze_text_for_ai(text):
    """Analyzes text for AI-generated content using Mistral LLM."""
    if not text.strip():
        return 0, []

    sentences = sent_tokenize(text)
    ai_scores = []
    analysis_results = []

    for sentence in sentences:
        # Use Mistral LLM for AI detection
        prompt = (
            f"Analyze this sentence and determine if it is AI-generated. "
            f"Respond only with a number from 0 to 1 (0 = fully human-written, 1 = fully AI-generated):\n\n{sentence}"
        )
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])

        try:
            ai_score = float(response["message"]["content"].strip())
            ai_scores.append(ai_score)
        except ValueError:
            ai_score = 0  

        analysis_results.append({
            "sentence": sentence,
            "ai_score": round(ai_score * 100, 2)
        })

    # Calculate the overall AI percentage
    ai_percentage = round(sum(ai_scores) / len(ai_scores) * 100, 2) if ai_scores else 0
    return ai_percentage, analysis_results

def store_ai_analysis(ai_percentage, analysis_results):
    """Stores AI-generated content analysis results in MongoDB."""
    result_data = {
        "timestamp": datetime.utcnow(),
        "ai_percentage": ai_percentage,
        "analysis_results": analysis_results,
    }
    aigenrel_collection.insert_one(result_data)
    return f"✅ AI content analysis stored successfully. AI-generated content detected: {ai_percentage:.2f}%."

def fetch_latest_document():
    """Fetches the latest document from MongoDB."""
    latest_document = db["documents"].find_one(sort=[("_id", -1)])
    return latest_document["content"] if latest_document else None

def process_ai_detection():
    """Runs AI detection on the latest document and saves results."""
    text = fetch_latest_document()
    if not text:
        return "⚠️ No document found for AI detection."

    ai_percentage, analysis_results = analyze_text_for_ai(text)
    return store_ai_analysis(ai_percentage, analysis_results)

# Allow this module to be used independently for testing
if __name__ == "__main__":
    result = process_ai_detection()
    print(result)