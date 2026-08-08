# ==============================
# Resume Screening System
# main.py (Part 1)
# ==============================

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import os

from parser import parse_file
from matcher import calculate_score
from report import generate_report, save_report


class ResumeScreeningSystem:

    def __init__(self, root):

        self.root = root

        self.root.title("Resume Screening & Job Description Matching System")

        self.root.geometry("1200x750")

        self.root.configure(bg="#F4F7FC")

        self.root.resizable(False, False)

        # ---------------- Variables ----------------

        self.jd_path = ""

        self.resume_paths = []

        self.results = []

        # ---------------- Header ----------------

        header = Label(
            self.root,
            text="Resume Screening & Job Description Matching System",
            font=("Arial", 22, "bold"),
            bg="#1E3A8A",
            fg="white",
            pady=15
        )

        header.pack(fill=X)

        # ---------------- Left Panel ----------------

        left = Frame(
            self.root,
            bg="#F4F7FC",
            width=350
        )

        left.pack(side=LEFT, fill=Y, padx=15, pady=15)

        # ---------------- JD Frame ----------------

        jd_frame = LabelFrame(
            left,
            text="Job Description",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10,
            bg="#F4F7FC"
        )

        jd_frame.pack(fill=X, pady=10)

        self.jd_label = Label(
            jd_frame,
            text="No Job Description Selected",
            bg="white",
            relief=SUNKEN,
            anchor="w",
            width=40
        )

        self.jd_label.pack(fill=X, pady=5)

        self.jd_button = Button(
            jd_frame,
            text="Upload Job Description",
            bg="#2563EB",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            command=self.upload_jd
        )

        self.jd_button.pack(fill=X)

        # ---------------- Resume Frame ----------------

        resume_frame = LabelFrame(
            left,
            text="Resume Upload",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10,
            bg="#F4F7FC"
        )

        resume_frame.pack(fill=X , pady=10)

        scrollbar = Scrollbar(resume_frame)

        scrollbar.pack(side=RIGHT, fill=Y)

        self.resume_list = Listbox(
            resume_frame,
            height=10,
            yscrollcommand=scrollbar.set
        )

        self.resume_list.pack(fill=BOTH, expand=True)

        scrollbar.config(command=self.resume_list.yview)

        self.resume_button = Button(
            resume_frame,
            text="Upload Resume(s)",
            bg="#10B981",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            command=self.upload_resumes
        )

        self.resume_button.pack(fill=X, pady=5)

        # ---------------- Analyze Button ----------------

        self.analyze_btn = Button(
            left,
            text="ANALYZE RESUMES",
            bg="#F59E0B",
            fg="white",
            font=("Arial", 12, "bold"),
            height=2,
            cursor="hand2",
            command=self.analyze
        )

        self.analyze_btn.pack(fill=X, pady=15)

        # ---------------- Right Panel ----------------

        right = Frame(
            self.root,
            bg="#F4F7FC"
        )

        right.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=15)

        # ---------------- Ranking Table ----------------

        table_frame = LabelFrame(
            right,
            text="Candidate Ranking",
            font=("Arial", 11, "bold"),
            bg="#F4F7FC",
            padx=10,
            pady=10
        )

        table_frame.pack(fill=BOTH, expand=True)

        columns = (
            "Rank",
            "Candidate",
            "Score",
            "Recommendation"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10
        )

        self.table.heading("Rank", text="Rank")

        self.table.heading("Candidate", text="Candidate")

        self.table.heading("Score", text="Score")

        self.table.heading("Recommendation", text="Recommendation")

        self.table.column("Rank", width=60, anchor=CENTER)

        self.table.column("Candidate", width=180)

        self.table.column("Score", width=80, anchor=CENTER)

        self.table.column("Recommendation", width=220)

        self.table.pack(fill=BOTH, expand=True)

        self.table.bind(
            "<<TreeviewSelect>>",
            self.show_details
        )

        # ---------------- Details ----------------

        detail = LabelFrame(
            right,
            text="Candidate Details",
            font=("Arial", 11, "bold"),
            bg="#F4F7FC",
            padx=10,
            pady=10
        )

        detail.pack(fill=BOTH, pady=10)

        self.detail_text = Text(
            detail,
            height=12,
            font=("Consolas", 10)
        )

        self.detail_text.pack(fill=BOTH, expand=True)

        # ---------------- Status ----------------

        self.status = Label(
            self.root,
            text="Ready",
            bg="#1E3A8A",
            fg="white",
            anchor=W
        )

        self.status.pack(fill=X, side=BOTTOM)
    # ---------------- Upload JD ----------------

    def upload_jd(self):

        path = filedialog.askopenfilename(
            title="Select Job Description",
            filetypes=[("Text Files", "*.txt")]
        )

        if path:

            self.jd_path = path

            self.jd_label.config(text=os.path.basename(path))

            self.status.config(text="Job Description Selected")


    # ---------------- Upload Resumes ----------------

    def upload_resumes(self):

        paths = filedialog.askopenfilenames(
            title="Select Resume Files",
            filetypes=[("Text Files", "*.txt")]
        )

        if paths:

            self.resume_paths = list(paths)

            self.resume_list.delete(0, END)

            for file in self.resume_paths:

                self.resume_list.insert(
                    END,
                    os.path.basename(file)
                )

            self.status.config(
                text=str(len(self.resume_paths)) + " Resume(s) Selected"
            )


    # ---------------- Analyze ----------------

    def analyze(self):

        if self.jd_path == "":

            messagebox.showerror(
                "Error",
                "Please upload a Job Description."
            )

            return

        if len(self.resume_paths) == 0:

            messagebox.showerror(
                "Error",
                "Please upload at least one Resume."
            )

            return

        self.results = []

        jd = parse_file(self.jd_path)

        for resume_file in self.resume_paths:

            resume = parse_file(resume_file)

            result = calculate_score(
                jd,
                resume
            )

            self.results.append(result)

        # Generate Report

        report = generate_report(self.results)

        save_report(report)

        # Display Ranking

        for row in self.table.get_children():

            self.table.delete(row)

        self.results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        rank = 1

        for result in self.results:

            self.table.insert(
                "",
                END,
                values=(
                    rank,
                    result["candidate"],
                    str(result["score"]) + "%",
                    result["recommendation"]
                )
            )

            rank += 1

        self.detail_text.delete(
            1.0,
            END
        )

        self.detail_text.insert(
            END,
            "Analysis Completed Successfully.\n\n"
        )

        self.detail_text.insert(
            END,
            "Select a candidate from the table "
            "to view details."
        )

        self.status.config(
            text="Analysis Completed | Report Saved"
        )

        messagebox.showinfo(
            "Success",
            "Resume Analysis Completed.\n\n"
            "Report saved to output/report.txt"
        )


    # ---------------- Show Candidate Details ----------------

    def show_details(self, event):

        selected = self.table.focus()

        if selected == "":

            return

        values = self.table.item(
            selected,
            "values"
        )

        candidate = values[1]

        self.detail_text.delete(
            1.0,
            END
        )

        for result in self.results:

            if result["candidate"] == candidate:

                self.detail_text.insert(
                    END,
                    "Candidate Name : "
                    + result["candidate"]
                    + "\n\n"
                )

                self.detail_text.insert(
                    END,
                    "Match Score : "
                    + str(result["score"])
                    + "%\n\n"
                )

                self.detail_text.insert(
                    END,
                    "Matched Skills\n"
                )

                if len(result["matched_skills"]) == 0:

                    self.detail_text.insert(
                        END,
                        "None\n"
                    )

                else:

                    for skill in result["matched_skills"]:

                        self.detail_text.insert(
                            END,
                            "✓ " + skill + "\n"
                        )

                self.detail_text.insert(
                    END,
                    "\nMissing Skills\n"
                )

                if len(result["missing_skills"]) == 0:

                    self.detail_text.insert(
                        END,
                        "None\n"
                    )

                else:

                    for skill in result["missing_skills"]:

                        self.detail_text.insert(
                            END,
                            "✗ " + skill + "\n"
                        )

                self.detail_text.insert(
                    END,
                    "\nRecommendation : "
                    + result["recommendation"]
                )

                break


# ---------------- Main ----------------

root = Tk()

app = ResumeScreeningSystem(root)

root.mainloop()