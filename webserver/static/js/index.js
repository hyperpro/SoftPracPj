$(function(){
	$('.video_block').on('click', function(){
		$('#block2').removeClass('wide_block');
		$('#block3').removeClass('hide_block');
		$('#expand').show();
	});

	$('#expand').on('click', function(){
		$('#block2').addClass('wide_block');
		$('#block3').addClass('hide_block');
		$('#expand').hide();
	});
	$('#close').on('click', function(){
		$('#expand').click();
	});
});