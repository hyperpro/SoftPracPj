$(function(){
	$('#upload_form #choose').on('click', function(){
		$('input[name=up_file]').click();
		return false;
	});

	$('input[name=up_file]').on('change', function(){
		var tip = $('#choose').next('.form_tip');

		file_name = $(this).val().match(/[^\\]*$/)[0];
		if(file_name!=""){
			file_type=file_name.match(/[^\.]*$/)[0];			
			if(file_type!="mp4" && file_type!="ogg" && file_type!="webm"){
				tip.addClass('error').text("File type not support!").fadeIn('slow').delay(2000).fadeOut('slow');
			}else{
				$('input[name=file_type]').val(file_type);
				tip.removeClass('error');
			}

			$('#choose').text(file_name);
			$('#submit').addClass('btn_stress');
		}else{
			tip.addClass('error').text("Please choose a file!").fadeIn('slow').delay(2000).fadeOut('slow');

			$('#choose').text("未选择文件...");
			$('#submit').removeClass('btn_stress');
		}
	});

	$('#submit').on('click', function(){
		if($('#upload_form .error').length>0){
			$('#upload_form .error').fadeIn('slow').delay(2000).fadeOut('slow');
			return false;
		}else{
			return true;
		}
	});
});