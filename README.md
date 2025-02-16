Plagiarism Remover & AI Content Detector
This project is a Plagiarism Removal & AI Content Detection System that utilizes LLM models to detect, rewrite, and improve text quality. It integrates Mistral-7B, Sentence Transformers, MongoDB, and Tkinter GUI to provide a seamless experience for users who want to check for plagiarism, rewrite content, and detect AI-generated text.

📌 Features
1. Plagiarism Detection

Sentence-level plagiarism detection using Sentence-BERT (SBERT) embeddings
Web search integration to find reference texts
Cosine similarity threshold-based matching
Plagiarism percentage calculation

2. Plagiarism Removal (Paraphrasing)

Context-aware rewriting using Mistral LLM
Multiple rewriting suggestions per sentence
Ensures the rewritten content stays under a plagiarism threshold
Stores rewritten texts in MongoDB for future analysis

3. AI Content Detection

Sentence-level analysis for AI-generated text
Uses Mistral-7B for checking AI-written content
Displays percentage of AI-generated content
Stores results in the MongoDB aigenrel collection

4. GUI with Tkinter

User-friendly interface to choose between different modes:

Plagiarism Check
Plagiarism Removal
AI Content Detection


Displays analysis results with a structured UI


📂 Project Structure
PlagRemover/
│── plagremover/
│   │── master.py           # Main GUI file to run the application
│   │── config.py           # Configuration settings & database connections
│   │── plagiarism_checker.py   # Plagiarism detection module
│   │── plagiarism_remover.py   # Plagiarism rewriting module
│   │── ai_detector.py      # AI content detection module
│   │── gui.py              # Tkinter GUI elements & layout
│   │── requirements.txt    # Dependencies required to run the project
│   │── README.md           # Project documentation (this file)



⚙️ Installation & Setup
🔹 1. Clone the Repository
git clone https://github.com/your-username/plag-remover.git
cd plag-remover

🔹 2. Set Up Virtual Environment (Recommended)
python -m venv vytavaran
source vytavaran/bin/activate  # For macOS/Linux
vytavaran\Scripts\activate     # For Windows

🔹 3. Install Dependencies
pip install -r requirements.txt

🔹 4. Start MongoDB
Ensure MongoDB is running on localhost:27017 before proceeding.
mongod --dbpath "C:/data/db"

🔹 5. Run the Application
python plagremover/master.py


📝 Usage Guide
🔹 Plagiarism Check

Upload or paste text into the input field.
Click "Check Plagiarism" to analyze text against stored references.
The results will show the plagiarism percentage and matched sentences.
If plagiarism is detected, you can proceed to Plagiarism Removal.

🔹 Plagiarism Removal (Paraphrasing)

Select a Plagiarism Result from the previous check.
Click "Remove Plagiarism" to generate rewritten text.
The model will paraphrase sentences with high similarity.
The final text will be saved and can be copied for use.

🔹 AI Content Detection

Paste or upload the text to check for AI generation.
Click "Check AI Content" to analyze the text.
The results will show AI-generated percentage per sentence and overall.
This helps detect AI-written or paraphrased content.


🛠️ Technologies Used
🔹 Programming Languages & Libraries

Python (Core programming language)
Tkinter (GUI framework)
PyTorch & Transformers (Mistral LLM for AI analysis & rewriting)
Sentence-BERT (SBERT for plagiarism detection)
NLTK (Tokenization & text processing)
MongoDB (Database for storing documents & results)

🔹 Machine Learning Models

Mistral-7B (Large Language Model for paraphrasing & AI detection)
Sentence-BERT (all-MiniLM-L6-v2) (For sentence embeddings in plagiarism detection)


🛡️ Security & Data Privacy

Locally hosted AI models (No external API calls, ensuring privacy)
MongoDB for local data storage (No cloud-based storage required)
No personal data collection


🔧 Future Improvements
✅ Better paraphrasing with multiple AI models
✅ Advanced citation checking for academic writing
✅ Fine-tuning the AI model for better detection
✅ Support for multiple languages

👨‍💻 Contributors

Indrudge Panwar (Project Lead & Developer)


📜 License
This project is open-source and follows the MIT License.

⭐ If you like this project, please give it a star on GitHub!
