$(document).ready(function() {

    var config = {
      runUrl: '/challenge/run',
    }

    $('#run-code').click(function() {
      // data = {action: 'run', code: editor.getValue()}
      // console.log(data);
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
