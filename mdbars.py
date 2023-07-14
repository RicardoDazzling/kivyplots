from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tooltip import MDTooltip
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import RoundedRectangle, Line
from kivy.properties import ObjectProperty, ColorProperty, BoundedNumericProperty, ListProperty, NumericProperty
from typing import Optional, Union
from .utils import metrics


class MDBar(MDFloatLayout, MDTooltip):
    percent = BoundedNumericProperty(0, min=0, max=1)
    bar_background_color = ColorProperty((.5, .5, .5, .05))
    bar_percent_color = ColorProperty((0, 0, 0, 1))
    bar_border_color = ColorProperty((0, 0, 0, .5))
    _bar_background = ObjectProperty()
    _bar_percent = ObjectProperty()
    _bar_border = ObjectProperty()

    def __init__(self,
                 percent: Optional[Union[int, float]] = None,
                 bar_background_color: Optional[tuple] = None,
                 bar_percent_color: Optional[tuple] = None,
                 bar_border_color: Optional[tuple] = None,
                 **kwargs):
        if percent is not None:
            self.percent = percent
        if bar_background_color is not None:
            self.bar_background_color = bar_background_color
        if bar_percent_color is not None:
            self.bar_percent_color = bar_percent_color
        if bar_border_color is not None:
            self.bar_border_color = bar_border_color

        super().__init__(**kwargs)
        self.bar_percent_color = self.theme_cls.primary_color

        c = self.create_bar
        self.bind(percent=c, bar_background_color=c, bar_percent_color=c, size=c, pos=c, on_size=c, on_pos=c, width=c)
        self.create_bar()

    def create_bar(self, *args):
        self.canvas.before.clear()
        self.canvas.clear()
        self.canvas.after.clear()
        with self.canvas.before:
            Color(*self.bar_background_color)
            self._bar_background = RoundedRectangle(pos=self.pos, size_hint=(None, None),
                                                    size=(self.width, self.height),
                                                    radius=[self.width // 2, ])
        with self.canvas:
            Color(*self.bar_percent_color)
            self._bar_percent = RoundedRectangle(pos=self.pos, size_hint=(None, None),
                                                 size=(self.width, self.height * self.percent),
                                                 radius=[self.width // 2, ])

        with self.canvas.after:
            Color(*self.bar_border_color)
            self._bar_border = Line(
                pos=self.pos, size_hint=(1, self.percent),
                rounded_rectangle=(self.pos[0], self.pos[1], self.width, self.height, 100))


class MDBars(MDBoxLayout):
    _max_value = NumericProperty(None)
    values = ListProperty([])
    descriptions = ListProperty([])
    bars = ListProperty([])
    bar_width = ObjectProperty('25dp')
    bar_color = ColorProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spacing = '20dp'
        self.spacing = '20dp'
        self.bind(values=self._value_changed, descriptions=self._description_changed, size=self._size_changed,
                  bar_width=self._size_changed, bar_color=self._color_changed)

    def add_bar(self, value: int, description: str):
        if self._max_value is None:
            self._max_value = value
        elif value > self._max_value:
            self._max_value = value
        __new_bar = MDBar(percent=0 if self._max_value == 0 else value / self._max_value,
                          size_hint=(None, 1), width=self.bar_width)
        self.add_widget(__new_bar)
        self.bars.append(__new_bar)
        self.values.append(value)
        self.descriptions.append(description)

    def update_values(self, *args, **kwargs):
        __list = args
        __values = kwargs.get('values', None)
        if isinstance(args[0], list):
            __list = args[0]
        elif __values is not None:
            if isinstance(__values, list):
                __list = __values
        self.values = __list

    def update_descriptions(self, *args, **kwargs):
        __list = args
        __values = kwargs.get('descriptions', None)
        if isinstance(args[0], list):
            __list = args[0]
        elif __values is not None:
            if isinstance(__values, list):
                __list = __values
        self.descriptions = __list
        self._description_changed()

    def _size_changed(self, *args):
        __bar_width = metrics(self.bar_width)
        __padding = self._is_list(self.padding)
        __spacing = self._is_list(self.spacing)
        __self_width = metrics(self.width) - __padding - __spacing * (len(self.bars) - 1)
        _new_width = min(__bar_width, __self_width / len(self.bars))
        for bar in self.bars:
            bar.width = _new_width

    def _color_changed(self, *args):
        if self.bar_color is not None:
            for bar in self.bars:
                bar.bar_percent_color = self.bar_color

    def _value_changed(self, *args):
        if len(self.values) != len(self.bars):
            raise Exception('The number of values is different from the bars quantity.')
        self._max_value = max(self.values)
        self._update()

    def _description_changed(self, *args):
        if len(self.descriptions) != len(self.bars):
            raise Exception('The number of descriptions is different from the bars quantity.')
        for idx, bar in enumerate(self.bars):
            bar.tooltip_text = self.descriptions[idx]

    def _update(self):
        for idx, bar in enumerate(self.bars):
            bar.percent = 0 if self._max_value == 0 else self.values[idx] / self._max_value

    @staticmethod
    def _is_list(value) -> Union[float, int]:
        if isinstance(value, list):
            return metrics(value[0]) + metrics(value[2])
        else:
            return metrics(value)
