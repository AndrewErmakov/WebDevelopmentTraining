$(document).on('submit', '.delete_product_in_cart_form',function(e){
     console.log(e.target);
     e.preventDefault();
     $.ajax({
            type:'POST',
            url: $(".delete_product_in_cart_form").prop('action'),
            data:{
                product_id:$(e.target).find('.product_id').first().val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success:function(json){
                    if (json.status === 'OK'){
                        alert('delete');
                        $("#container_" + json.id).hide();
                        var total_sum = $('.total_sum').val();
                        alert(total_sum);
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

