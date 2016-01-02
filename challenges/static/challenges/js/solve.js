$(document).ready(function() {
    var runCodeButton = $('#run_code');

    runCodeButton.click(function() {

        var body = JSON.stringify({
            solution: editor.getValue(),
            challengeId: challengeId,
            userId: userId,
        });

        $.post('/challenge/run-code', {
            data: body,
            csrfmiddlewaretoken: csrfToken
          })
          .done(function(data) {
            if (data.ok) {
                var spinnerCode = '<i class="fa fa-refresh fa-spin"></i>';
                runCodeButton.html(spinnerCode + ' Testing solution');
            }
            else {
                alert('Run code failed');
            }
          })
          .fail(function(err) {
            console.log(err);
            alert('Something went wrong, sorry');
          });
    })
})
