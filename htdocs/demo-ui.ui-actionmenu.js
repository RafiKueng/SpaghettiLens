/**
 * creates and handles the Action Menu
 * in the bottom right
 */



function init_ActionMenu() {
	ui.actionMenu = new Widget(
		"actionMenu",
		"demo-ui.svg.br.svg",
		-10, -10,
		Widget.h_pos.right | Widget.v_pos.bot
	);

  ui.actionMenu.addHandler("save", Widget.event.click, ui.am.onclick.save);
  ui.actionMenu.addHandler("model", Widget.event.click, ui.am.onclick.model);
  ui.actionMenu.addHandler("next", Widget.event.click, ui.am.onclick.next);
  ui.actionMenu.addHandler("prev", Widget.event.click, ui.am.onclick.prev);

  //ui.actionMenu.addHandler("prev", Widget.event.mousemove, ui.am.onmove.prev);
  //ui.actionMenu.addHandler("bg", Widget.event.click, ui.am.onclick.bg);
  
  
  ui.actionMenu.init();  
}


ui.am = {
	onclick: {
		bg: function(evt) {alert('click on bg');},
		
		save: function(evt) {
			alert('clicked on save');
		},
		
		model:  function(evt) {
			alert('clicked on model');
			calculateModel();
		},
		
		next:  function(evt) {
			alert('clicked on next');
		},
		
		prev: function(evt) {
			var tmp = this.children[0].style;
			tmp.fill = "#8888ff";
			alert('clicked on prev');
			
			var tmp = ui.actionMenu;
			tmp = 0;
		},
	},
	onmove: {
		prev: function(evt) {
			alert('mouse moved');
		}
	}
} 