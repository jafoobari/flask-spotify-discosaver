(function() {
	var burger = document.querySelector('.burger');
	var menu = document.querySelector('#'+burger.dataset.target);
	burger.addEventListener('click', function() {
		burger.classList.toggle('is-active');
		burger.classList.toggle('has-background-success');
		menu.classList.toggle('is-active');
		menu.classList.toggle('box');
	});
})();
