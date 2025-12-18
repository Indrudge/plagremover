🛡️ Plagiarism Remover & AI Content Detector

     

> A fully local, privacy-focused plagiarism removal and AI content detection system powered by Large Language Models.




---

✨ Overview

Plagiarism Remover & AI Content Detector is an advanced desktop application designed to help users:

Detect sentence-level plagiarism

Rewrite and paraphrase content intelligently

Identify AI-generated text

Maintain academic integrity and originality


Built using Mistral-7B, Sentence-BERT, MongoDB, and Tkinter, the system runs completely offline, ensuring full data privacy and control.


---

🎯 Why This Project?

✔ No cloud APIs
✔ No data leakage
✔ High-accuracy semantic detection
✔ Research-oriented & academic-friendly
✔ Ideal for students, researchers, and content creators


---

🚀 Features

🔍 Plagiarism Detection

Sentence-level plagiarism analysis using SBERT embeddings

Web search integration for reference retrieval

Cosine similarity–based matching

Configurable similarity thresholds

Accurate plagiarism percentage calculation

Highlighted matched content



---

✍️ Plagiarism Removal (Paraphrasing)

Context-aware rewriting using Mistral-7B

Multiple paraphrase suggestions per sentence

Ensures rewritten content stays below plagiarism thresholds

Stores rewritten content in MongoDB for audit and reuse



---

🤖 AI Content Detection

Sentence-wise AI-generated text detection

Powered by Mistral-7B

Displays:

Per-sentence AI probability

Overall AI-generated percentage


Results stored in the aigenrel MongoDB collection



---

🖥️ Desktop GUI (Tkinter)

Clean, minimal, and intuitive interface

Dedicated modes:

Plagiarism Check

Plagiarism Removal

AI Content Detection


Structured, readable output panels



---

🧱 System Architecture (High-Level)

User Input
   │
   ▼
Sentence Tokenization (NLTK)
   │
   ├──► Plagiarism Detection (SBERT + Cosine Similarity)
   │
   ├──► Paraphrasing Engine (Mistral-7B)
   │
   └──► AI Detection Module (Mistral-7B)
   │
   ▼
MongoDB (Results Storage)
   │
   ▼
Tkinter GUI (Visualization)


---

📂 Project Structure

PlagRemover/
│── plagremover/
│   │── master.py                 # Application entry point
│   │── config.py                 # Configuration & database setup
│   │── plagiarism_checker.py     # Plagiarism detection logic
│   │── plagiarism_remover.py     # Paraphrasing engine
│   │── ai_detector.py            # AI content detection module
│   │── gui.py                    # Tkinter UI components
│   │── requirements.txt          # Dependencies
│   │── README.md                 # Documentation


---

⚙️ Installation & Setup

1️⃣ Clone the Repository

git clone https://github.com/your-username/plag-remover.git
cd plag-remover

2️⃣ Create Virtual Environment (Recommended)

python -m venv vytavaran
source vytavaran/bin/activate   # macOS/Linux
vytavaran\Scripts\activate      # Windows

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Start MongoDB

mongod --dbpath "C:/data/db"

5️⃣ Run the Application

python plagremover/master.py


---

🧪 Usage Workflow

📝 Plagiarism Check

1. Paste or upload text


2. Click Check Plagiarism


3. View similarity percentage and matched sentences


4. Proceed to paraphrasing if required




---

🔄 Plagiarism Removal

1. Select plagiarized sentences


2. Click Remove Plagiarism


3. Review AI-generated rewrites


4. Copy final clean content




---

🧠 AI Content Detection

1. Paste or upload text


2. Click Check AI Content


3. Analyze sentence-wise AI probability


4. Use results for compliance or review




---

🛠️ Tech Stack

Core Technologies

Python

Tkinter

MongoDB

NLTK

PyTorch

Transformers


Models Used

Mistral-7B – Paraphrasing & AI detection

Sentence-BERT (all-MiniLM-L6-v2) – Semantic similarity detection



---

🔐 Privacy & Security

✔ 100% offline execution
✔ No third-party APIs
✔ Local AI models
✔ Local database storage
✔ No personal data collection


---

🔮 Future Roadmap

Multi-model paraphrasing comparison

Academic citation and reference validation

Fine-tuned AI-detection models

Multilingual support

PDF & DOCX input support



---

👨‍💻 Author

Indrudge Panwar
Project Lead & Developer


---

📜 License

Licensed under the MIT License.


---

⭐ Support the Project

If you find this project useful or inspiring, please consider giving it a star ⭐ on GitHub.