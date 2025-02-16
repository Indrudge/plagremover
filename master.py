import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
from config import process_plagiarism_check, process_plagiarism_removal, process_ai_detection
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["plagir"]

### GUI APPLICATION ###
class PlagiarismCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📌 Plagiarism & AI Content Detection")
        self.root.geometry("800x600")
        self.root.configure(bg="#f4f4f4")

        # 📌 TEXT INPUT SECTION
        self.text_input = scrolledtext.ScrolledText(root, width=90, height=10, wrap=tk.WORD)
        self.text_input.pack(pady=10)

        self.upload_button = tk.Button(root, text="📂 Upload File", command=self.upload_file, bg="#008CBA", fg="white", font=("Arial", 10, "bold"))
        self.upload_button.pack(pady=5)

        # 🔧 FEATURE BUTTONS
        self.buttons_frame = tk.Frame(root, bg="#f4f4f4")
        self.buttons_frame.pack(pady=10)

        self.plag_check_btn = tk.Button(self.buttons_frame, text="🔍 Check Plagiarism", command=self.check_plagiarism, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=20)
        self.plag_check_btn.grid(row=0, column=0, padx=5, pady=5)

        self.plag_remove_btn = tk.Button(self.buttons_frame, text="♻ Remove Plagiarism", command=self.remove_plagiarism, bg="#FF9800", fg="white", font=("Arial", 10, "bold"), width=20)
        self.plag_remove_btn.grid(row=0, column=1, padx=5, pady=5)

        self.ai_detect_btn = tk.Button(self.buttons_frame, text="🤖 AI Content Detection", command=self.detect_ai_content, bg="#E91E63", fg="white", font=("Arial", 10, "bold"), width=20)
        self.ai_detect_btn.grid(row=0, column=2, padx=5, pady=5)

        # 📊 RESULTS DISPLAY
        self.results_label = tk.Label(root, text="📊 Results:", font=("Arial", 12, "bold"), bg="#f4f4f4")
        self.results_label.pack(pady=5)

        self.results_box = scrolledtext.ScrolledText(root, width=90, height=10, wrap=tk.WORD)
        self.results_box.pack(pady=5)

        # 📂 VIEW PREVIOUS REPORTS
        self.history_label = tk.Label(root, text="📂 View Previous Reports:", font=("Arial", 12, "bold"), bg="#f4f4f4")
        self.history_label.pack(pady=5)

        self.report_dropdown = tk.StringVar(root)
        self.report_dropdown_menu = tk.OptionMenu(root, self.report_dropdown, *self.get_previous_reports())
        self.report_dropdown_menu.pack(pady=5)

        self.view_report_btn = tk.Button(root, text="🔎 View Report", command=self.view_report, bg="#3F51B5", fg="white", font=("Arial", 10, "bold"))
        self.view_report_btn.pack(pady=5)

    ### 📂 FILE UPLOAD FUNCTION ###
    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert(tk.END, content)

    ### 🔍 PLAGIARISM CHECK FUNCTION ###
    def check_plagiarism(self):
        input_text = self.text_input.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showerror("Error", "Please enter text or upload a file.")
            return

        self.results_box.delete("1.0", tk.END)
        self.results_box.insert(tk.END, "🔍 Checking for plagiarism...\n")
        self.root.update()

        plagiarism_percentage, matches = process_plagiarism_check(input_text)
        self.results_box.insert(tk.END, f"\n🚨 Plagiarism Detected: {plagiarism_percentage:.2f}%\n")
        for match in matches:
            self.results_box.insert(tk.END, f"\n🔗 Matched: {match['match']}\n")

    ### ♻ REMOVE PLAGIARISM FUNCTION ###
    def remove_plagiarism(self):
        input_text = self.text_input.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showerror("Error", "Please enter text or upload a file.")
            return

        self.results_box.delete("1.0", tk.END)
        self.results_box.insert(tk.END, "♻ Removing plagiarism...\n")
        self.root.update()

        rewritten_text = process_plagiarism_removal(input_text)
        self.results_box.insert(tk.END, "\n✅ Plagiarism Removed! Rewritten Text:\n")
        self.results_box.insert(tk.END, f"\n{rewritten_text}\n")

    ### 🤖 AI CONTENT DETECTION FUNCTION ###
    def detect_ai_content(self):
        input_text = self.text_input.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showerror("Error", "Please enter text or upload a file.")
            return

        self.results_box.delete("1.0", tk.END)
        self.results_box.insert(tk.END, "🤖 Detecting AI-generated content...\n")
        self.root.update()

        ai_percentage, analysis_results = process_ai_detection(input_text)
        self.results_box.insert(tk.END, f"\n🚨 AI-Generated Content: {ai_percentage:.2f}%\n")
        for result in analysis_results:
            self.results_box.insert(tk.END, f"\n📌 {result['sentence']} - {result['ai_score']}% AI-generated\n")

    ### 📂 FETCH PREVIOUS REPORTS ###
    def get_previous_reports(self):
        reports = db["plagiarism_reports"].find({}, {"timestamp": 1})
        return [str(report["timestamp"]) for report in reports]

    ### 🔎 VIEW PREVIOUS REPORT ###
    def view_report(self):
        selected_report = self.report_dropdown.get()
        if not selected_report:
            messagebox.showerror("Error", "Please select a report.")
            return

        report_data = db["plagiarism_reports"].find_one({"timestamp": selected_report})
        if report_data:
            self.results_box.delete("1.0", tk.END)
            self.results_box.insert(tk.END, f"📊 Report from {selected_report}:\n")
            self.results_box.insert(tk.END, f"\n🚨 Plagiarism Detected: {report_data['plagiarism_percentage']}%\n")
            for match in report_data["matches"]:
                self.results_box.insert(tk.END, f"\n🔗 Matched: {match['match']}\n")
        else:
            messagebox.showerror("Error", "Report not found.")

### 🏁 RUN APPLICATION ###
if __name__ == "__main__":
    root = tk.Tk()
    app = PlagiarismCheckerApp(root)
    root.mainloop()