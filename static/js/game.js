document.addEventListener('DOMContentLoaded', () => {
    const boardElement = document.getElementById('board');
    const statusElement = document.getElementById('status');
    const resetButton = document.getElementById('reset-button');
    let gameActive = true;

    // Function to render the board
    const renderBoard = (board) => {
        boardElement.innerHTML = '';
        board.forEach((row, rowIndex) => {
            row.forEach((cell, colIndex) => {
                const cellElement = document.createElement('div');
                cellElement.classList.add('cell');
                cellElement.dataset.row = rowIndex;
                cellElement.dataset.col = colIndex;
                cellElement.textContent = cell;
                if (gameActive && cell === ' ') {
                    cellElement.addEventListener('click', handleCellClick);
                }
                boardElement.appendChild(cellElement);
            });
        });
    };

    // Function to update game status
    const updateStatus = (winner) => {
        gameActive = false;
        if (winner === 'Tie') {
            statusElement.textContent = "It's a Tie!";
        } else {
            statusElement.textContent = `Player ${winner} wins!`;
        }
    };

    // Handle a click on a cell
    const handleCellClick = async (event) => {
        if (!gameActive) return;

        const row = event.target.dataset.row;
        const col = event.target.dataset.col;

        statusElement.textContent = "AI is thinking...";

        const response = await fetch('/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ row: parseInt(row), col: parseInt(col) }),
        });

        const data = await response.json();
        renderBoard(data.board);

        if (data.status === 'game_over') {
            updateStatus(data.winner);
        } else {
            statusElement.textContent = "Your Turn";
        }
    };

    // Handle reset button click
    const resetGame = async () => {
        const response = await fetch('/reset', { method: 'POST' });
        const data = await response.json();
        gameActive = true;
        statusElement.textContent = "Your Turn";
        renderBoard(data.board);
    };

    // Initial game setup
    resetButton.addEventListener('click', resetGame);
    resetGame(); // Initial call to load the first board
});