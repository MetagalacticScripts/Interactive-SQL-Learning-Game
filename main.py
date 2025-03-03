import sqlite3
import random
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, simpledialog
import json
import os


def setup_db():
    """Set up an in-memory SQLite database with sample data."""
    conn = sqlite3.connect(':memory:')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            department TEXT
        )
    ''')
    employees_data = [
        (1, 'Alice', 30, 'HR'),
        (2, 'Bob', 25, 'Engineering'),
        (3, 'Charlie', 28, 'Sales'),
        (4, 'Diana', 32, 'Engineering'),
        (5, 'Eve', 27, 'Sales')
    ]
    cur.executemany("INSERT INTO employees VALUES (?, ?, ?, ?)", employees_data)

    cur.execute('''
        CREATE TABLE departments (
            department TEXT PRIMARY KEY,
            location TEXT
        )
    ''')
    departments_data = [
        ('HR', 'Building A'),
        ('Engineering', 'Building B'),
        ('Sales', 'Building C'),
        ('Marketing', 'Building D')
    ]
    cur.executemany("INSERT INTO departments VALUES (?, ?)", departments_data)

    conn.commit()
    return conn


class SQLGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL Learning Game")
        self.conn = setup_db()

        # Game State
        self.current_challenge = 0
        self.score = 0
        self.hints_used = 0
        self.max_hints = 3
        self.time_per_challenge = 60
        self.time_left = self.time_per_challenge
        self.timer_id = None
        self.paused = False
        self.correct_count = 0
        self.incorrect_count = 0
        self.streak = 0
        self.achievements = set()

        # Default background
        self.default_bg = root.cget("bg")

        # Difficulty selection
        self.difficulty = tk.StringVar(value="Beginner")

        # Challenges with difficulty, explanations, and variety
        self.all_challenges = [
            # Beginner
            {"question": "Retrieve all employees from the Engineering department.",
             "expected": {(2, 'Bob', 25, 'Engineering'), (4, 'Diana', 32, 'Engineering')},
             "solution": "SELECT * FROM employees WHERE department = 'Engineering';",
             "hint": "Use WHERE to filter by department.",
             "explanation": "This query filters employees where the department is 'Engineering'.",
             "difficulty": "Beginner"},
            {"question": "Retrieve the names of employees older than 28.", "expected": {('Alice',), ('Diana',)},
             "solution": "SELECT name FROM employees WHERE age > 28;",
             "hint": "Select only the name column and filter by age.",
             "explanation": "This selects only the 'name' column for employees with age greater than 28.",
             "difficulty": "Beginner"},
            # Intermediate
            {"question": "Retrieve unique department names in alphabetical order.",
             "expected": {('Engineering',), ('HR',), ('Sales',)},
             "solution": "SELECT DISTINCT department FROM employees ORDER BY department;",
             "hint": "Use DISTINCT and ORDER BY.",
             "explanation": "DISTINCT removes duplicates, and ORDER BY sorts alphabetically.",
             "difficulty": "Intermediate"},
            {"question": "Retrieve the COUNT of employees in Sales.", "expected": {(2,)},
             "solution": "SELECT COUNT(*) FROM employees WHERE department = 'Sales';",
             "hint": "Use COUNT with a WHERE clause.",
             "explanation": "COUNT(*) tallies rows matching the Sales department.", "difficulty": "Intermediate"},
            # Advanced
            {"question": "Retrieve all departments and employee counts, even those with no employees.",
             "expected": {('HR', 1), ('Engineering', 2), ('Sales', 2), ('Marketing', 0)},
             "solution": "SELECT d.department, COUNT(e.id) FROM departments d LEFT JOIN employees e ON d.department = e.department GROUP BY d.department;",
             "hint": "Use LEFT JOIN and COUNT.",
             "explanation": "LEFT JOIN includes all departments, COUNT(e.id) counts employees per department (0 if none).",
             "difficulty": "Advanced"},
            {"question": "Find employees older than the average age.",
             "expected": {(1, 'Alice', 30, 'HR'), (4, 'Diana', 32, 'Engineering')},
             "solution": "SELECT * FROM employees WHERE age > (SELECT AVG(age) FROM employees);",
             "hint": "Use a subquery with AVG.",
             "explanation": "The subquery calculates the average age (28.4), and the main query finds employees above that.",
             "difficulty": "Advanced"}
        ]
        self.filter_challenges()

        self.create_widgets()
        self.display_challenge()

    def filter_challenges(self):
        """Filter challenges based on selected difficulty."""
        level = self.difficulty.get()
        self.challenges = [c for c in self.all_challenges if c["difficulty"] == level]
        random.shuffle(self.challenges)
        if not self.challenges:
            self.challenges = self.all_challenges  # Fallback
            random.shuffle(self.challenges)

    def create_widgets(self):
        # Difficulty Selection
        difficulty_frame = tk.Frame(self.root)
        difficulty_frame.pack(pady=5)
        tk.Label(difficulty_frame, text="Difficulty:").pack(side=tk.LEFT)
        for level in ["Beginner", "Intermediate", "Advanced"]:
            tk.Radiobutton(difficulty_frame, text=level, variable=self.difficulty, value=level,
                           command=self.restart_game).pack(side=tk.LEFT)

        # Database Info Button
        self.db_info_button = tk.Button(self.root, text="Database Info", command=self.show_db_info,
                                        font=("Helvetica", 12))
        self.db_info_button.pack(pady=5)

        # Progress Bar
        self.progress = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, maximum=len(self.challenges), variable=self.progress)
        self.progress_bar.pack(pady=5)

        # Challenge Question Label
        self.question_label = tk.Label(self.root, text="", wraplength=500, justify="left", font=("Helvetica", 14))
        self.question_label.pack(pady=10)

        # Timer Label
        self.timer_label = tk.Label(self.root, text=f"Time Left: {self.time_left} sec", font=("Helvetica", 12))
        self.timer_label.pack(pady=5)

        # Pause Button
        self.pause_button = tk.Button(self.root, text="Pause", command=self.toggle_pause, font=("Helvetica", 12))
        self.pause_button.pack(pady=5)

        # SQL Query Input with Syntax Highlighting
        self.input_area = scrolledtext.ScrolledText(self.root, height=5, width=60, font=("Consolas", 12))
        self.input_area.pack(pady=10)
        self.input_area.bind("<KeyRelease>", self.highlight_syntax)

        # Submit Button
        self.submit_button = tk.Button(self.root, text="Submit Query", command=self.submit_query,
                                       font=("Helvetica", 14, "bold"), width=25, height=2, bg="#f0e68c")
        self.submit_button.pack(pady=5)

        # Hint Button
        self.hint_button = tk.Button(self.root, text="Hint", command=self.show_hint, font=("Helvetica", 12))
        self.hint_button.pack(pady=5)

        # Next Challenge Button
        self.next_button = tk.Button(self.root, text="Next Challenge", command=self.next_challenge,
                                     font=("Helvetica", 12), state="disabled")
        self.next_button.pack(pady=5)

        # Restart Button
        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_game, font=("Helvetica", 12))
        self.restart_button.pack(pady=5)

        # Results Area with Color Tags
        self.result_area = scrolledtext.ScrolledText(self.root, height=10, width=60, state='disabled',
                                                     font=("Consolas", 12))
        self.result_area.pack(pady=10)
        self.result_area.tag_config("success", foreground="green")
        self.result_area.tag_config("error", foreground="red")
        self.result_area.tag_config("info", foreground="blue")

        # Score Label
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Helvetica", 12))
        self.score_label.pack(pady=5)

        # Show Answer Button
        self.show_answer_button = tk.Button(self.root, text="Show Answer", command=self.show_answer,
                                            font=("Helvetica", 12))
        self.show_answer_button.pack(pady=10)

    def show_db_info(self):
        info_text = (
            "Database Structure:\n\n"
            "Table: employees\n - id (INTEGER PRIMARY KEY)\n - name (TEXT)\n - age (INTEGER)\n - department (TEXT)\n\n"
            "Table: departments\n - department (TEXT PRIMARY KEY)\n - location (TEXT)\n\n"
            "Sample Data (employees):\n (1, 'Alice', 30, 'HR')\n (2, 'Bob', 25, 'Engineering')\n (3, 'Charlie', 28, 'Sales')\n (4, 'Diana', 32, 'Engineering')\n (5, 'Eve', 27, 'Sales')\n\n"
            "Sample Data (departments):\n ('HR', 'Building A')\n ('Engineering', 'Building B')\n ('Sales', 'Building C')\n ('Marketing', 'Building D')"
        )
        messagebox.showinfo("Database Info", info_text)

    def display_challenge(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.root.configure(bg=self.default_bg)
        if self.current_challenge < len(self.challenges):
            challenge = self.challenges[self.current_challenge]
            self.question_label.config(text=challenge["question"])
            self.input_area.delete('1.0', tk.END)
            self.result_area.config(state='normal')
            self.result_area.delete('1.0', tk.END)
            self.result_area.config(state='disabled')
            self.time_left = self.time_per_challenge
            self.next_button.config(state="disabled")
            self.progress.set(self.current_challenge)
            if not self.paused:
                self.update_timer()
        else:
            self.show_final_summary()

    def update_timer(self):
        self.timer_label.config(text=f"Time Left: {self.time_left} sec")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.handle_timeout()

    def handle_timeout(self):
        self.result_area.config(state='normal')
        self.result_area.delete('1.0', tk.END)
        self.result_area.insert(tk.END, "Time's up! -100 points.\n", "error")
        challenge = self.challenges[self.current_challenge]
        self.result_area.insert(tk.END, "Correct query:\n", "info")
        self.result_area.insert(tk.END, f"{challenge['solution']}\n", "info")
        self.result_area.config(state='disabled')
        self.score -= 100
        self.incorrect_count += 1
        self.streak = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.next_button.config(state="normal")

    def toggle_pause(self):
        if not self.paused:
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            self.pause_button.config(text="Resume")
            self.paused = True
        else:
            self.update_timer()
            self.pause_button.config(text="Pause")
            self.paused = False

    def highlight_syntax(self, event):
        self.input_area.tag_remove("keyword", "1.0", tk.END)
        keywords = ["SELECT", "FROM", "WHERE", "JOIN", "GROUP", "ORDER", "DISTINCT", "COUNT", "AVG"]
        for word in keywords:
            start = "1.0"
            while True:
                pos = self.input_area.search(word, start, tk.END, nocase=True)
                if not pos:
                    break
                end = f"{pos}+{len(word)}c"
                self.input_area.tag_add("keyword", pos, end)
                start = end
        self.input_area.tag_config("keyword", foreground="lime")  # Changed to bright green

    def submit_query(self):
        query = self.input_area.get('1.0', tk.END).strip()
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            result = cur.fetchall()
            result_set = set(result)
            challenge = self.challenges[self.current_challenge]
            expected = challenge["expected"]

            self.result_area.config(state='normal')
            self.result_area.delete('1.0', tk.END)
            self.result_area.insert(tk.END, "Your query returned:\n")
            for row in result:
                self.result_area.insert(tk.END, f"{row}\n")

            if result_set == expected:
                bonus = self.time_left * 2
                self.score += 200 + bonus
                self.correct_count += 1
                self.streak += 1
                self.result_area.insert(tk.END, "Correct!\n", "success")  # Added "Correct!" in green
                self.result_area.insert(tk.END, f"+{200 + bonus} points.\n", "success")
                if self.streak == 3:
                    self.achievements.add("Streak Master")
                    messagebox.showinfo("Achievement", "Streak Master: 3 correct in a row!")
            else:
                self.score -= 100
                self.incorrect_count += 1
                self.streak = 0
                self.result_area.insert(tk.END, "\nIncorrect. -100 points.\n", "error")
                self.result_area.insert(tk.END, "Correct query:\n", "info")
                self.result_area.insert(tk.END, f"{challenge['solution']}\n", "info")

            self.result_area.insert(tk.END, "\nExplanation:\n", "info")
            self.result_area.insert(tk.END, f"{challenge['explanation']}\n", "info")
            self.score_label.config(text=f"Score: {self.score}")
            self.result_area.config(state='disabled')
            self.next_button.config(state="normal")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}\nCheck your syntax or table/column names.")

    def show_hint(self):
        if self.hints_used < self.max_hints:
            challenge = self.challenges[self.current_challenge]
            messagebox.showinfo("Hint", challenge["hint"])
            self.hints_used += 1
            self.score -= 50
            self.score_label.config(text=f"Score: {self.score}")
            if self.hints_used == self.max_hints:
                self.achievements.add("Hint Master")
                messagebox.showinfo("Achievement", "Hint Master: Used all hints!")
        else:
            messagebox.showinfo("Hint", "No hints left!")

    def show_answer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        challenge = self.challenges[self.current_challenge]
        self.result_area.config(state='normal')
        self.result_area.delete('1.0', tk.END)
        self.result_area.insert(tk.END, "Correct query:\n", "info")
        self.result_area.insert(tk.END, f"{challenge['solution']}\n", "info")
        self.result_area.insert(tk.END, "\nExplanation:\n", "info")
        self.result_area.insert(tk.END, f"{challenge['explanation']}\n", "info")
        self.result_area.config(state='disabled')
        self.score -= 100
        self.incorrect_count += 1
        self.streak = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.next_button.config(state="normal")

    def next_challenge(self):
        self.current_challenge += 1
        self.display_challenge()

    def show_final_summary(self):
        total = len(self.challenges)
        percent = self.correct_count / total if total > 0 else 0
        summary_text = (
            f"Game Over!\n\n"
            f"Score: {self.score}\n"
            f"Total Questions: {total}\n"
            f"Correct: {self.correct_count}\n"
            f"Incorrect: {self.incorrect_count}\n"
            f"Achievements: {', '.join(self.achievements) or 'None'}\n\n"
        )
        if percent >= 0.8:
            summary_text += "Excellent! You're mastering SQL."
        elif percent >= 0.5:
            summary_text += "Good effort! Review WHERE, aggregates, and joins."
        else:
            summary_text += "Keep practicing! Focus on SQL basics."

        self.save_score()
        messagebox.showinfo("Final Summary", summary_text)
        self.question_label.config(text="Thank you for playing!")
        self.input_area.config(state='disabled')
        self.submit_button.config(state='disabled')
        self.hint_button.config(state='disabled')
        self.show_answer_button.config(state='disabled')
        self.next_button.config(state='disabled')
        self.pause_button.config(state='disabled')
        tk.Button(self.root, text="View Leaderboard", command=self.show_leaderboard).pack(pady=5)

    def save_score(self):
        name = simpledialog.askstring("Name", "Enter your name for the leaderboard:")
        if name:
            leaderboard_file = "leaderboard.json"
            score_entry = {"name": name, "score": self.score}
            if os.path.exists(leaderboard_file):
                with open(leaderboard_file, "r") as f:
                    scores = [json.loads(line) for line in f if line.strip()]
            else:
                scores = []
            scores.append(score_entry)
            with open(leaderboard_file, "w") as f:
                for score in scores:
                    json.dump(score, f)
                    f.write("\n")

    def show_leaderboard(self):
        leaderboard_file = "leaderboard.json"
        if os.path.exists(leaderboard_file):
            with open(leaderboard_file, "r") as f:
                scores = [json.loads(line) for line in f if line.strip()]
            scores.sort(key=lambda x: x["score"], reverse=True)
            top_scores = scores[:5]
            text = "Leaderboard:\n\n" + "\n".join(
                f"{i + 1}. {s['name']}: {s['score']}" for i, s in enumerate(top_scores))
        else:
            text = "Leaderboard:\n\nNo scores yet!"
        messagebox.showinfo("Leaderboard", text)

    def restart_game(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.conn.close()
        self.conn = setup_db()
        self.current_challenge = 0
        self.score = 0
        self.hints_used = 0
        self.correct_count = 0
        self.incorrect_count = 0
        self.streak = 0
        self.achievements.clear()
        self.paused = False
        self.pause_button.config(text="Pause", state="normal")
        self.filter_challenges()
        self.display_challenge()
        self.input_area.config(state='normal')
        self.submit_button.config(state='normal')
        self.hint_button.config(state='normal')
        self.show_answer_button.config(state='normal')
        self.next_button.config(state='disabled')


def main():
    root = tk.Tk()
    app = SQLGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()