/* ========================================
   GLOBAL VARIABLES & INITIAL SETUP
======================================== */
let playerPosition = 0;
const totalSpaces = 17;       // Number of tiles
let hintsLeft = 3;            // How many hints are available
let playerIcon = "🍭";        // Default player icon

/* These values have been increased to make
   the board and tiles appear larger. */
const tileSize = 100;
const tileSpacing = 120;

/* Prepare array to store [x, y] coordinates of each tile */
const tilePositions = [];

/* ========================================
   GENERATE TILE POSITIONS
======================================== */
for (let i = 0; i < totalSpaces; i++) {
  // Using 5 columns, so row = Math.floor(i/5), col = i%5
  let x = 100 + (i % 5) * tileSpacing;
  let y = 100 + Math.floor(i / 5) * tileSpacing;
  tilePositions.push([x, y]);
}

/* ========================================
   GENERATE TILES
======================================== */
function generateTiles() {
  const tilesContainer = document.getElementById("tiles-container");
  tilesContainer.innerHTML = "";

  // Create "Start" tile
  const startTile = document.createElement("div");
  startTile.classList.add("tile", "start-tile");
  startTile.innerText = "Start";
  startTile.style.left = `${tilePositions[0][0]}px`;
  startTile.style.top = `${tilePositions[0][1]}px`;
  tilesContainer.appendChild(startTile);

  // Create numbered tiles, with the last tile as a castle
  for (let i = 1; i < totalSpaces; i++) {
    const tile = document.createElement("div");
    tile.classList.add("tile");
    tile.innerText = i === totalSpaces - 1 ? "🏰" : i;
    tile.style.left = `${tilePositions[i][0]}px`;
    tile.style.top = `${tilePositions[i][1]}px`;
    tilesContainer.appendChild(tile);
  }

  // Place the player at the start tile
  resetPlayer();
}

/* ========================================
   PLAYER MOVEMENT
======================================== */
function movePlayer(spaces) {
  // Move forward by 'spaces', not exceeding last tile
  playerPosition = Math.min(playerPosition + spaces, totalSpaces - 1);

  // Reposition player icon
  const [x, y] = tilePositions[playerPosition];
  const player = document.getElementById("player");
  player.style.left = `${x}px`;
  player.style.top = `${y}px`;

  // Check if player reached the final castle
  if (playerPosition === totalSpaces - 1) {
    alert("🎉 Congratulations! You've reached the Candy Castle!");
    resetPlayer();
  }
}

/* ========================================
   RESET PLAYER
======================================== */
function resetPlayer() {
  playerPosition = 0;
  hintsLeft = 3; // Reset hints each time
  document.getElementById("hints-left").innerText = `Hints Left: ${hintsLeft}`;

  const [x, y] = tilePositions[playerPosition];
  const player = document.getElementById("player");
  player.style.left = `${x}px`;
  player.style.top = `${y}px`;
}

/* ========================================
   CHARACTER SELECTION
======================================== */
function selectCharacter(icon) {
  playerIcon = icon;
  document.getElementById("player").innerText = icon;
  resetPlayer();
}

/* ========================================
   SQL CHALLENGES
======================================== */
let currentQuestion = null;

const sqlQuestions = {
  easy: [
    {
      question: "Find all candy shops in 'Candyland'.",
      answer: "SELECT * FROM candy_shops WHERE location = 'Candyland';"
    },
    {
      question: "Get all candy ingredients that are 'Rare'.",
      answer: "SELECT * FROM candy_ingredients WHERE rarity = 'Rare';"
    }
  ],
  medium: [
    {
      question: "List all unique candy ingredient rarities.",
      answer: "SELECT DISTINCT rarity FROM candy_ingredients;"
    },
    {
      question: "Find the highest-rated candy shops.",
      answer: "SELECT * FROM candy_shops WHERE rating = 5;"
    }
  ],
  advanced: [
    {
      question: "Retrieve candy ingredients and their shop names.",
      answer: "SELECT candy_ingredients.name, candy_shops.name FROM candy_ingredients JOIN candy_shops ON candy_ingredients.shop_id = candy_shops.id;"
    },
    {
      question: "Find the number of ingredients available at each shop.",
      answer: "SELECT COUNT(*) FROM candy_ingredients GROUP BY shop_id;"
    }
  ]
};

/* ========================================
   QUESTION LOGIC
======================================== */
function getQuestion(difficulty) {
  const questionList = sqlQuestions[difficulty];
  // Randomly pick a question from the chosen difficulty
  currentQuestion = questionList[Math.floor(Math.random() * questionList.length)];

  // Display question in popup
  document.getElementById("question-text").innerText = currentQuestion.question;
  document.getElementById("answer").value = "";
  document.getElementById("question-popup").style.display = "block";
}

function submitAnswer() {
  const userAnswer = document.getElementById("answer").value.trim();

  // Compare ignoring case
  if (userAnswer.toLowerCase() === currentQuestion.answer.toLowerCase()) {
    alert("🎉 Correct! Moving forward.");
    movePlayer(1);
    document.getElementById("question-popup").style.display = "none";
    currentQuestion = null;
  } else {
    alert("❌ Incorrect! Try again.");
  }
}

function showHint() {
  if (hintsLeft > 0 && currentQuestion) {
    // Basic hint from question text
    const keyCondition = currentQuestion.question.split("'")[1] || "the key condition";
    alert(`Hint: Think about filtering with WHERE on '${keyCondition}'.`);
    hintsLeft--;
    document.getElementById("hints-left").innerText = `Hints Left: ${hintsLeft}`;
  } else {
    alert("No hints left!");
  }
}

function showDatabaseSchema() {
  alert(
    "Tables:\n" +
    "1. candy_shops - id, name, location, rating\n" +
    "2. candy_ingredients - id, name, rarity, shop_id"
  );
}

function showAnswer() {
  if (currentQuestion) {
    alert(
      `Answer: ${currentQuestion.answer}\n\n` +
      "Explanation: This query retrieves the requested data using " +
      "SQL filtering and joins as needed."
    );
  }
}

/* ========================================
   ON WINDOW LOAD
======================================== */
window.onload = () => {
  generateTiles();
};
