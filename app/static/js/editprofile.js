$(function() {
  $('#deleteGPtModal').on('shown.bs.modal', function () {
    $('#myInput').focus()
  });

// Retrieve godparent id from clicking list point
  $('#godparents_list i').on('click', function(e) {
    godparent_id = $(e.target).attr('data-id');
  });
  
// Delete godparent when confirming delete godparent warning modal
  $('#deleteGodparentForm').on('submit', function(e) {
    e && e.preventDefault();

    var data = {
      _csrf_token: $('#deleteGodparentForm input[name="_csrf_token"]').val(),
      godparent_id: godparent_id,
    };

    $.ajax({
      type: 'POST',
      url: '/delete-godparent/' + godparent_id,
      contentType: 'application/json',
      headers: {
        'X-CSRFToken': data._csrf_token,
      },
      success: function(response) {
        $("#deleteGodparentModalBody").html( "<p>Godparent deleted!</p>" );
        $("#deleteModalLabel").html( "DELETED" );
        $("#deleteGodparentCancelButton").html("Close");
        $("#deleteGodparentButton").remove();
        $('#deleteGPModal').on('hide.bs.modal', function () {
          location.reload();
        });
      },
      error: function(error) {
          $("#deleteGodparentModalBody").append('<div class="alert alert-danger" role="alert"> There was an issue. Please try again. </div>');
          console.log(error);
      }
    });
  });

// Show 'godparent will convert to project sponsor' warning modal when clicking on child activity Off toggle
  $('#is_active').change(function()  {
    
    if (!$('#is_active').prop('checked')) {
      $('#hideModal').modal('show');
    }
  });

// If clicking 'Cancel' on godparent conversion warning modal, switch activity toggle back to On
  $('#cancelHide').on('click', function() {
    $('#is_active').bootstrapToggle('on');
  })

});