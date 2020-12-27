$(document).on('submit', '.delete_product_in_cart_form',function(e){
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
                        console.log('delete');
                        $("#container_" + json.id).hide();
                        var total_sum = $('.total_sum').text();
                        var price_product = $('#price_' + json.id).text();
                        total_sum = +total_sum - +price_product;
                        $('.total_sum').text(total_sum);
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

