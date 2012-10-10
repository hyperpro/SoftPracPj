$(function(){
	$('.video_block').on('click', function(){
		$('#block2').removeClass('wide_block').addClass('normal_block');
		$('#block3').removeClass('hide_block');
		$('#expand').show();
	});

	$('#expand').on('click', function(){
		$('#block2').removeClass('normal_block').addClass('wide_block');
		$('#block3').addClass('hide_block');
		$('#expand').hide();
	});
	$('#close').on('click', function(){
		$('#expand').click();
	});
});