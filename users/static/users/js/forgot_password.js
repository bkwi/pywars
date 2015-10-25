$(document).ready(function() {

  var changeState = function () {
    $('.js_arrow').toggle();
    $('.js_spinner').toggle();
  }

  var displayInfo = function () {
    $('#forgot_password_elements').hide();
    $('.js_email_sent').fadeIn();
  }

  $('form').submit(function (event) {
    event.preventDefault();
    email = $('input[type="email"]').val();

    if (email === '') { return }
    changeState();

    $.post('/user/forgot-password/', {
        email: email,
        csrfmiddlewaretoken: csrfToken
      })
      .done(function(data) {
        if (data.ok) {
          changeState();
          displayInfo();
        }
        else {
          alert('Something went wrong, sorry');
        }
      })
      .fail(function(err) {
        console.log(err);
        alert('Something went wrong, sorry');
      });

  });
})
