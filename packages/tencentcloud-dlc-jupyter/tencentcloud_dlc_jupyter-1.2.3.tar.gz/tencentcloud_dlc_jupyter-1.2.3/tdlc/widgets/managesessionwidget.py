from ipywidgets import widgets 
from tdlc.utils import render


class ManageSessionWidget(widgets.Box):


	def __init__(self, controller, **kwargs):
		super().__init__(**kwargs)

		self.controller = controller

		self.children = []

		self._control_region_dropdowns = widgets.Dropdown()
	

	def _init_controls(self):
		pass
	

	def _repr_html(self):
		for child in self.children:
			render.render(child)

	def hide_all(self):
		for child in self.children:
			child.visible = False
	
	def run():
		pass

	

