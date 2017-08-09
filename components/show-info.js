AFRAME.registerComponent('show-info', {
	schema: {default: ''},
	init() {
		this.el.addEventListener('click', () => {
			request_end(this.el.id);
		});
	}
});

