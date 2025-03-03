let playerPosition = 0;
const totalSpaces = 10; // Number of spaces on the board

function movePlayer(difficulty) {
    let moveBy = 0;

    if (difficulty === "easy") moveBy = 1;
    if (difficulty === "medium") moveBy = 2;
    if (difficulty === "advanced") moveBy = 3;

    playerPosition += moveBy;

    if (playerPosition >= totalSpaces) {
        alert("🎉 You finished the game!");
        playerPosition = totalSpaces; // Stops movement at end
    }

    updateBoard();
}

function updateBoard() {
    document.getElementById("player").style.left = (playerPosition * 50) + "px";
}
