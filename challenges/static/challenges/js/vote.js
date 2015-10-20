$(document).ready(function() {

  var renderElements = function(data, solutionId) {
    var comments = $('#comments-list-' + solutionId);
    $.each(data.comments, function (i, elem) {
      // use mustache/handlebars...?
      comment = $('.js_solution_comment_template').first().html()
                  .replace('__username__', elem.author)
                  .replace('__comment_body__', elem.body)
                  .replace('__user_image__', elem.avatarUrl)
                  .replace('__created_at__', elem.createdAt)
                  .replace('__comment_id__', elem.commentId);
      comments.html(comments.html() + comment);
    });
  }

  $('.js_show_comments').click( function() {
    var solutionId = $(this).attr('solution-id');
    var commentsList = $('#comments-list-' + solutionId);
    if (commentsList.hasClass('js_comments_loaded')) { return }

    var body = JSON.stringify({
      solutionId: solutionId,
    });

    $.get('/challenge/solution-comment', {data: body})
      .done(function(data) {
        if (data.ok) {
          commentsList.addClass('js_comments_loaded');
          renderElements(data, solutionId);
        }
        else {
          alert('Something went wrong, sorry');
        }
      })
      .fail(function(err) {
        console.log(err);
        alert('Something went wrong, sorry');
      });
  })

  $('.js_add_comment').click( function() {
    var solutionId = $(this).attr('solution-id');
    var commentBody = $('input[solution-id=' + solutionId  + ']').val()

    if (commentBody === '') { return }

    var body = JSON.stringify({
      userId: userId,
      solutionId: solutionId,
      body: $('input[solution-id=' + solutionId  + ']').val()
    });

    $.post('/challenge/solution-comment', {
        data: body,
        csrfmiddlewaretoken: csrfToken
      })
      .done(function(data) {
        if (data.ok) {
          $('input[solution-id=' + solutionId  + ']').val('');
          renderElements(data, solutionId);
        }
        else {
            alert('Something went wrong, sorry');
        }
      })
      .fail(function(err) {
        console.log(err);
        alert('Something went wrong, sorry');
      });

  })

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

