$(document).on('submit', '#delete_product_in_cart_form',function(e){
     e.preventDefault();
     $.ajax({
            type:'POST',
            url: $("#delete_product_in_cart_form").prop('action'),
            data:{
                product_id:$('#product_id').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success:function(json){
                    if (json.status === 'OK'){
                        alert('delete');
                        /*$("#product_" + json.id).hide();*/
                    }
                    else{
                        alert('not delete');
                    }
                },
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
    }
    });
});