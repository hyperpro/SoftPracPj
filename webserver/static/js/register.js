

var first_in = true;

$(function(){
	$('#register_form input').each(function(){
		var tip = $(this).next('.form_tip');
		if($(this).val()==''){
			tip.addClass('error').text("Can't be blank");
		}
	});

	$('#register_form input').on('blur', function(){
		var tip = $(this).next('.form_tip');
		if($(this).val()==''){
			tip.addClass('error').text("Can't be blank").fadeIn('fast').delay(2000).fadeOut('slow');
		}else{
			tip.removeClass('error');

			var pwd_in = $('#pwd_in');
			var pwd_cfm_in = $('#pwd_cfm_in');
			if($(this).attr('type')=='password'){
				var pwd1 = pwd_in.val();
				var pwd2 = pwd_cfm_in.val();
				if(pwd1 != pwd2){
					if(!first_in){
						tip.addClass('error').text("Different password!").fadeIn('fast').delay(2000).fadeOut('slow');
					}else{
						tip.addClass('error').text("Different password!");
						first_in = false;
					}
				}else{
					pwd_ins = [pwd_in, pwd_cfm_in];
					for(var i in pwd_ins){
						var _tip = pwd_ins[i].next('.form_tip'); 
						if(_tip.text()=="Different password!"){
							_tip.removeClass('error');
						}
					}
					$('#pwd_in').val($.md5($('#pwd_in').val()));
					$('#pwd_cfm_in').val($.md5($('#pwd_cfm_in').val()));
				}
			}
		}

	});

	$('#submit').on('click', function(){
		if($('#register_form .error').length>0){
			$('#register_form .error').fadeIn('fast').delay(2000).fadeOut('slow');
			return false;
		}else{
			return true;
		}
	});

});
