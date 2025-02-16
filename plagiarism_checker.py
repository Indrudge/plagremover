import torch
import nltk
import re
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer, util
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime
import numpy as np

# Ensure NLTK resources are available
nltk.download('punkt')
nltk.download('punkt_tab')

# Load Sentence Transformer model (Use GPU if available)
device = "cuda" if torch.cuda.is_available() else "cpu"
embedding_model = SentenceTransformer("all-MiniLM-L6-v2").to(device)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["plagir"]
documents_collection = db["documents"]  # Original document storage
websave_collection = db["websave"]  # Web scraped content
plagiarism_reports_collection = db["plagiarism_reports"]  # Plagiarism results

def preprocess_text(text):
    """Lowercase, remove citations, and clean text."""
    text = text.lower()
    text = re.sub(r'\d+', '', text)  # Remove citation numbers [1], [2], etc.
    return text

def get_embedding(text):
    """Generate sentence embeddings."""
    return embedding_model.encode(text, convert_to_tensor=True)

def fetch_document_text():
    """Fetch the latest document from MongoDB (original text)."""
    latest_document = documents_collection.find_one(sort=[("_id", -1)])
    return preprocess_text(latest_document["content"]) if latest_document else None

def fetch_web_results():
    """Fetch all web search results from MongoDB (only 'content' field)."""
    results = websave_collection.find({}, {"content": 1, "_id": 0})
    return [preprocess_text(res["content"]) for res in results if "content" in res]

def ngram_jaccard_similarity(sent1, sent2, n=3):
    """Compute Jaccard Similarity for N-grams (for exact phrase matching)."""
    set1 = set([sent1[i:i+n] for i in range(len(sent1) - n + 1)])
    set2 = set([sent2[i:i+n] for i in range(len(sent2) - n + 1)])
    return len(set1 & set2) / len(set1 | set2) if set1 | set2 else 0

def tfidf_cosine_similarity(sent1, sent2):
    """Compute Cosine Similarity using TF-IDF (for paraphrased sentences)."""
    vectorizer = TfidfVectorizer().fit([sent1, sent2])
    vectors = vectorizer.transform([sent1, sent2]).toarray()
    cosine_sim = np.dot(vectors[0], vectors[1]) / (np.linalg.norm(vectors[0]) * np.linalg.norm(vectors[1]))
    return cosine_sim

def check_plagiarism(original_text, reference_texts, exact_thresh=0.85, paraphrase_thresh=0.7, semantic_thresh=0.75):
    """
    Compares original document with web results using multiple similarity methods.

    :param original_text: The uploaded document's content
    :param reference_texts: List of texts from web search results
    :param exact_thresh: Threshold for exact matches (N-gram Jaccard)
    :param paraphrase_thresh: Threshold for paraphrasing (TF-IDF Cosine)
    :param semantic_thresh: Threshold for deep meaning (SBERT Embeddings)
    :return: Final plagiarism percentage and detected matches
    """
    original_sentences = sent_tokenize(original_text)
    plagiarized_count = 0
    matches = []

    for sentence in original_sentences:
        original_embedding = get_embedding(sentence)
        
        for ref_text in reference_texts:
            ref_sentences = sent_tokenize(ref_text)
            
            for ref_sentence in ref_sentences:
                # Check exact match (N-gram Jaccard)
                if ngram_jaccard_similarity(sentence, ref_sentence) > exact_thresh:
                    plagiarized_count += 1
                    matches.append({"original": sentence, "match": ref_sentence, "method": "Exact Match"})
                    continue  # Move to next sentence if already matched
                
                # Check paraphrase match (TF-IDF Cosine)
                if tfidf_cosine_similarity(sentence, ref_sentence) > paraphrase_thresh:
                    plagiarized_count += 1
                    matches.append({"original": sentence, "match": ref_sentence, "method": "Paraphrase Detection"})
                    continue

                # Check deep semantic similarity (SBERT Embeddings)
                ref_embedding = get_embedding(ref_sentence)
                similarity = util.pytorch_cos_sim(original_embedding, ref_embedding).item()
                
                if similarity > semantic_thresh:
                    plagiarized_count += 1
                    matches.append({"original": sentence, "match": ref_sentence, "method": "Deep Semantic Similarity"})
                    continue

    # Normalize Plagiarism Percentage (Ensuring max 100%)
    total_sentences = len(original_sentences)
    plagiarism_percentage = min((plagiarized_count / total_sentences) * 100, 100)

    return plagiarism_percentage, matches

def store_plagiarism_report(plagiarism_percentage, matches):
    """Store plagiarism report in MongoDB."""
    report = {
        "timestamp": datetime.utcnow(),
        "plagiarism_percentage": plagiarism_percentage,
        "matches": matches,
    }
    plagiarism_reports_collection.insert_one(report)
    print("✅ Plagiarism report stored successfully.")

def process_plagiarism_check():
    """Main function to check plagiarism and store results."""
    print("🔍 Fetching original document...")
    original_text = fetch_document_text()
    
    print("🔍 Fetching web search results...")
    reference_texts = fetch_web_results()

    if not original_text:
        print("⚠️ No document found for plagiarism check.")
        return

    if not reference_texts:
        print("⚠️ No web search results found.")
        return

    print("🔎 Comparing document with web data...")
    plagiarism_percentage, matches = check_plagiarism(original_text, reference_texts)

    print(f"🚨 Plagiarism detected: {plagiarism_percentage:.2f}%")
    store_plagiarism_report(plagiarism_percentage, matches)

    return plagiarism_percentage, matches

# Example Usage
if __name__ == "__main__":
    process_plagiarism_check()