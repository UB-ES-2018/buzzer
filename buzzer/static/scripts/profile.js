$(document).ready(function(){
	$(".multimedia").on('click', function(event) {
		event.stopPropagation();
		$(this).toggleClass("big");
	});

	$("#btn-follow").on('click', function(event) {
		$.ajax({
			method: "GET",
			url: '/buzzer/ajax/follow_toggle/',
			data: {
				'user': user,
				'profile': profile
			},
			dataType: 'json',
			success: function(data){
				$("#count_follower").text(data.followers);

				$("#btn-follow").toggleClass("btn-primary");
				$("#btn-follow").toggleClass("btn-success");

				var isFollowed = ($("#btn-follow").hasClass("btn-success"));

				if(isFollowed){
					$("#btn-follow-text").text("Siguiendo");					
				} else{
					$("#btn-follow-text").text("Seguir");
				}
			}
		});
	});
});