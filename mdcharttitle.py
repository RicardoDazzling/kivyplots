from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDIcon, MDLabel
from kivy.properties import StringProperty


class MDChartTitle(MDBoxLayout):

    # region Properties
    icon = StringProperty('')
    font_style = StringProperty('Body1')
    _title_list = []
    _showing_titles = []
    # endregion

    # region __init__:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(icon=self._update, font_style=self._update)
    # endregion

    # region Public Methods:
    def add_title(self, title: str, color: list):
        if len(self._showing_titles) == len(self._title_list):
            __bl = MDBoxLayout(spacing='10dp', size_hint=(None, None), adaptive_height=True)
            __label = MDLabel(font_style=self.font_style, size_hint=(None, None), adaptive_height=True)
            __icon = MDIcon(icon=self.icon, theme_text_color="Custom", text_size=__label.text_size,
                            size_hint=(None, None), adaptive_height=True)
            self._title_list.append(__bl)
        else:
            __bl = self._title_list[len(self._showing_titles)]
            __label = __bl.children[0]
            __icon = __bl.children[1]
        __label.text = title
        __icon.text_color = color
        __bl.add_widget(__icon)
        __bl.add_widget(__label)
        self.add_widget(__bl)
        self._showing_titles.append(__bl)

    def clear_titles(self):
        for idx in range(len(self._showing_titles)):
            self.remove_widget(self._showing_titles.pop(idx))
    # endregion

    # region Bind Methods:
    def _update(self, *args):
        if self._title_list:
            for title in self._title_list:
                title.children[0].font_style = self.font_style
                title.children[1].text_size = title.children[0].text_size
                title.children[1].icon = self.icon
    # endregion
