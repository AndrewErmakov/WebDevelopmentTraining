$(document).on('submit', '.delete_product_in_cart_form',function(e){
     e.preventDefault();
     var prod_id = $(e.target).find('.product_id').first().val();
     $.ajax({
            type:'POST',
            url: $(".delete_product_in_cart_form").prop('action'),
            data:{
                product_id:prod_id,
                count_products:$('.count_' + prod_id).text(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success:function(json){
                    if (json.status === 'OK'){
                        console.log('delete');
                        $("#container_" + json.id).hide();
                        var total_sum = $('.total_sum').text();
                        var price_product = $('#price_' + json.id).text();
                        $('.total_sum').text(+total_sum - +price_product);
                    }
                    else {
                        alert('not delete');
                    }
                },
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
    });
});
/**/
$(document).on('submit', '.reduce_count_products_form',function(e){
     e.preventDefault();
     var prod_id = $(e.target).find('.product_id').first().val();
     var count_prod= $('.count_' + prod_id).text();
     $.ajax({
            type:'POST',
            url: $(".reduce_count_products_form").prop('action'),
            data:{
                product_id:prod_id,
                count_products:count_prod,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success:function(json){
                    if (json.status === 'OK'){
                        $('.count_' + prod_id).text(+count_prod - 1);

                        var price = $('#price_' + json.id).text();
                        $('#price_' + json.id).text(+price - +json.price);

                        var total_sum = $('.total_sum').text();
                        $('.total_sum').text(+total_sum - +json.price);
                    }
                    else if(json.status === 'ENOUGH'){
                        alert('Вы увлеклися');
                    }
                    else{
                        alert('Не уменьшилось');
                    }
                },
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
    }
    });
});
/**/
$(document).on('submit', '.increase_count_products_form',function(e){
     e.preventDefault();
     var prod_id = $(e.target).find('.product_id').first().val();
     var count_prod= $('.count_' + prod_id).text();
     $.ajax({
            type:'POST',
            url: $(".increase_count_products_form").prop('action'),
            data:{
                product_id:prod_id,
                count_products:count_prod,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success:function(json){
                    if (json.status === 'OK'){
                        $('.count_' + prod_id).text(+count_prod + 1);

                        var price = $('#price_' + json.id).text();
                        $('#price_' + json.id).text(+price + +json.price);

                        var total_sum = $('.total_sum').text();
                        $('.total_sum').text(+total_sum + +json.price);
                    }
                    else if(json.status === 'Not available'){
                        alert('Нет товара на складе');
                    }
                    else{
                        alert(json.status);
                    }
                },
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
    }
    });
});