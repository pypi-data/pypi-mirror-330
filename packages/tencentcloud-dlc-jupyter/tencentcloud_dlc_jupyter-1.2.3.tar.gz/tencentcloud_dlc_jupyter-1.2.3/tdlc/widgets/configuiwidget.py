from ipywidgets import widgets 
from tdlc.utils import render

from tdlc.widgets import createsessionwidget, managesessionwidget


class ConfigUiWidget(widgets.VBox):


    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)

        self.children = []

        self.controller = controller

        self._on_refresh()

    def hide_all(self):
        for child in self.children:
            child.visible = False

    def _repr_html_(self):
        for child in self.children:
            render.render(child)
        return ""

    def _on_refresh(self):

        widget_tab = widgets.Tab()
        widget_tab.children = [
            createsessionwidget.CreateSessionWidget(self.controller),
            # managesessionwidget.ManageSessionWidget(self.controller)
        ]

        widget_tab.set_title(0, 'Session 创建')
        # widget_tab.set_title(1, 'Session 列表')

        self.children = [widget_tab]
        widget_tab.parent_widget = self