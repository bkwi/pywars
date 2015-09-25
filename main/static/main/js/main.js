$(document).ready(function() {


    $('.js_send_feedback').click(function() {
      $.post('/main/feedback', {
          data: $('.js_feedback').val(),
          csrfmiddlewaretoken: csrfToken
        })
        .done(function(data) {
          $('.js_send_feedback').hide();
          $('.js_feedback_form').hide();
          $('.js_feedback_success').fadeIn();
        })
        .fail(function(err) {
          alert('Something went wrong, sorry :(');
        });
    })
})
