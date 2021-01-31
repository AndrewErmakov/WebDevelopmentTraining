$(document).ready(function(){
    var id;
    $('.btn-info').click(function(){
        id = $(this).attr('id').split('_')[4];
        $("#form_send_message_" + id).removeAttr("hidden");
    });
    $(document).on('submit', '.form_send_message',function(e){
         e.preventDefault();
         $.ajax({
                type:'POST',
                url: $(".form_send_message").prop('action'),
                data:{
                    text_answer:$('#answer_to_question_client_' + id).val(),
                    request_feedback_id:id,
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                    action: 'post'
                },
                success:function(json){
                        if (json.status === 'OK'){
                            alert('send');
                            $('#panel_' + id).hide();
                            $('#accordion_' + id).hide();

                        }
                        else{
                            alert('not send');
                        }
                },
                error : function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText);
                }
         });
    });

});
