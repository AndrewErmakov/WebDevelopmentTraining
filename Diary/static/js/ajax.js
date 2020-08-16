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

                if (document.getElementById("participants") == null){
                    $('#note_details').append('<h3 id="participants">Participants</h3>')
                }

                $('#note_details').append(document.createTextNode(json.name));
            }
            else {
                alert('Participant was not found with name: ' + json.name);

            }
            document.getElementById("add_participant").reset();

         },
        error : function(xhr,errmsg,err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    });
});
