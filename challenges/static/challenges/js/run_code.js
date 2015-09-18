$(document).ready(function() {

    var readyToSubmit = false;
    var testsPassedMsg = $('.js_tests_passed');
    var testsFailedMsg = $('.js_tests_failed');
    var errorMsg = $('.js_error_msg');
    var runCodeButton = $('#run_code');
    var tokenField = $('#id_solution_token');

    function handleData (data) {
      if (data.action == 'test_result') {
        if (data.passed) {
          testsPassedMsg.show();
          testsFailedMsg.hide();

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
      }
    }

    var ws = new WebSocket(websocketUrl);

    ws.onopen = function() {
      data = {
        action: 'init',
        user: userId,
        challenge: challengeId
      }
      ws.send(JSON.stringify(data));
    };

    ws.onmessage = function (evt) {
      try {
        // console.log(evt.data);
        data = jQuery.parseJSON(evt.data);
        handleData(data);
      }
      catch(err) {
        console.log(err);
        console.log(evt.data);
      }
    };

    $('#run_code').click(function() {
      var body = JSON.stringify({
        action: 'test_solution',
        solution: editor.getValue(),
        challengeId: challengeId,
        userId: userId,
        tests: tests
      });
      ws.send(body)
    })
})

