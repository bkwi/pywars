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

    var channel = pusher.subscribe('test_channel');
    channel.bind('test_result', function(data) {
        var elem = $('#test_result');
        if (data.passed) {
            elem.html('PASSED!').show();
        }
        else {
            elem.html('NOT PASSED!').show();
        }
    });

    var config = {
      runUrl: '/run',
    }

    $('#run-code').click(function() {
      var body = JSON.stringify({
            solution: editor.getValue(),
            challengeId: challengeId
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
