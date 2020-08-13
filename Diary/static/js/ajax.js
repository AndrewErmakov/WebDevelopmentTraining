$(document).on('submit', '#add_participant',function(e){
    e.preventDefault();
    $.ajax({
        type:'POST',
        url: $("#add_participant").prop('action'),
        data:{
            participant:$('#participant').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success:function(json){
            if (json.status === 'OK') {
                alert('Participant was added with name: '  + json.name);
            }
            else {
                alert('Participant was not found with name: ' + json.name);
            }
            document.getElementById("add_participant").reset();
            $('#note_details').load('{% url 'details_note' note.pk %}');
//            document.location.href = "{% url 'details_note' note.pk %}";
//            document.getElementById("note_details").reset();
         },
        error : function(xhr,errmsg,err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    });
});
