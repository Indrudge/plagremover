# 🛡️ Plagiarism Remover & AI Content Detector

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![LLM](https://img.shields.io/badge/LLM-Mistral--7B-purple?style=for-the-badge)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-green?style=for-the-badge&logo=mongodb)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-black?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

> **A fully local, privacy-focused plagiarism removal and AI content detection system powered by Large Language Models.**

---

## ✨ Overview

**Plagiarism Remover & AI Content Detector** is an advanced desktop application designed to help users:

- Detect **sentence-level plagiarism**
- **Rewrite and paraphrase** content intelligently
- Identify **AI-generated text**
- Maintain **academic integrity and originality**

The system integrates **Mistral-7B**, **Sentence-BERT**, **MongoDB**, and **Tkinter**, and runs entirely **offline**, ensuring complete data privacy.

---

## 🎯 Why This Project?

✔ No cloud APIs  
✔ No data leakage  
✔ High-accuracy semantic detection  
✔ Academic & research friendly  
✔ Suitable for students, researchers, and content creators  

---

## 🚀 Features

### 🔍 Plagiarism Detection
- Sentence-level plagiarism detection using **Sentence-BERT embeddings**
- Web search integration for reference retrieval
- **Cosine similarity-based matching**
- Threshold-controlled similarity checks
- Plagiarism percentage calculation
- Highlighted matched sentences

---

### ✍️ Plagiarism Removal (Paraphrasing)
- Context-aware paraphrasing using **Mistral-7B**
- Multiple rewrite suggestions per sentence
- Ensures rewritten content stays below plagiarism thresholds
- Stores rewritten results in **MongoDB**

---

### 🤖 AI Content Detection
- Sentence-level AI content analysis
- Detection powered by **Mistral-7B**
- Displays sentence-wise and overall AI probability
- Results stored in the `aigenrel` MongoDB collection

---

### 🖥️ Desktop GUI (Tkinter)
- Clean and intuitive interface
- Multiple operational modes:
  - Plagiarism Check
  - Plagiarism Removal
  - AI Content Detection
- Structured, readable result visualization

---

## 🧰 Tech Stack

### 🔧 Core Technologies

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white&style=flat-square)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange?style=flat-square)
![MongoDB](https://img.shields.io/badge/MongoDB-Local_DB-green?logo=mongodb&logoColor=white&style=flat-square)
![NLTK](https://img.shields.io/badge/NLTK-Text_Processing-yellow?style=flat-square)
![PyTorch](https://img.shields.io/badge/PyTorch-ML_Framework-red?logo=pytorch&logoColor=white&style=flat-square)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-FFD21F?logo=huggingface&logoColor=black&style=flat-square)

---

### 🧠 Machine Learning Models

![Mistral](https://img.shields.io/badge/Mistral--7B-LLM-purple?style=flat-square)
![SentenceBERT](https://img.shields.io/badge/Sentence--BERT-all--MiniLM--L6--v2-blueviolet?style=flat-square)
![CosineSimilarity](https://img.shields.io/badge/Similarity-Cosine_Matching-informational?style=flat-square)

---

### 🗄️ Storage & Privacy

![MongoDB](https://img.shields.io/badge/Database-MongoDB-green?logo=mongodb&logoColor=white&style=flat-square)
![LocalStorage](https://img.shields.io/badge/Storage-Local_Only-success?style=flat-square)
![Privacy](https://img.shields.io/badge/Privacy-No_Cloud_APIs-critical?style=flat-square)

---

## 🧱 System Architecture

### 🔲 High-Level Workflow
┌──────────────────────────┐ │        User Input        │ │ (Text / File / Paste)   │ └─────────────┬────────────┘ ▼ ┌──────────────────────────┐ │  Text Preprocessing      │ │ (Tokenization - NLTK)   │ └─────────────┬────────────┘ ▼ ┌───────────────────────────────────────────┐ │            Analysis Layer                  │ │                                           │ │  ┌──────────────┐   ┌─────────────────┐  │ │  │ Plagiarism   │   │ AI Content      │  │ │  │ Detection    │   │ Detection       │  │ │  │ (SBERT)      │   │ (Mistral-7B)    │  │ │  └──────────────┘   └─────────────────┘  │ │                                           │ │        ┌────────────────────────┐         │ │        │ Paraphrasing Engine    │         │ │        │ (Mistral-7B)           │         │ │        └────────────────────────┘         │ └─────────────┬─────────────────────────────┘ ▼ ┌──────────────────────────┐ │      MongoDB Storage     │ │ (Results & Rewrites)    │ └─────────────┬────────────┘ ▼ ┌──────────────────────────┐ │     Tkinter GUI Output   │ │ (Visualized Results)    │ └──────────────────────────┘

---

### 🔲 Module Interaction Diagram

┌──────────────────────┐ │      master.py       │ │  (Application Core)  │ └───────────┬──────────┘ ▼ ┌──────────────────────┐ │        gui.py        │ │   (Tkinter UI)       │ └─────┬────────┬───────┘ ▼        ▼ ┌──────────┐  ┌──────────────┐ │ plagiarism│  │ ai_detector  │ │ _checker  │  │ .py          │ │ .py       │  │ (Mistral)    │ └────┬──────┘  └──────┬───────┘ ▼                 ▼ ┌──────────────────────────┐ │ plagiarism_remover.py    │ │ (Paraphrasing - LLM)     │ └─────────────┬────────────┘ ▼ ┌──────────────────────────┐ │        MongoDB           │ │ (Local Persistence)     │ └──────────────────────────┘


---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/plag-remover.git
cd plag-remover
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv vytavaran
source vytavaran/bin/activate   # macOS/Linux
vytavaran\Scripts\activate      # Windows
```
### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 4️⃣ Start MongoDB
```bash
mongod --dbpath "C:/data/db"
```
### 5️⃣ Run Application
```bash
python plagremover/master.py
```
---

🔐 Security & Privacy

✔ Fully offline execution
✔ No external APIs
✔ Local AI models
✔ Local database storage
✔ No personal data collection


---

🔮 Future Roadmap

Multi-model paraphrasing comparison

Academic citation validation

Fine-tuned AI detection models

Multilingual support

PDF / DOCX input support



---

👨‍💻 Author

Indrudge Panwar
Project Lead & Developer


---

📜 License

This project is licensed under the MIT License.


---

⭐ Support the Project

If you find this project useful, consider giving it a star ⭐ on GitHub.
