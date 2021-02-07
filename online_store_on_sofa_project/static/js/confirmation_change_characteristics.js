$('#change_characteristics').click(function(event) {
    event.preventDefault();
    if (confirm("Вы уверены в изменении?") ) {
        $('#change').submit();
    }
    else{
        location.reload();
    }
});

