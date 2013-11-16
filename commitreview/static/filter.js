$(document).ready(function() {
	commit_list_func();

	$('.tag').change(function(){
		$('#all').attr('checked', false);

		commit_list_func();
	});
});

var commit_list_func = function(){
	var filters = [];
	$('.tag:checkbox:checked').each(function () {
	    filters.push($(this).attr("id"));
	});

	$("#data").empty();

	$.get($SCRIPT_ROOT + '/review_ajax', 
		{filter_list: filters.join(",")})
		.done(function(data){
			if (data['user_list']){
				// make UL element
				var ulist = '<ul id="ulist"></ul>'
				$('#data').append(ulist);
				$.each(data['user_list'], function(index, user){
					// make IL element for each user
					var ielem = '<li id=user' + user["id"] + '>' + user["username"] + '</li>';
					$('#ulist').append(ielem);
					if (user['commits']){
						var ulist2 = '<ul id="ucommitlist' + user['id'] + '"></ul>';
						$('#user' + user['id']).append(ulist2);
						$.each(user['commits'], function(index, commit){
							if (!(commit['reviewed'])){
								var ielem2 = '<li id=u' + user["id"] + 'commit'+ commit['id'] + '>' + commit['time'] + '<a href=' + commit['url'] + '>' + commit['commit_msg'] + '</a> <form action="/markreviewed" method="post"><input type="submit" name="mark" value="mark as reviewed"><input type="hidden" name="shahash" value=' + commit['sha'] + '></form></li>';
								$('#ucommitlist' + user["id"]).append(ielem2);
							}
						});
					}
				});
			}
		});
	}