$(document).on('submit', '#add_product_to_basket',function(e){
     e.preventDefault();
     $.ajax({
            type:'POST',
            url: $("#add_product_to_basket").prop('action'),
            data:{
                product_id:$('#product_id_to_basket').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                action: 'post'
            },
            success:function(json){
                    if (json.status === 'OK'){
                        alert('added to basket')
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
