$(document).ready(function() {

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
