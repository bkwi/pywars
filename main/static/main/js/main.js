$(document).ready(function() {

    $('.notifications-menu').click(function() {
      var notificationsCounter = $('.js_notifications_count')
      if (notificationsCounter.hasClass('hidden')) { return; }

      $.post('/main/notifications?action=dismiss', {
          csrfmiddlewaretoken: csrfToken
        })
        .done(function(data) {
          notificationsCounter.addClass('hidden');
        })
        .fail(function(err) {
          alert('Something went wrong, sorry :(');
        });
    })

    $('.js_notification').click(function() {
      var notification = $(this);
      var notificationId = $(this).attr('id');

      $.post('/main/notifications?action=deactivate&id=' + notificationId, {
          csrfmiddlewaretoken: csrfToken
        })
        .done(function(data) {
          notification.removeClass('active-notification');
        })
        .fail(function(err) {
          console.log(err);
          alert('Something went wrong, sorry :(');
        });
    })

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
