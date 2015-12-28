$(document).ready(function() {

    var readyToSubmit = false;
    var testsPassedMsg = $('.js_tests_passed');
    var testsFailedMsg = $('.js_tests_failed');
    var errorMsg = $('.js_error_msg');
    var runCodeButton = $('#run_code');
    var tokenField = $('#id_solution_token');

    function renderNotification(data) {
      notifications = $('.js_notifications_list');
      count = $('.js_notifications_count');
      notification = $('.js_notification_template').first().html()
                       .replace('__notification_body__', data.text)
                       .replace('__notification_url__', data.url);
      notifications.html(notification + notifications.html());

      if (count.hasClass('hidden')) {
        count.html('1');
        count.removeClass('hidden');
      }
      else {
        count.html(parseInt(count.html(), 10) + 1)
      }

    }

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
      else if (data.action == 'notification') {
        renderNotification(data);
      }
    }

    var ws = new WebSocket(websocketUrl + '?' + userId);

    ws.onopen = function() {
      data = {
        action: 'init',
        user: userId,
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

})
