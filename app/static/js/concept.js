$(document).ready(function(){
	console.log('hello')
	$(".delete").click(function(){
		val = $(this).val()
		$("#"+val).remove()

		$.ajax({
			url : '/deleteConcept',
			dataType: "json",
			data: {'data': val},
			type: 'POST',
			success: function (data) {
				console.log(data);
				}
			});

	})
})

