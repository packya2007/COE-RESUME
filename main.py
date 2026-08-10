

from tkinter import *
from tkinter import filedialog, ttk, messagebox
import os
import re

from parser import parse_file
from matcher import calculate_score
from report import generate_report, save_report


class ResumeScreeningSystem:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Resume Screening & Job Description Matching System"
        )

        self.root.geometry("1200x800")

        self.root.configure(bg="#F4F7FC")

        self.root.resizable(False, False)

        # ---------------- Variables ----------------

        self.resume_paths = []
        self.results = []


        header = Label(
            self.root,
            text="Resume Screening & Job Description Matching System",
            font=("Arial", 22, "bold"),
            bg="#1E3A8A",
            fg="white",
            pady=15
        )

        header.pack(fill=X)

  
  

        left = Frame(
            self.root,
            bg="#F4F7FC",
            width=350
        )

        left.pack(
            side=LEFT,
            fill=Y,
            padx=15,
            pady=15
        )

        left.pack_propagate(False)


        jd_frame = LabelFrame(
            left,
            text="Job Description",
            font=("Arial", 11, "bold"),
            padx=8,
            pady=8,
            bg="#F4F7FC"
        )

        jd_frame.pack(
            fill=X,
            pady=5
        )

        self.jd_text = Text(
            jd_frame,
            height=12,
            width=38,
            font=("Arial", 9),
            wrap=WORD
        )

        self.jd_text.pack(
            fill=X,
            pady=5
        )

        self.jd_text.insert(
            "1.0",
            "Type or paste Job Description here..."
        )

        self.jd_status = Label(
            jd_frame,
            text="Job Description: Not Entered",
            bg="#F4F7FC",
            fg="#555555",
            anchor="w"
        )

        self.jd_status.pack(fill=X)

 
        resume_frame = LabelFrame(
            left,
            text="Resume Upload",
            font=("Arial", 11, "bold"),
            padx=8,
            pady=8,
            bg="#F4F7FC"
        )

        resume_frame.pack(
            fill=X,
            pady=8
        )

        scrollbar = Scrollbar(resume_frame)

        scrollbar.pack(
            side=RIGHT,
            fill=Y
        )

        self.resume_list = Listbox(
            resume_frame,
            height=6,
            font=("Arial", 9),
            yscrollcommand=scrollbar.set
        )

        self.resume_list.pack(
            fill=X,
            expand=False
        )

        scrollbar.config(
            command=self.resume_list.yview
        )

        self.resume_button = Button(
            resume_frame,
            text="Upload Resume(s)",
            bg="#10B981",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            command=self.upload_resumes
        )

        self.resume_button.pack(
            fill=X,
            pady=5
        )

    

        self.clear_button = Button(
            left,
            text="CLEAR",
            bg="#6B7280",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            command=self.clear_all
        )

        self.clear_button.pack(
            fill=X,
            pady=5
        )



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

        self.analyze_btn.pack(
            fill=X,
            pady=10
        )



        right = Frame(
            self.root,
            bg="#F4F7FC"
        )

        right.pack(
            side=RIGHT,
            fill=BOTH,
            expand=True,
            padx=10,
            pady=15
        )



        table_frame = LabelFrame(
            right,
            text="Candidate Ranking",
            font=("Arial", 11, "bold"),
            bg="#F4F7FC",
            padx=10,
            pady=10
        )

        table_frame.pack(
            fill=BOTH,
            expand=True
        )

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
            height=12
        )

        self.table.heading("Rank", text="Rank")
        self.table.heading("Candidate", text="Candidate")
        self.table.heading("Score", text="Score")
        self.table.heading(
            "Recommendation",
            text="Recommendation"
        )

        self.table.column(
            "Rank",
            width=60,
            anchor=CENTER
        )

        self.table.column(
            "Candidate",
            width=180
        )

        self.table.column(
            "Score",
            width=100,
            anchor=CENTER
        )

        self.table.column(
            "Recommendation",
            width=220,
            anchor=CENTER
        )

        self.table.pack(
            fill=BOTH,
            expand=True
        )

        self.table.bind(
            "<<TreeviewSelect>>",
            self.show_details
        )



        detail = LabelFrame(
            right,
            text="Candidate Details",
            font=("Arial", 11, "bold"),
            bg="#F4F7FC",
            padx=10,
            pady=10
        )

        detail.pack(
            fill=BOTH,
            pady=10
        )

        self.detail_text = Text(
            detail,
            height=12,
            font=("Consolas", 10),
            wrap=WORD
        )

        self.detail_text.pack(
            fill=BOTH,
            expand=True
        )

  

        self.status = Label(
            self.root,
            text="Ready",
            bg="#1E3A8A",
            fg="white",
            anchor=W
        )

        self.status.pack(
            fill=X,
            side=BOTTOM
        )



    def parse_typed_jd(self, text):

        data = {
            "name": "",
            "skills": [],
            "experience": "",
            "education": "",
            "projects": [],
            "certifications": []
        }

        current_section = None

        lines = text.splitlines()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            clean_line = line.lstrip("-•*").strip()

            lower_line = clean_line.lower()

            # ---------------- Name ----------------

            if lower_line.startswith("name:"):

                data["name"] = clean_line.split(
                    ":", 1
                )[1].strip()

                current_section = None
                continue

            # ---------------- Skills ----------------

            if lower_line.startswith("skills:"):

                current_section = "skills"

                value = clean_line.split(
                    ":", 1
                )[1].strip()

                if value:

                    for skill in re.split(
                        r"[,;]",
                        value
                    ):

                        skill = skill.strip()

                        if skill:
                            data["skills"].append(skill)

                continue

            # ---------------- Experience ----------------

            if lower_line.startswith("experience:"):

                current_section = "experience"

                value = clean_line.split(
                    ":", 1
                )[1].strip()

                if value:
                    data["experience"] = value

                continue

            # ---------------- Education ----------------

            if lower_line.startswith("education:"):

                current_section = "education"

                value = clean_line.split(
                    ":", 1
                )[1].strip()

                if value:
                    data["education"] = value

                continue

            # ---------------- Projects ----------------

            if lower_line.startswith("projects:"):

                current_section = "projects"

                value = clean_line.split(
                    ":", 1
                )[1].strip()

                if value:
                    data["projects"].append(value)

                continue

            # ---------------- Certifications ----------------

            if lower_line.startswith("certifications:"):

                current_section = "certifications"

                value = clean_line.split(
                    ":", 1
                )[1].strip()

                if value:
                    data["certifications"].append(value)

                continue



            if current_section == "skills":

                parts = re.split(
                    r"[,;]",
                    clean_line
                )

                for skill in parts:

                    skill = skill.strip()

                    if skill:

                        if skill.lower() not in [
                            x.lower()
                            for x in data["skills"]
                        ]:

                            data["skills"].append(skill)

            elif current_section == "experience":

                data["experience"] = clean_line

            elif current_section == "education":

                data["education"] = clean_line

            elif current_section == "projects":

                data["projects"].append(clean_line)

            elif current_section == "certifications":

                data["certifications"].append(clean_line)

        return data

 

    def upload_resumes(self):

        paths = filedialog.askopenfilenames(
            title="Select Resume Files",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )

        if paths:

            self.resume_paths = list(paths)

            self.resume_list.delete(
                0,
                END
            )

            for file in self.resume_paths:

                self.resume_list.insert(
                    END,
                    os.path.basename(file)
                )

            self.status.config(
                text=str(
                    len(self.resume_paths)
                ) + " Resume(s) Selected"
            )

  

    def analyze(self):

        jd_text = self.jd_text.get(
            "1.0",
            END
        ).strip()

        if (
            not jd_text
            or jd_text
            == "Type or paste Job Description here..."
        ):

            messagebox.showerror(
                "Error",
                "Please type or paste a Job Description."
            )

            return

        if len(self.resume_paths) == 0:

            messagebox.showerror(
                "Error",
                "Please upload at least one Resume."
            )

            return

        # Parse typed Job Description

        jd = self.parse_typed_jd(jd_text)

        if len(jd["skills"]) == 0:

            messagebox.showwarning(
                "Warning",
                "No skills detected.\n\n"
                "Please use:\n\n"
                "Skills:\n"
                "Python\n"
                "Java\n"
                "SQL"
            )

        self.results = []

        # Analyze each Resume

        for resume_file in self.resume_paths:

            try:

                resume = parse_file(
                    resume_file
                )

                result = calculate_score(
                    jd,
                    resume
                )

                self.results.append(result)

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    "Error processing:\n"
                    + os.path.basename(resume_file)
                    + "\n\n"
                    + str(e)
                )

                return

        # Generate Report

        try:

            report = generate_report(
                self.results
            )

            save_report(report)

        except Exception as e:

            messagebox.showwarning(
                "Warning",
                "Analysis completed but report "
                "could not be saved.\n\n"
                + str(e)
            )

        # Sort Results

        self.results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        # Clear Table

        for row in self.table.get_children():

            self.table.delete(row)

        # Display Results

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
            "1.0",
            END
        )

        self.detail_text.insert(
            END,
            "Analysis Completed Successfully.\n\n"
            "Select a candidate from the table "
            "to view details."
        )

        self.jd_status.config(
            text="Job Description: Entered",
            fg="#059669"
        )

        self.status.config(
            text="Analysis Completed | Report Saved"
        )

        messagebox.showinfo(
            "Success",
            "Resume Analysis Completed Successfully.\n\n"
            "Report saved to output/report.txt"
        )



    def show_details(self, event):

        selected = self.table.focus()

        if selected == "":
            return

        values = self.table.item(
            selected,
            "values"
        )

        if not values:
            return

        candidate = values[1]

        self.detail_text.delete(
            "1.0",
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
                    "Recommendation : "
                    + result["recommendation"]
                    + "\n\n"
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

                break



    def clear_all(self):

        self.jd_text.delete(
            "1.0",
            END
        )

        self.jd_text.insert(
            "1.0",
            "Type or paste Job Description here..."
        )

        self.jd_status.config(
            text="Job Description: Not Entered",
            fg="#555555"
        )

        self.resume_paths = []

        self.resume_list.delete(
            0,
            END
        )

        for row in self.table.get_children():

            self.table.delete(row)

        self.detail_text.delete(
            "1.0",
            END
        )

        self.results = []

        self.status.config(
            text="Ready"
        )




if __name__ == "__main__":

    root = Tk()

    app = ResumeScreeningSystem(root)

    root.mainloop()