$(document).on('submit', '#add_product_to_basket',function(e){
     e.preventDefault();
     $.ajax({
            type:'POST',
            url: $("#add_product_to_basket").prop('action'),
            data:{
                count_product:$('#number').val(),
                product_id:$(e.target).find('#product_id_to_basket').first().val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success:function(json){
                    if (json.status === 'OK'){
                        alert('added to basket');
                        if (document.getElementById("go_to_basket") == null){
                            $('#main_info_product').append('<input id="go_to_basket" type="button" value="Перейти в корзину">');
                        }
                        var count_in_warehouse = $('#count_in_warehouse').text();
                        var count_to_cart = $('#number').val();
                        $('#count_in_warehouse').text(+count_in_warehouse - +count_to_cart);

                    }
                    else if(json.status === 'MORE'){
                        alert('too much');
                    }

                    else{
                        alert('do not add to basket');
                    }
                },
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
    }
    });
});

$('#increase_num').on('click', function() {
	var current_count = $('#number').val();
	current_count = +current_count + 1;
	$('#number').val(current_count);
});


$('#reduce_num').on('click', function() {
	var current_count = $('#number').val();
	if (current_count > 1){
		current_count = +current_count - 1;
		$('#number').val(current_count);
	}
	else{
		alert('Минимальное количество товаров для заказа - 1');
	}

});

