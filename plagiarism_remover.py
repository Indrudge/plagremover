import torch
import nltk
import ollama
from pymongo import MongoClient
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer, util
from datetime import datetime

# Ensure NLTK resources are available
nltk.download('punkt')
nltk.download('punkt_tab')

# Load sentence transformer model for similarity check
device = "cuda" if torch.cuda.is_available() else "cpu"
embedding_model = SentenceTransformer("all-MiniLM-L6-v2").to(device)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["plagir"]
documents_collection = db["documents"]  # Original documents
rewritten_collection = db["plagrem"]  # Stores rewritten content

def get_embedding(text):
    """Generate sentence embeddings."""
    return embedding_model.encode(text, convert_to_tensor=True)

def fetch_latest_document():
    """Fetch the latest document from MongoDB."""
    latest_document = documents_collection.find_one(sort=[("_id", -1)])
    return latest_document if latest_document else None

def detect_plagiarism(original_text, reference_texts, threshold=0.8):
    """
    Detects plagiarism using sentence-level similarity.
    Returns sentences that need to be rewritten.
    """
    original_sentences = sent_tokenize(original_text)
    plagiarized_sentences = []

    for sentence in original_sentences:
        original_embedding = get_embedding(sentence)

        for ref_text in reference_texts:
            ref_sentences = sent_tokenize(ref_text)
            ref_embeddings = [get_embedding(ref) for ref in ref_sentences]

            for ref_embedding, ref_sentence in zip(ref_embeddings, ref_sentences):
                similarity = util.pytorch_cos_sim(original_embedding, ref_embedding).item()
                if similarity > threshold:
                    plagiarized_sentences.append(sentence)
                    break  # Stop checking once plagiarism is detected for this sentence

    return plagiarized_sentences

def rewrite_text_mistral(text):
    """
    Uses Mistral LLM to generate high-quality paraphrased content.
    """
    prompt = f"Paraphrase the following text while maintaining its meaning and making it sound natural:\n\n{text}"
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

def validate_rewrite(original, rewritten):
    """
    Ensures the rewritten sentence retains the original meaning using semantic similarity.
    """
    original_embedding = get_embedding(original)
    rewritten_embedding = get_embedding(rewritten)
    similarity = util.pytorch_cos_sim(original_embedding, rewritten_embedding).item()

    # Acceptable similarity range: 0.65 - 0.85 (Ensures meaning is preserved)
    return similarity >= 0.65

def process_plagiarism_removal():
    """Main function to detect and rewrite plagiarized content."""
    print("🔍 Fetching latest document...")
    document = fetch_latest_document()
    
    if not document:
        print("⚠️ No document found.")
        return
    
    original_text = document["content"]
    reference_texts = [doc["content"] for doc in db["websave"].find({}, {"content": 1, "_id": 0})]

    print("🔎 Detecting plagiarized content...")
    plagiarized_sentences = detect_plagiarism(original_text, reference_texts)

    if not plagiarized_sentences:
        print("✅ No plagiarism detected.")
        return

    rewritten_sentences = {}

    print("✍️ Rewriting plagiarized sentences...")
    for sentence in plagiarized_sentences:
        rewritten = rewrite_text_mistral(sentence)

        # Validate the rewritten text
        if validate_rewrite(sentence, rewritten):
            rewritten_sentences[sentence] = rewritten
        else:
            print(f"⚠️ Failed validation for: {sentence} → Rewriting again...")
            rewritten = rewrite_text_mistral(sentence)  # Try again
            rewritten_sentences[sentence] = rewritten if validate_rewrite(sentence, rewritten) else sentence

    # Replace plagiarized sentences with rewritten ones
    rewritten_text = original_text
    for original, rewritten in rewritten_sentences.items():
        rewritten_text = rewritten_text.replace(original, rewritten)

    print("🚀 Plagiarism removed successfully!")

    # Store rewritten content in MongoDB
    rewritten_collection.insert_one({
        "timestamp": datetime.utcnow(),
        "original_content": original_text,
        "rewritten_content": rewritten_text,
        "rewritten_sentences": rewritten_sentences
    })

    print("✅ Rewritten content stored successfully.")

    return rewritten_text

# Example Usage
if __name__ == "__main__":
    process_plagiarism_removal()