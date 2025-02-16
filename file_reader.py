from pymongo import MongoClient
import os
from docx import Document

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["plagir"]
documents_collection = db["documents"]

def read_text_file(file_path):
    """Read text from a .txt file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def read_docx_file(file_path):
    """Read text from a .docx file."""
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def process_file(file_path):
    """Determine file type and extract text."""
    if not os.path.exists(file_path):
        print("❌ Error: File not found!")
        return
    
    print(f"🔍 Processing file: {file_path}")

    # Check file type
    if file_path.endswith(".txt"):
        text = read_text_file(file_path)
    elif file_path.endswith(".docx"):
        text = read_docx_file(file_path)
    else:
        print("❌ Unsupported file format. Use .txt or .docx")
        return

    if not text.strip():
        print("⚠️ Warning: File is empty or contains no readable text.")
        return
    
    # Store in MongoDB
    documents_collection.insert_one({"content": text})
    print("✅ File processed successfully!")
    print(f"📄 Stored in MongoDB: {text[:100]}...")

if __name__ == "__main__":
    file_path = input("Enter file path: ").strip()
    process_file(file_path)