import torch
import nltk
import ollama
from pymongo import MongoClient
from nltk.tokenize import sent_tokenize
from datetime import datetime

# Ensure NLTK resources are available
nltk.download('punkt')
nltk.download('punkt_tab')

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["plagir"]
aigenrel_collection = db["aigenrel"]  # AI-generated content results storage

def analyze_text_for_ai(text):
    """Analyzes text for AI-generated content at the sentence level using Mistral LLM."""
    sentences = sent_tokenize(text)
    ai_scores = []
    analysis_results = []

    for sentence in sentences:
        # Use Mistral LLM for analysis
        prompt = f"Analyze this sentence and determine if it is AI-generated. Respond only with a number from 0 to 1 (0 = fully human-written, 1 = fully AI-generated):\n\n{sentence}"
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        
        try:
            ai_score = float(response["message"]["content"].strip())  # Extract numeric response
            ai_scores.append(ai_score)
        except ValueError:
            ai_score = 0  # Default to human-written if parsing fails

        analysis_results.append({
            "sentence": sentence,
            "ai_score": round(ai_score * 100, 2)  # Convert to percentage
        })

    # Final AI percentage (average of sentence scores)
    ai_percentage = round(sum(ai_scores) / len(ai_scores) * 100, 2)

    return ai_percentage, analysis_results

def store_ai_analysis(text, ai_percentage, analysis_results):
    """Stores AI-generated content analysis results in MongoDB."""
    result_data = {
        "timestamp": datetime.utcnow(),
        "ai_percentage": ai_percentage,
        "analysis_results": analysis_results
    }
    aigenrel_collection.insert_one(result_data)
    print("✅ AI content analysis stored successfully.")

def process_ai_detection():
    """Fetches the latest document and checks for AI-generated content."""
    # Fetch the latest document from MongoDB
    latest_document = db["documents"].find_one(sort=[("_id", -1)])
    if not latest_document:
        print("⚠️ No document found for AI detection.")
        return

    text = latest_document["content"]
    print("🔍 Analyzing document for AI-generated content...")

    # Perform AI content detection
    ai_percentage, analysis_results = analyze_text_for_ai(text)

    print(f"🚨 AI-Generated Content: {ai_percentage:.2f}%")
    store_ai_analysis(text, ai_percentage, analysis_results)

    return ai_percentage, analysis_results

# Example Usage
if __name__ == "__main__":
    process_ai_detection()