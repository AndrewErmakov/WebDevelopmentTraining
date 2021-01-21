$("#client_phone").hover(function(){
    $("#client_phone").mask("+7(999)999-9999");
});


$(document).on('submit', '.feedback_form',function(e){
     e.preventDefault();
     $.ajax({
            type:'POST',
            url: $(".feedback_form").prop('action'),
            data:{
                name:$('#client_name').val(),
                phone:$('#client_phone').val(),
                email:$('#client_email').val(),
                question:$('#question_client').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success:function(json){
                    if (json.status === 'OK'){
                        $(".modal-body").empty();
                        $(".modal-body").append("<h3 align='center'><code>Спасибо, мы с вами свяжемся</code></h3><hr>")
                    }
                    else {
                        alert('Чет не получилось, сорян');
                    }
                },
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
    });
});
