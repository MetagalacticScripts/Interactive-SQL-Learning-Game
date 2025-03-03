import sqlite3
import random
import tkinter as tk
from tkinter import scrolledtext, messagebox

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
    data = [
        (1, 'Alice', 30, 'HR'),
        (2, 'Bob', 25, 'Engineering'),
        (3, 'Charlie', 28, 'Sales'),
        (4, 'Diana', 32, 'Engineering')
    ]
    cur.executemany("INSERT INTO employees VALUES (?, ?, ?, ?)", data)
    conn.commit()
    return conn

class SQLGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL Learning Game")
        self.conn = setup_db()
        self.current_challenge = 0
        self.score = 0
        self.hints_used = 0
        self.max_hints = 2
        self.time_per_challenge = 60  # 60 seconds per question
        self.time_left = self.time_per_challenge
        self.timer_id = None  # reference for the countdown timer
        self.timeouts = 0
        self.default_bg = root.cget("bg")

        # Define challenges.
        self.challenges = [
            {
                "question": "Retrieve all employees from the Engineering department.\nHint: Use the WHERE clause.",
                "expected": {(2, 'Bob', 25, 'Engineering'), (4, 'Diana', 32, 'Engineering')},
                "solution": "SELECT * FROM employees WHERE department = 'Engineering';",
                "hint": "Filter the 'department' column with department = 'Engineering'."
            },
            {
                "question": "Retrieve the names of all employees older than 28.\nHint: Use WHERE with age > 28.",
                "expected": {('Alice',), ('Diana',)},
                "solution": "SELECT name FROM employees WHERE age > 28;",
                "hint": "Select only the 'name' column and filter using age > 28."
            },
            {
                "question": "Retrieve all employees from the HR department.\nHint: Use the WHERE clause.",
                "expected": {(1, 'Alice', 30, 'HR')},
                "solution": "SELECT * FROM employees WHERE department = 'HR';",
                "hint": "Look for employees where the department is 'HR'."
            },
            {
                "question": "Retrieve the employee with id = 3.\nHint: Use WHERE with id = 3.",
                "expected": {(3, 'Charlie', 28, 'Sales')},
                "solution": "SELECT * FROM employees WHERE id = 3;",
                "hint": "Filter by the primary key column 'id'."
            },
            {
                "question": "Retrieve all employees.\nHint: Use the SELECT statement without a WHERE clause.",
                "expected": {(1, 'Alice', 30, 'HR'), (2, 'Bob', 25, 'Engineering'),
                             (3, 'Charlie', 28, 'Sales'), (4, 'Diana', 32, 'Engineering')},
                "solution": "SELECT * FROM employees;",
                "hint": "No filtering is needed; simply select all rows."
            }
        ]
        random.shuffle(self.challenges)

        self.create_widgets()
        self.display_challenge()

    def create_widgets(self):
        # Button to show database info.
        self.db_info_button = tk.Button(self.root, text="Database Info", command=self.show_db_info,
                                        font=("Helvetica", 12), width=15, height=2)
        self.db_info_button.pack(pady=5)

        # Label to display challenge questions.
        self.question_label = tk.Label(self.root, text="", wraplength=500, justify="left", font=("Helvetica", 14))
        self.question_label.pack(pady=10)

        # Label for the timer.
        self.timer_label = tk.Label(self.root, text=f"Time Left: {self.time_left} sec", font=("Helvetica", 12))
        self.timer_label.pack(pady=5)

        # ScrolledText widget for SQL query input.
        self.input_area = scrolledtext.ScrolledText(self.root, height=5, width=60, font=("Consolas", 12))
        self.input_area.pack(pady=10)

        # Button to submit the SQL query.
        self.submit_button = tk.Button(self.root, text="Submit Query", command=self.submit_query,
                                       font=("Helvetica", 12), width=15, height=2)
        self.submit_button.pack(pady=5)

        # Button to request a hint.
        self.hint_button = tk.Button(self.root, text="Hint", command=self.show_hint,
                                     font=("Helvetica", 12), width=15, height=2)
        self.hint_button.pack(pady=5)

        # Button to move to the next challenge.
        self.next_button = tk.Button(self.root, text="Next Challenge", command=self.next_challenge,
                                     font=("Helvetica", 12), width=15, height=2, state="disabled")
        self.next_button.pack(pady=5)

        # Text area to display results and feedback.
        self.result_area = scrolledtext.ScrolledText(self.root, height=10, width=60, state='disabled',
                                                     font=("Consolas", 12))
        self.result_area.pack(pady=10)

        # Label to display the current score.
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Helvetica", 12))
        self.score_label.pack(pady=5)

    def show_db_info(self):
        """Display the database schema and sample data."""
        info_text = (
            "Database Structure:\n\n"
            "Table: employees\n"
            "Columns:\n"
            " - id (INTEGER PRIMARY KEY)\n"
            " - name (TEXT)\n"
            " - age (INTEGER)\n"
            " - department (TEXT)\n\n"
            "Sample Data:\n"
            " (1, 'Alice', 30, 'HR')\n"
            " (2, 'Bob', 25, 'Engineering')\n"
            " (3, 'Charlie', 28, 'Sales')\n"
            " (4, 'Diana', 32, 'Engineering')\n\n"
            "Use this info to write your SQL queries."
        )
        messagebox.showinfo("Database Info", info_text)

    def display_challenge(self):
        """Display the current challenge or completion message."""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        # Reset background color to default
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
            self.update_timer()
        else:
            self.question_label.config(text="Congratulations! You've completed all challenges!")
            self.input_area.config(state='disabled')
            self.submit_button.config(state='disabled')
            self.hint_button.config(state='disabled')
            self.next_button.config(state='disabled')
            self.show_achievements()

    def update_timer(self):
        """Update the countdown timer every second."""
        self.timer_label.config(text=f"Time Left: {self.time_left} sec")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.handle_timeout()

    def handle_timeout(self):
        """Handle timeout: deduct points and display the correct answer."""
        self.result_area.config(state='normal')
        self.result_area.delete('1.0', tk.END)
        self.result_area.insert(tk.END, "Time's up! You lost 100 points.\n", "error")
        challenge = self.challenges[self.current_challenge]
        self.result_area.insert(tk.END, "The correct query is:\n", "info")
        self.result_area.insert(tk.END, f"{challenge['solution']}\n", "info")
        self.result_area.config(state='disabled')
        self.score -= 100
        self.timeouts += 1
        self.score_label.config(text=f"Score: {self.score}")
        # Enable next button so they can review the answer.
        self.next_button.config(state="normal")

    def submit_query(self):
        """Execute query, update score, and display feedback."""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
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
                self.result_area.insert(tk.END, "\nAwesome! That is the correct query.\n", "success")
                self.score += 200
                # Keep background green until Next is pressed.
                self.root.configure(bg="#d0f0c0")
            else:
                self.result_area.insert(tk.END, "\nIncorrect. You lost 100 points.\n", "error")
                self.result_area.insert(tk.END, "The correct query is:\n", "info")
                self.result_area.insert(tk.END, f"{challenge['solution']}\n", "info")
                self.score -= 100
            self.score_label.config(text=f"Score: {self.score}")
            self.result_area.config(state='disabled')
            # Enable next button.
            self.next_button.config(state="normal")
        except Exception as e:
            messagebox.showerror("Error", f"There was an error with your query:\n{e}")

    def show_hint(self):
        """Display a hint for the current challenge."""
        if self.hints_used < self.max_hints:
            challenge = self.challenges[self.current_challenge]
            messagebox.showinfo("Hint", challenge.get("hint", "No hint available for this challenge."))
            self.hints_used += 1
        else:
            messagebox.showinfo("Hint", "You have used all available hints for this game.")

    def next_challenge(self):
        """Move to the next challenge."""
        self.current_challenge += 1
        self.display_challenge()

    def show_achievements(self):
        """Display achievements based on final score and hint usage."""
        achievements = []
        if self.score >= 800:
            achievements.append("SQL Pro: Amazing performance!")
        elif self.score >= 400:
            achievements.append("SQL Enthusiast: Great job!")
        else:
            achievements.append("SQL Beginner: Keep practicing!")
        if self.hints_used == 0:
            achievements.append("Hint-Free Hero: You didn't need any hints!")
        elif self.hints_used == 1:
            achievements.append("Almost Hint-Free: Only one hint used!")
        if self.timeouts == 0:
            achievements.append("Quick Thinker: You never ran out of time!")
        achievement_text = "Achievements Unlocked:\n" + "\n".join(achievements)
        messagebox.showinfo("Game Over", f"Final Score: {self.score}\n{achievement_text}")

def main():
    root = tk.Tk()
    app = SQLGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
