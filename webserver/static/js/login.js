$(function(){
	$('#login_form input').each(function(){
		var tip = $(this).next('.form_tip');
		if($(this).val()==''){
			tip.addClass('error').text("Can't be blank");
		}
	});

	$('#login_form input').on('blur', function(){
		var tip = $(this).next('.form_tip');
		if($(this).val()==''){
			tip.addClass('error').text("Can't be blank").fadeIn('slow').delay(2000).fadeOut('slow');
		}else{
			tip.removeClass('error')
		}
	});
	
	$('#submit').on('click', function(){
		if($('#login_form .error').length>0){
			$('#login_form .error').fadeIn('slow').delay(2000).fadeOut('slow');
			return false;
		}else{
			$('#pwd_in').val($.md5($('#pwd_in').val()));
			return true;
		}
	});
});