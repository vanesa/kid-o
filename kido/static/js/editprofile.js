$(function() {
  $('#removeGPtModal').on('shown.bs.modal', function () {
    $('#myInput').focus()
  });

// Show or remove Add Godparent button when selecting "Has Godparent"
$(document).ready (function () {
    let gpselect = $('#godparent_status_chosen a span').text();
    if (gpselect == 'Has godparent' && (!$('#addgpbutton').length)) {
    $('#right_info').append('<p><button type="button" id="addgpbutton" class="btn btn-sm btn-success" data-toggle="modal" data-target="#godparentModal"> Add Godparent </button></p>');
    } 
  });

$('#godparent_status_chosen').on('click', function() {
  let gpselect = $('#godparent_status_chosen a span').text();
  if (gpselect == 'Has godparent' && (!$('#addgpbutton').length)) {
    $('#guardian').append('<p><button type="button" id="addgpbutton" class="btn btn-sm btn-success" data-toggle="modal" data-target="#godparentModal"> Add Godparent </button></p>');
  } 
  if (gpselect != 'Has godparent' && ($('#addgpbutton').length)) {
    $('#addgpbutton').remove();
  } 
  
});


// Retrieve godparent id from clicking list point
  $('#godparents_list i').on('click', function(e) {
    godparent_id = $(e.target).attr('data-id');
  });
  
// Remove godparent when confirming remove godparent warning modal
  $('#removeGodparentForm').on('submit', function(e) {
    e && e.preventDefault();

    var data = {
      _csrf_token: $('#removeGodparentForm input[name="_csrf_token"]').val(),
      godparent_id: godparent_id,
    };

    $.ajax({
      type: 'POST',
      url: '/remove-godparent/' + godparent_id,
      contentType: 'application/json',
      headers: {
        'X-CSRFToken': data._csrf_token,
      },
      success: function(response) {
        $("#removeGodparentModalBody").html( "<p>Godparent removed!</p>" );
        $("#removeModalLabel").html( "REMOVED" );
        $("#removeGodparentCancelButton").html("Close");
        $("#removeGodparentButton").remove();
        $('#removeGPModal').on('hide.bs.modal', function () {
          location.reload();
        });
      },
      error: function(error) {
          $("#removeGodparentModalBody").append('<div class="alert alert-danger" role="alert"> There was an issue. Please try again. </div>');
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