$(document).ready(function(){
	$("#buzz-button").on('click', function(event) {
		event.stopPropagation();
		$(".form-container").removeClass("invisible");
		$("#unfocus-div").addClass("unfocus");
		height = $(document).height();
		$("#unfocus-div").css('height', height);
	});
	
	$(document).on('click', function(event) {
		if (!$(event.target).closest('.form-container').length)  {
			$(".form-container").addClass("invisible");
			$("#unfocus-div").removeClass("unfocus");
			$("#unfocus-div").css('height', 0);
		}
	});

});