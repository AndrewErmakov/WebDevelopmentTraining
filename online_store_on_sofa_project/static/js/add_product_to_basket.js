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