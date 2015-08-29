$(document).ready(function() {

    var config = {
      runUrl: '/run',
    }

    $('#run-code').click(function() {
      var body = JSON.stringify({
            code: editor.getValue()
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
