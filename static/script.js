let playerPosition = 0;
const totalSpaces = 10;
let currentQuestion = null;
let hintsLeft = 3;

// Fun SQL Questions
const sqlQuestions = {
    easy: [
        { question: "Find all candy shops in 'Candyland'.", answer: "SELECT * FROM candy_shops WHERE location = 'Candyland';" },
        { question: "Get all candy ingredients that are 'Rare'.", answer: "SELECT * FROM candy_ingredients WHERE rarity = 'Rare';" }
    ],
    medium: [
        { question: "Get a list of all unique candy ingredient rarities.", answer: "SELECT DISTINCT rarity FROM candy_ingredients;" },
        { question: "Find the highest-rated candy shops.", answer: "SELECT * FROM candy_shops WHERE rating = 5;" }
    ],
    advanced: [
        { question: "Find candy ingredients and their shop names.", answer: "SELECT candy_ingredients.name, candy_shops.name FROM candy_ingredients JOIN candy_shops ON candy_ingredients.shop_id = candy_shops.id;" },
        { question: "Find the number of ingredients available at each shop.", answer: "SELECT shop_id, COUNT(*) FROM candy_ingredients GROUP BY shop_id;" }
    ]
};

// Get a random question
function getQuestion(difficulty) {
    const questions = sqlQuestions[difficulty];
    currentQuestion = questions[Math.floor(Math.random() * questions.length)];
    document.getElementById("question").innerText = currentQuestion.question;
}

// Submit answer and move player
function submitAnswer() {
    const userAnswer = document.getElementById("answer").value.trim().toLowerCase();

    if (!currentQuestion) {
        alert("Please select a difficulty first!");
        return;
    }

    if (userAnswer === currentQuestion.answer.toLowerCase()) {
        movePlayer();
        document.getElementById("answer").value = "";
        document.getElementById("question").innerText = "🎉 Correct! Select a new difficulty.";
        currentQuestion = null;
    } else {
        alert("❌ Incorrect! Try again.");
    }
}

// Move player when they answer correctly
function movePlayer() {
    let moveBy = 1;
    if (currentQuestion && sqlQuestions.medium.includes(currentQuestion)) moveBy = 2;
    if (currentQuestion && sqlQuestions.advanced.includes(currentQuestion)) moveBy = 3;

    playerPosition += moveBy;
    if (playerPosition >= totalSpaces) {
        alert("🎉 You collected all the magical candy ingredients!");
        playerPosition = totalSpaces;
    }

    updateBoard();
}

// Display movement visually
function updateBoard() {
    document.getElementById("player").style.transform = `translateX(${playerPosition * 60}px)`;
}

// Provide hints (only 3 allowed)
function getHint() {
    if (hintsLeft > 0) {
        alert("💡 Hint: Think about using WHERE or JOIN.");
        hintsLeft--;
        document.getElementById("hints").innerText = `Hints Left: ${hintsLeft}`;
    } else {
        alert("🚫 No hints left!");
    }
}
