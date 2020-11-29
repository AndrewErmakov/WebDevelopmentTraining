$(document).on('submit', '#add_comment_form',function(e){
     e.preventDefault();
     $.ajax({
            type:'POST',
            url: $("#add_comment_form").prop('action'),
            data:{
                rating:$('#rating').val(),
                text_comment:$('#text_comment').val(),
                product_id:$('#product_id').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success:function(json){
                    if (json.status === 'OK'){
                        alert('added');
                        if (document.getElementById("comments") == null){
                            $('#product_details').append('<div class="row" id="comments"></div>');
                        }
                        $("#comments").append('<div class="panel panel-primary">'+
                            '<div class="panel-heading">Оценка: '+ json.rating +'</div>' +
                            '<div class="panel-body">' + json.text_comment + '</div>' +
                            '<div class="panel-footer">' + json.user + '</div></div>'
                        );
                        document.getElementById("add_comment_form").reset();
                        $("#add_comment_form").hide();
                    }
                    else{
                        alert('no comment added');
                    }
                },
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
    }
    });
});