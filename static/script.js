let playerPosition = 0;
let hintsLeft = 3;
let currentQuestion = null;
let playerIcon = "❓"; // Default before selection

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
        { question: "Find candy ingredients and their shop names.", answer: "SELECT candy_ingredients.name, candy_shops.name FROM candy_ingredients JOIN candy_shops ON candy_ingredients.shop_id = candy_shops.id;" }
    ]
};

// Character Selection
function selectCharacter(icon) {
    playerIcon = icon;
    document.getElementById("player").innerText = icon;
}

// Display Schema
function showSchema() {
    alert(`
    Tables:
    1. candy_shops (id, name, location, rating)
    2. candy_ingredients (id, name, rarity, shop_id)
    `);
}

// Movement Animation
function movePlayer(spaces) {
    playerPosition += spaces;
    if (playerPosition >= 16) {
        alert("🎉 You reached the Candy Castle!");
        playerPosition = 16;
    }
    document.getElementById("player").style.transform = `translate(${(playerPosition % 4) * 65}px, ${(Math.floor(playerPosition / 4)) * 65}px)`;
}
