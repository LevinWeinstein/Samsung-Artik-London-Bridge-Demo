AFRAME.registerComponent('show-info', {
	schema: {default: ''},
	init() {
		this.el.addEventListener('fusing', () => {
			g_endpoint = this.el.id;
			console.log(this.el.id);
			request_end();
			//g_update = 1;
		});
	}
});

