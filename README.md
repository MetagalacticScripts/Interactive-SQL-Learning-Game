# SQL Learning Game

Welcome to the SQL Learning Game! This is an interactive desktop application built with Python and Tkinter to help you learn and practice SQL queries in a fun, gamified way. Test your skills with challenges ranging from basic SELECT statements to advanced JOINs, aggregations, and more – all while earning points and unlocking achievements.

## Features

- **Interactive Challenges:**  
  - Practice SQL with a variety of questions across multiple skill areas including filtering, aggregations, grouping, and joins.
  - Challenges cover basic ad hoc queries, aggregations (SUM, COUNT, MAX, MIN, GROUP BY), table creation, indexing, and both inner and outer joins.

- **Educational Feedback:**  
  - Get detailed explanations and syntax hints for each query to understand why your answer was right or wrong.

- **Gamification:**  
  - Earn points based on correctness and time management.
  - Use hints (up to 3 per game) or show the answer (for a penalty) if you’re stuck.
  - Track your progress with real-time score updates and a final summary of your performance.

- **User-Friendly Interface:**  
  - Features a clean and clear interface with a prominent “Submit Query” button.
  - In-memory SQLite database with sample `employees` and `departments` tables.
  - A timer for each challenge keeps you on track.

## Installation

### Prerequisites

- Python 3.x (tested with Python 3.9+)
- No external libraries are required beyond Python's standard library (uses `sqlite3`, `tkinter`, etc.)

### Download and Setup

Clone this repository or download the ZIP file:

```bash
git clone https://github.com/yourusername/sql-learning-game.git
```

*Replace `yourusername` with your GitHub username.*

Navigate to the project folder:

```bash
cd sql-learning-game
```

## Usage

Run the game by executing:

```bash
python main.py
```

### How to Play

1. **Start the Game:**  
   Launch the app. Click "Database Info" to see the table structures and sample data.
   
2. **Answer Challenges:**  
   - Each challenge displays a SQL question.  
   - Type your SQL query in the input box and click the **Submit Query** button.
   - If you’re stuck, click **Hint** (up to 3 times per game) for detailed syntax help.
   - If needed, click **Show Answer** (at the bottom) to reveal the correct query (this deducts 100 points).

3. **Timer:**  
   - Each question has a 60-second timer.  
   - When time runs out, 100 points are deducted, and the correct answer is shown.

4. **Progress:**  
   - Move to the next challenge with the **Next Challenge** button.
   - After all challenges, a final summary shows your total questions, correct/incorrect counts, and suggestions for further study.

## Sample Gameplay

**Challenge:** "Retrieve all employees from the Engineering department."  
**Your Query:** `SELECT * FROM employees WHERE department = 'Engineering';`  
**Result:**  
- If correct, you'll see a confirmation message and earn points.  
- If incorrect, you'll lose points and see the correct query along with a detailed hint.

### Database Info

- **employees:** (id, name, age, department)  
- **departments:** (department, location)

## Contributing

Contributions are welcome! To contribute:

1. Fork this repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a Pull Request.

**Ideas for Future Enhancements:**

- Additional SQL challenges (e.g., INSERT, UPDATE, DELETE)
- More complex aggregations and grouping challenges (e.g., SUM, MIN, GROUP BY)
- Outer joins and index creation challenges
- A local leaderboard or multiplayer mode

## License

This project is open-source under the [MIT License](LICENSE). Feel free to use, modify, and share it!

## Acknowledgments

- Built with ❤️ using Python, Tkinter, and SQLite.
- Inspired by a passion for teaching SQL in an engaging and interactive way.

Enjoy learning SQL, and happy querying!
