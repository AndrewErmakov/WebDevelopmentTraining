$(".phone").mask("+7(999)999-9999");

var name_user = $('.name_recipient').val();
var surname_user = $('.surname_recipient').val();

$('#who_receive_order').on('click', function() {
   if ($('#who_receive_order').is(':checked')){
	    $('.name_recipient').val('');
	    $('.surname_recipient').val('');

   }
    else {
        $('.name_recipient').val(name_user);
        $('.surname_recipient').val(surname_user);
    }

});
