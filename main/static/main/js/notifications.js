$(document).ready(function() {

    $('#mark_all_as_read').click(function() {
      if (!window.confirm("Are you sure?")) { return; }

      $.post('/main/notifications?action=all_read', {
          csrfmiddlewaretoken: csrfToken
        })
        .done(function(data) {
          $('.active-notification').removeClass('active-notification');
        })
        .fail(function(err) {
          alert('Something went wrong, sorry :(');
        });
    })

})
