$(function() {
  $('#show_hidden_profiles').on('change', function(e) {
    var $form = $(e.target.form);
    $form.submit();
  });

});