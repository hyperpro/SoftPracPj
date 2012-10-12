$(function(){
	$('#edit_form input').each(function(){
		var tip = $(this).next('.form_tip');
		if($(this).val()==''){
			tip.addClass('error').text("Can't be blank");
		}
	});

	$('#edit_form input').on('blur', function(){
		var tip = $(this).next('.form_tip');
		if($(this).val()==''){
			tip.addClass('error').text("Can't be blank").fadeIn('slow').delay(2000).fadeOut('slow');
		}else{
			tip.removeClass('error')
		}
	});

	$('#your_form input').on('blur', function(){
		if($(this).val()==''){
			alert("blank!")
		}
	});

	$('#submit').on('click', function(){
		if($('#edit_form .error').length>0){
			$('#edit_form .error').fadeIn('slow').delay(2000).fadeOut('slow');
			return false;
		}else{
			return true;
		}
	});
});