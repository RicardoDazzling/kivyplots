from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDIcon, MDLabel
from kivy.properties import StringProperty, ListProperty
from .utils import metrics


class MDChartTitle(MDBoxLayout):

    # region Properties
    icon = StringProperty('')
    font_style = StringProperty('Body1')
    min_size = ListProperty([0, 0])
    _title_list = []
    # endregion

    # region __init__:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(icon=self._update, font_style=self._update)
    # endregion

    # region Public Methods:
    def add_title(self, title: str, color: list):
        __bl = MDBoxLayout(spacing='10dp', size_hint=(None, None), adaptive_height=True)
        __label = MDLabel(text=title, font_style=self.font_style, size_hint=(None, None), adaptive_height=True)
        __icon = MDIcon(icon=self.icon, text_color=color, theme_text_color="Custom", text_size=__label.text_size,
                        size_hint=(None, None), adaptive_height=True)
        __bl.add_widget(__icon)
        __bl.add_widget(__label)
        self._update_min_size(__label, __icon, __bl)
        self.add_widget(__bl)
        self._title_list.append(__bl)
    # endregion

    # region Protected Methods:
    def _update_min_size(self, label: MDLabel, icon: MDIcon, title_box: MDBoxLayout):
        __new_min_size = (label.width + icon.width + metrics(title_box.spacing),
                          label.height + icon.height)
        self.min_size[0] = max(self.min_size[0], __new_min_size[0])
        self.min_size[1] = max(self.min_size[1], __new_min_size[1])
    # endregion

    # region Bind Methods:
    def _update(self, *args):
        if self._title_list:
            for title in self._title_list:
                title.children[0].font_style = self.font_style
                title.children[1].text_size = title.children[0].text_size
                title.children[1].icon = self.icon

    def _min_size_update(self, *args):
        self.min_size = [0, 0]
        for title in self._title_list:
            __label = title.children[0]
            __icon = title.children[1]
            self._update_min_size(__label, __icon, title)
    # endregion
