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

    var readyToSubmit = false;

    var channel = pusher.subscribe(channelName);
    channel.bind('test_result', function(data) {
        console.log(data);

        var testsPassedMsg = $('.js_tests_passed');
        var testsFailedMsg = $('.js_tests_failed');
        var errorMsg = $('.js_error_msg');
        var runCodeButton = $('#run_code');
        var tokenField = $('#id_solution_token');

        if (data.passed) {
            testsPassedMsg.show();
            testsFailedMsg.hide()

            if (readyToSubmit) {
                $('#challenge_form').submit();
            }

            tokenField.val(data.solution_token);
            readyToSubmit = true;
            runCodeButton.html('Submit solution');
        }
        else {
            errorMsg.html(data.msg);
            testsFailedMsg.show();
            testsPassedMsg.hide();
            readyToSubmit = false;
            runCodeButton.html('Test my solution');
        }
    });

    var config = {
      runUrl: '/run',
    }

    $('#run_code').click(function() {
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

