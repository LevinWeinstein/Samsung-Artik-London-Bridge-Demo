AFRAME.registerComponent('show-info', {
	schema: {default: ''},
	init() {
		this.el.addEventListener('click', () => {
			g_endpoint = this.el.id;
			console.log(this.el.id);
			//g_update = 1;
		});
	}
});

