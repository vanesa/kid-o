$('#searchform input[name="searchform"]').on("keyup", function(e) {
	var term = $('#searchform input[name="searchform"]').val();
	console.log(term);
});