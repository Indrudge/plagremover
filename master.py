import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import threading
import file_reader
import document_analyzer
import web_search
import plagiarism_checker
import ai_checker
import plagiarism_remover
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["plagir"]

# GUI Setup
root = tk.Tk()
root.title("Plagiarism Remover")
root.geometry("800x600")

# Global flag for canceling process
cancel_process = False

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("Word Documents", "*.docx")])
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

def log_message(message):
    text_output.insert(tk.END, message + "\n")
    text_output.yview(tk.END)

def process_pipeline():
    global cancel_process
    cancel_process = False
    progress_bar.start()

    def run_pipeline():
        global cancel_process
        file_path = entry_file_path.get().strip()
        
        if not file_path:
            messagebox.showerror("Error", "Please select a file first!")
            progress_bar.stop()
            return
        
        log_message("\n📌 Step 1: Processing the file...")
        file_result = file_reader.process_file(file_path)
        log_message(file_result)
        
        if cancel_process:
            log_message("❌ Process canceled.")
            progress_bar.stop()
            return
        
        if "✅" in file_result:
            log_message("\n📌 Step 2: Analyzing document...")
            analysis_result = document_analyzer.process_document()
            log_message(analysis_result)
            
            if cancel_process:
                log_message("❌ Process canceled.")
                progress_bar.stop()
                return
            
            if "✅" in analysis_result:
                log_message("\n📌 Step 3: Performing web search...")
                web_result = web_search.fetch_and_store_web_results()
                log_message(web_result)
                
                if cancel_process:
                    log_message("❌ Process canceled.")
                    progress_bar.stop()
                    return
                
                if "✅" in web_result:
                    log_message("\n📌 Step 4: Checking for plagiarism...")
                    plagiarism_result = plagiarism_checker.process_plagiarism_check()
                    log_message(plagiarism_result)
                    
                    log_message("\n📌 Step 5: Checking for AI-generated content...")
                    ai_result = ai_checker.process_ai_detection()
                    log_message(ai_result)
                    
                    if cancel_process:
                        log_message("❌ Process canceled.")
                        progress_bar.stop()
                        return
                    
                    user_input = messagebox.askyesno("Plagiarism Detected", 
                        f"Plagiarism: {plagiarism_result}% | AI Content: {ai_result}%\nDo you want to remove plagiarism?")
                    
                    if user_input:
                        log_message("\n📌 Step 6: Removing plagiarism...")
                        plagiarism_removed = plagiarism_remover.process_plagiarism_removal()
                        log_message(plagiarism_removed)
                    else:
                        log_message("📌 Plagiarism removal skipped.")
        
        progress_bar.stop()
        log_message("✔️ Process completed successfully!")
    
    threading.Thread(target=run_pipeline, daemon=True).start()

def cancel_pipeline():
    global cancel_process
    cancel_process = True
    log_message("⚠️ Canceling process...")

def show_rewritten_content():
    log_message("\n📌 Fetching rewritten content...")
    result = db["plagrem"].find_one()
    
    if result and "rewritten_content" in result:
        text_output.insert(tk.END, "\n📜 Rewritten Content:\n" + result["rewritten_content"] + "\n")
    else:
        text_output.insert(tk.END, "\n❌ No rewritten content found!\n")

def reset_database():
    collections = ["algenrel", "documents", "plagiarism_reports", "plagrem", "web_results"]
    for collection in collections:
        db[collection].delete_many({})
    
    messagebox.showinfo("Reset", "Database cleared successfully!")
    log_message("\n🗑️ All collections cleared. Ready for a new check.")

frame = tk.Frame(root)
frame.pack(pady=20)

tk.Label(frame, text="Select File:").grid(row=0, column=0, padx=10)
entry_file_path = tk.Entry(frame, width=50)
entry_file_path.grid(row=0, column=1, padx=10)
tk.Button(frame, text="Browse", command=select_file).grid(row=0, column=2)

tk.Button(root, text="Start Process", command=process_pipeline, bg="lightgreen").pack(pady=5)
tk.Button(root, text="Cancel Process", command=cancel_pipeline, bg="orange").pack(pady=5)
tk.Button(root, text="Show Rewritten Content", command=show_rewritten_content, bg="lightblue").pack(pady=5)
tk.Button(root, text="Reset Database", command=reset_database, bg="red", fg="white").pack(pady=5)

progress_bar = ttk.Progressbar(root, mode='indeterminate', length=300)
progress_bar.pack(pady=10)

text_output = scrolledtext.ScrolledText(root, height=20, width=90)
text_output.pack(pady=10)

root.mainloop()
