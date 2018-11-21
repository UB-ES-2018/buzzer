$(document).ready(function(){
	$(".multimedia").on('click', function(event) {
		event.stopPropagation();
		$(this).toggleClass("big");
	});
	
});