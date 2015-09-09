$(document).ready(function() {

  $('.js_vote_up').click( function() {
      var solutionId = $(this).attr('solution-id');

      var body = JSON.stringify({
        userId: userId
      });

      $.post('/solution/' + solutionId + '/vote', {
          data: body,
          csrfmiddlewaretoken: csrfToken
        })
        .done(function(data) {
          console.log(data);
          if (data.ok) {
            $('span[solution-id=' + solutionId + ']')
              .html(data.new_value);
          }
          else {
              alert('You already voted on this solution');
          }
        })
        .fail(function(err) {
          console.log(err);
          alert('Something went wrong, sorry');
        });
    })
  })

