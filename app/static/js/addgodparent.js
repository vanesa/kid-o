$(function() {
  $('#newGodparentModal').on('shown.bs.modal', function () {
    $('#myInput').focus()
  });

  $('#addNewGodparentForm').on('submit', function(e) {
    e && e.preventDefault();

    var data = {
      _csrf_token: $('#addNewGodparentForm input[name="_csrf_token"]').val(),
      first_name: $('#addNewGodparentForm input[name="first_name"]').val(),
      last_name: $('#addNewGodparentForm input[name="last_name"]').val(),
      email: $('#addNewGodparentForm input[name="email"]').val(),
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
        $("#newGodparentModalBody").html( "<p>Success!</p>" );
        $("#addNewGodparentCancelButton").html("Close");
        $("#addNewGodparentButton").remove();
        $('#godparentModal').on('hide.bs.modal', function () {
          location.reload();
        });
      },
      error: function(error) {
          $("#newGodparentModalBody").append('<div class="alert alert-danger" role="alert"> Please check if all fields are valid. </div>');
          console.log(error);
      }
    });
  });
});