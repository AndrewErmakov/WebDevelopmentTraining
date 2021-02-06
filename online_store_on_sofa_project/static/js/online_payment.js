$(document).ready(function() {
    var stripe = Stripe('pk_test_51IHBBrCVzhpZupSsd4RsGtgafwZ9YBs4E0XCmPJsM8BNpN023gMYw0iekw0sxiR2V5330eCOW9fkrbYxaGx0hqjx00GAEMjZ1M');
    var elements = stripe.elements();
    var clientSecret = $('#pay').attr('data-secret');

    var style = {
        base: {
            color: "#32325d",
          }
      };

    var card = elements.create("card", { style: style });
    card.mount("#card-element");
    card.on('change', function(event) {
      var displayError = document.getElementById('card-errors');
      if (event.error) {
        displayError.textContent = event.error.message;
      } else {
        displayError.textContent = '';
      }
    });
    var form = document.getElementById('payment-form');
    form.addEventListener('submit', function(ev) {
      var surname_name_client = $('#surname_and_name_on_card').val();
      ev.preventDefault();
      stripe.confirmCardPayment(clientSecret, {
        payment_method: {
          card: card,
          billing_details: {
            name: surname_name_client
          }
        }
      }).then(function(result) {
        if (result.error) {
          // Show error to your customer (e.g., insufficient funds)
          console.log(result.error.message);
        } else {
          // The payment has been processed!
          if (result.paymentIntent.status === 'succeeded') {
            alert('Оплата прошла успешно');
            $('#pay').hide();
            $('#send_order').click();
          }
        }
      });
    });
});