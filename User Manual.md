Instruction Manual: Plagiarism Checker, AI Detection & Paraphraser

This manual provides a step-by-step guide on how to set up, install, and run the Plagiarism Checker, AI Detection, and Plagiarism Remover system.

1. System Requirements

Before proceeding, ensure you have the following:

Operating System: Windows, macOS, or Linux

Python Version: 3.9 or later

MongoDB: Installed and running locally (mongodb://localhost:27017/)

GPU (Optional): For faster AI processing (Recommended: NVIDIA GPU with CUDA support)



---

2. Installation Guide

Step 1: Clone the Repository

git clone https://github.com/yourusername/plagiarism-ai-detector.git
cd plagiarism-ai-detector


---

Step 2: Create a Virtual Environment

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows


---

Step 3: Install Dependencies

pip install -r requirements.txt

This installs all required Python libraries.


---

Step 4: Start MongoDB

Ensure MongoDB is running locally before starting the application.

For Windows: Open Command Prompt and run:

mongod

For Linux/macOS: Run:

sudo systemctl start mongod



---

Step 5: Configure MongoDB Connection (Optional)

If MongoDB is running on a different host, update config.py:

MONGO_URI = "mongodb://your-mongodb-server-ip:27017/"


---

3. Running the Application

Start the GUI (Main Interface)

Run the following command in the project directory:

python plagremover/master.py

This will launch the Tkinter-based GUI where you can perform plagiarism checks, AI detection, and plagiarism removal.


---

Using Individual Components (Command Line Execution)

If you want to run the features separately:

1. Plagiarism Checker

python plagremover/plagiarism_checker.py

Fetches the latest document from MongoDB

Compares it with stored web results

Generates a plagiarism report


2. AI-Generated Content Detector

python plagremover/ai_checker.py

Detects AI-generated or paraphrased content

Stores results in MongoDB under aigenrel


3. Plagiarism Remover (Paraphraser)

python plagremover/plagiarism_remover.py

Rewrites plagiarized content

Uses an LLM model (mistral) for paraphrasing



---

4. GUI Overview & Features


---

5. Additional Notes

Updating Dependencies

If new features are added, update dependencies:

pip freeze > requirements.txt

Troubleshooting

If MongoDB connection fails, check that MongoDB is running.

If CUDA errors occur, ensure you have the correct NVIDIA drivers installed.

If Tkinter GUI doesn’t launch, ensure your Python installation includes Tkinter.

