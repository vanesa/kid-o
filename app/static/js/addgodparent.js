$(function() {
  $('#godparentModal').on('shown.bs.modal', function () {
    $('#myInput').focus()
  });

  $('#addGodparentForm').on('submit', function(e) {
    e && e.preventDefault();

    var data = {
      _csrf_token: $('#addGodparentForm input[name="_csrf_token"]').val(),
      first_name: $('#addGodparentForm input[name="first_name"]').val(),
      last_name: $('#addGodparentForm input[name="last_name"]').val(),
      email: $('#addGodparentForm input[name="email"]').val(),
    };

    $.ajax({
      type: 'POST',
      url: '/add-godparent/' + child_id,
      contentType: 'application/json',
      headers: {
        'X-CSRFToken': data._csrf_token,
      },
      data: JSON.stringify(data),
      success: function(response) {
        $("#godparentModalBody").html( "<p>Success!</p>" );
      },
      error: function(error) {
          console.log(error);
      }
    });
  });
});