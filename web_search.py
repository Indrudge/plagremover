from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import random
import time

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["plagir"]
websave_collection = db["websave"]  # Collection for scraped data
key_topics_collection = db["web_results"]  # Collection for key topics

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

def fetch_key_topics():
    """Fetch the latest key topics from MongoDB."""
    latest_entry = key_topics_collection.find_one(sort=[("_id", -1)])
    return latest_entry["topics"] if latest_entry else []

def search_web(query, num_results=5):
    """Search Google and return webpage URLs."""
    try:
        return list(search(query, num_results=num_results))
    except Exception as e:
        print(f"⚠️ Google Search Error: {e}")
        return []

def extract_text_from_url(url):
    """Extract main content from a webpage with retries."""
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            response.raise_for_status()  
            
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")

            content = "\n".join(p.get_text() for p in paragraphs if p.get_text())

            if len(content) > 100:
                return content  
            else:
                print(f"⚠️ Skipped {url} (Insufficient content)")
                return None

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Attempt {attempt+1} failed for {url}: {e}")
            time.sleep(2)  

    print(f"❌ Giving up on {url} after multiple failures")
    return None

def fetch_and_store_web_results():
    """Fetch key topics, search the web, extract content, and store results in `websave`."""
    topics = fetch_key_topics()
    
    if not topics:
        return "⚠️ No key topics found in the database."

    print("🔍 Searching the web for:", topics)
    web_data = []

    for topic in topics:
        urls = search_web(topic)
        
        for url in urls:
            content = extract_text_from_url(url)
            if content:
                web_data.append({"topic": topic, "url": url, "content": content})

    if web_data:
        websave_collection.insert_many(web_data)  
        return "✅ Web search results stored in MongoDB (websave collection)."
    
    return "⚠️ No relevant content found."