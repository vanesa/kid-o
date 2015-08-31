$('#searchform input[name="searchform"]').on("keyup", function(e) {
	var term = $('#searchform input[name="searchform"]').val();
	console.log(term);
});

$(window).scroll(function() {
  if ($(document).scrollTop() > 50) {
    $('nav').addClass('shrink');
  } else {
    $('nav').removeClass('shrink');
  }
});