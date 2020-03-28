window.onload = function () {
    let players_move = 0; // number of moves made by players
    let filled_blocks = []; // an array of current tic tac toe
    let flag = true; // game continuation flag
    which_player_makes_move();
    generate_field();

    /*When clicking on a cell, a cross or a zero is put*/
    document.getElementById('playing_field').onclick = function (event) {
        if (flag == false){
            return;
        }
        if (event.target.className == 'empty_ceil'){
            if (players_move % 2 == 0) {
                event.target.innerHTML = 'X';
                filled_blocks[Number.parseInt(event.target.id)] = 'X';
            }
            else {
                event.target.innerHTML = 'O';
                filled_blocks[Number.parseInt(event.target.id)] = 'O';
            }
            players_move += 1;
            which_player_makes_move();
            event.target.className = 'ceil';
            if (checkWinner() == true){
                flag = false;
                return;
            }
            determination_tie();
        }
    }
    function generate_field() {

        let field_cell = '';
        /*Generating a tic-tac-toe field of size 3*/
        for (let i = 0; i < 9; i++){
            if (i % 3 == 0){
                field_cell += '<tr>';
            }
            field_cell += '<td class="empty_ceil" id="' + String(i) + '"></td>';
            if ((i + 1) % 3 == 0){
                field_cell += '</tr>';
            }
            document.getElementById('playing_field').innerHTML = field_cell;
        }
    }
    function which_player_makes_move() {
        if (players_move % 2 == 0){
            document.getElementById('which_player').innerHTML = 'First player makes a move';
        }
        else {
            document.getElementById('which_player').innerHTML = 'Second player makes a move';
        }
    }

    function determination_tie() {
        if (players_move == 9){
            alert('the game is tied');
        }

    }

    
    function checkWinner() {
        let winning_combinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]
        for (let i = 0; i < winning_combinations.length; i++){
            if (filled_blocks[winning_combinations[i][0]] == 'X' && filled_blocks[winning_combinations[i][1]] == 'X'
            && filled_blocks[winning_combinations[i][2]] == 'X'){
                alert('first player won');
                return true;
            }
            else if (filled_blocks[winning_combinations[i][0]] == 'O' && filled_blocks[winning_combinations[i][1]] == 'O'
                && filled_blocks[winning_combinations[i][2]] == 'O'){
                alert('second player won');
                return true;
            }
        }
    }
    document.getElementById('restart').onclick = function () {
        document.getElementById('playing_field').innerHTML = '';
        players_move = 0;
        filled_blocks = [];
        flag = true;
        generate_field();
    }
}