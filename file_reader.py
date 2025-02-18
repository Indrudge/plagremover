from pymongo import MongoClient
import os
from docx import Document

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["plagir"]
documents_collection = db["documents"]

def read_text_file(file_path):
    """Read text from a .txt file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"❌ Error reading text file: {e}")
        return None

def read_docx_file(file_path):
    """Read text from a .docx file."""
    try:
        doc = Document(file_path)
        return "\n".join(para.text for para in doc.paragraphs)
    except Exception as e:
        print(f"❌ Error reading DOCX file: {e}")
        return None

def process_file(file_path):
    """Determine file type, extract text, and store it in MongoDB."""
    if not os.path.exists(file_path):
        return "❌ Error: File not found!"

    # Check file type and extract content
    file_extension = os.path.splitext(file_path)[1].lower()
    extractors = {".txt": read_text_file, ".docx": read_docx_file}
    
    if file_extension not in extractors:
        return "❌ Unsupported file format. Use .txt or .docx"

    text = extractors[file_extension](file_path)
    if not text or not text.strip():
        return "⚠️ Warning: File is empty or contains no readable text."

    # Check if content already exists
    if documents_collection.find_one({"content": text}):
        return "ℹ️ Info: This document is already stored in the database."

    # Store in MongoDB
    try:
        documents_collection.insert_one({"content": text})
        return "✅ File processed successfully!"
    except Exception as e:
        return f"❌ Error inserting into MongoDB: {e}"