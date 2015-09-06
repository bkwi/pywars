$(document).ready(function() {

    // Enable pusher logging - don't include this in production
    Pusher.log = function(message) {
      if (window.console && window.console.log) {
        window.console.log(message);
      }
    };

    var pusher = new Pusher('f6529fc03db74bc20068', {
      encrypted: true
    });

    var channel = pusher.subscribe(channelName);
    channel.bind('test_result', function(data) {
        console.log(data);

        var elem = $('#test_result');
        var submitButton = $('#submit_solution');

        if (data.passed) {
            elem.html('All tests passed!').show();
            submitButton.show();
        }
        else {
            elem.html('Tests not passed! ' + data.msg).show();
            submitButton.hide();
        }
    });

    var config = {
      runUrl: '/run',
    }

    $('#run-code').click(function() {
      var body = JSON.stringify({
            solution: editor.getValue(),
            challengeId: challengeId,
            userId: userId
        });

      $.post(config.runUrl, {
            data: body,
            csrfmiddlewaretoken: csrfToken
          })
          .done(function(data) {
              console.log(data);
          })
          .fail(function(err) {
              console.log(err);
          });
    })
})

