let playerPosition = 0;
const totalSpaces = 16;
let hintsLeft = 3;
let playerIcon = "❓";

// Define tile positions for a winding path
const tilePositions = [
    [50, 400], [100, 400], [150, 400], [200, 380],
    [250, 350], [300, 320], [320, 280], [350, 250],
    [380, 220], [400, 180], [420, 140], [450, 100],
    [470, 70], [500, 50], [550, 30], [600, 10]
];

// Generate tiles dynamically in a winding path
function generateTiles() {
    const tilesContainer = document.getElementById("tiles-container");
    tilesContainer.innerHTML = "";
    for (let i = 0; i < totalSpaces; i++) {
        const tile = document.createElement("div");
        tile.classList.add("tile");
        tile.innerText = i === totalSpaces - 1 ? "🏰" : i + 1;
        tile.style.left = `${tilePositions[i][0]}px`;
        tile.style.top = `${tilePositions[i][1]}px`;
        tilesContainer.appendChild(tile);
    }
}

// Move player along the predefined path
function movePlayer(spaces) {
    playerPosition += spaces;
    if (playerPosition >= totalSpaces) {
        alert("🎉 You reached the Candy Castle!");
        playerPosition = totalSpaces - 1;
    }

    let [x, y] = tilePositions[playerPosition];
    document.getElementById("player").style.transform = `translate(${x}px, ${y}px)`;
}

// Select character icon
function selectCharacter(icon) {
    playerIcon = icon;
    document.getElementById("player").innerText = icon;
}

// Display schema
function showSchema() {
    alert(`
    Tables:
    1. candy_shops (id, name, location, rating)
    2. candy_ingredients (id, name, rarity, shop_id)
    `);
}

// Generate board on load
window.onload = generateTiles;
