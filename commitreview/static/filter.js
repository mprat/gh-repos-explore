$(document).ready(function() {
	$('.tag').change(function(){
		$('#all').attr('checked', false);

		var filters = [];
		$('.tag:checkbox:checked').each(function () {
		    filters.push($(this).attr("id"));
		});
		$.get($SCRIPT_ROOT + '/review', 
			{filter_list: filters.join(",")})
			.done(function(data){
				alert("ajax call done")
			});
	});
});