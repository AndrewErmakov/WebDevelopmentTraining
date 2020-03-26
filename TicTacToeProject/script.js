window.onload = function () {
    let field_cell = '';
    /*Generating a tic-tac-toe field of size 3*/
    for (let i = 0; i < 9; i++){
        if (i % 3 == 0){
            field_cell += '<tr>'
        }
        field_cell += '<td class="empty_ceil"></td>'
        if ((i + 1) % 3 == 0){
            field_cell += '</tr>'
        }
        document.getElementById('playing_field').innerHTML = field_cell
    }
    let players_move = 0;
    /*When clicking on a cell, a cross or a zero is put*/
    document.getElementById('playing_field').onclick = function (event) {
        if (event.target.className == 'empty_ceil'){
            if (players_move % 2 == 0) {
                event.target.innerHTML = 'X';
            }
            else {
                event.target.innerHTML = 'O';
            }
            players_move += 1;
            event.target.className = 'ceil'
        }
    }
    function checkWinner() {
        let boxes = document.getElementsByClassName('ceil');
        console.log(boxes);
    }
}