/* global.js */

$(function(){
	var pageName = document.location.pathname

    $("#main_ops > a[href='" + pageName + "'] > li").addClass("current");
});