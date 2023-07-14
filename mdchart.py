from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.properties import ListProperty, NumericProperty, BooleanProperty, BoundedNumericProperty, ColorProperty, \
    StringProperty
from kivy.graphics import Color, Line
from kivy.lang import Builder
from typing import Optional, Union, Dict, Literal
from .mdcharttitle import MDChartTitle
from .utils import metrics, drange, dround


# region Build:
Builder.load_string("""
<MDRotatedLabel>:
    canvas.before:
        PushMatrix
        Rotate:
            angle: 90
            origin: self.center
    canvas.after:
        PopMatrix
""")


class MDRotatedLabel(MDLabel):
    pass
# endregion


class MDChart(MDBoxLayout):

    # region Properties:
    label_x_text = StringProperty('')
    label_y_text = StringProperty('')
    cords_x = ListProperty([])
    min_x = NumericProperty(None)
    max_x = NumericProperty(None)
    cords_y = ListProperty([])
    min_y = NumericProperty(None)
    max_y = NumericProperty(None)
    step_y = BoundedNumericProperty(5, min=3, max=15)
    fields = ListProperty([])
    high_precision = BooleanProperty(True)
    guidelines_color = ColorProperty([.2, .2, .2, .2])
    show_x_guidelines = BooleanProperty(False)
    show_y_guidelines = BooleanProperty(False)
    show_title_list = BooleanProperty(False)
    _type = StringProperty(None, allownone=True)
    _xlabels = ListProperty([])
    _ylabels = ListProperty([])
    # endregion

    # region __init__
    def __init__(self,
                 label_x_text: Optional[str] = None, label_y_text: Optional[str] = None,
                 cords_x: Optional[Union[list, tuple, Dict[int, str]]] = None,
                 fields: Optional[Union[list, tuple]] = None,
                 cords_y: Optional[Union[list, tuple]] = None, min_x: Optional[Union[int, float]] = None,
                 max_x: Optional[Union[int, float]] = None, min_y: Optional[Union[int, float]] = None,
                 max_y: Optional[Union[int, float]] = None, step_y: Optional[Union[int, float]] = None,
                 high_precision: Optional[bool] = None, guidelines_color: Optional[list] = None,
                 show_x_guidelines: Optional[bool] = None, show_y_guidelines: Optional[bool] = None,
                 show_title_list: Optional[bool] = None, font_style: Optional[str] = None,
                 **kwargs):
        # region kwargs:
        __spa = kwargs.get('spacing', None)
        __ori = kwargs.get('orientation', None)
        if __spa is not None:
            kwargs['spacing'] = metrics('20dp') + metrics(__spa)
        else:
            kwargs['spacing'] = metrics('20dp')
        if __ori is not None:
            __ori = 'vertical' if __ori == 'horizontal' else 'horizontal'
        else:
            __ori = 'horizontal'
            kwargs['orientation'] = 'vertical'
        super().__init__(**kwargs)
        if fields is not None:
            self.fields = list(fields)
        if cords_x is not None and len(cords_x) != 0:
            if isinstance(cords_x, dict):
                for key, value in cords_x.items():
                    self.fields.append(value)
                    self.cords_x.append(key)
            elif isinstance(cords_x, list) or isinstance(cords_x, tuple):
                self.cords_x = list(cords_x)
        if cords_y is not None and len(cords_y) != 0:
            self.cords_y = list(cords_y)
        if min_x is not None and max_x is not None:
            if min_x >= max_x:
                raise ValueError(f'The cords_x max value is less or equals than cords_x min value: {min_x} >= {max_x}')
        if min_y is not None and max_y is not None:
            if min_y >= max_y:
                raise ValueError(f'The cords_y max value is less or equals than cords_y min value: {min_y} >= {max_y}')
        if label_x_text is not None:
            self.label_x_text = label_x_text
        if label_y_text is not None:
            self.label_y_text = label_y_text
        if min_x is not None:
            self.min_x = min_x
        if max_x is not None:
            self.max_x = max_x
        if min_y is not None:
            self.min_y = min_y
        if max_y is not None:
            self.max_y = max_y
        if step_y is not None:
            self.step_y = min(15, max(3, step_y))
        if high_precision is not None:
            self.high_precision = high_precision
        if guidelines_color is not None:
            self.guidelines_color = guidelines_color
        if show_x_guidelines is not None:
            self.show_x_guidelines = show_x_guidelines
        if show_y_guidelines is not None:
            self.show_y_guidelines = show_y_guidelines
        if show_title_list is not None:
            self.show_title_list = show_title_list
        # endregion

        # region X:
        self._xlabel_box = MDBoxLayout(orientation='vertical', size_hint=(1, None), adaptive_height=True,
                                       spacing='10dp', padding=(0, '10dp'))
        self._xlabels_box = MDFloatLayout(size_hint=(1, None))
        self._xlabel = MDLabel(text=self.label_x_text, adaptive_size=True, pos_hint={'center_x': .5, 'center_y': .5})
        self._xlabel_box.add_widget(self._xlabels_box)
        if self.label_x_text != '':
            self._xlabel_box.add_widget(self._xlabel)
        # endregion

        # region Graph:
        self._graph = MDFloatLayout(size_hint=(1, 1))
        self._graph_card = MDCard(size_hint=(1, 1), radius=0, elevation=1)
        self._graph_card.add_widget(self._graph)
        # endregion

        # region Y:
        self._ylabel_box = MDBoxLayout(size_hint=(None, 1), adaptive_width=True, spacing='10dp', padding=('10dp', 0))
        self._ylabels_box = MDFloatLayout(size_hint=(None, 1))
        self._ylabel = MDRotatedLabel(text=self.label_y_text, adaptive_size=True,
                                      pos_hint={'center_x': .5, 'center_y': .5})
        if self.label_y_text != '':
            self._ylabel_box.add_widget(self._ylabel)
        self._ylabel_box.add_widget(self._ylabels_box)
        # endregion

        # region Title Box:
        self._title_box = MDCard(adaptive_size=True, pos_hint={'center_x': .5, 'top': 1}, elevation=1,
                                 padding='10dp')
        self._title_list = MDChartTitle(adaptive_size=True, spacing='10dp', orientation=__ori)
        if self._type is not None:
            self._title_list.icon = self._get_icon()
        self._title_list.bind(min_size=self._update_title_box_size)
        self._title_box.add_widget(self._title_list)
        self._title_list_items = []
        self._title_list_item_icons = []
        # endregion

        # region Grid:
        self._grid = MDGridLayout(cols=2)
        self._grid.add_widget(self._ylabel_box)
        self._grid.add_widget(self._graph_card)
        self._grid.add_widget(MDFloatLayout(size_hint=(0, 0)))
        self._grid.add_widget(self._xlabel_box)
        # endregion

        # Binding:
        self._bind()

        # region Add Widgets:
        self._title_list_status = self.show_title_list
        if self.show_title_list and __ori == 'vertical':
            self.add_widget(self._title_box)
        self.add_widget(self._grid)
        if self.show_title_list and __ori == 'horizontal':
            self.add_widget(self._title_box)
        self.on_size()
        #endregion
    # endregion

    # region Public Functions:
    def on_size(self, *args):
        self._update()
        self._draw_basic_graph()
        self._get_label_height()
        self._get_label_width()
        self._title_list._min_size_update()
    # endregion

    # region Protected Functions:
    def _bind(self):
        u = self._update
        self.bind(cords_x=u, cords_y=u, fields=u, min_x=u, max_x=u, min_y=u, max_y=u, step_y=u, high_precision=u)
        l = self._update_label_text
        self.bind(label_x_text=l, label_y_text=l)
        d = self._draw_basic_graph
        self.bind(guidelines_color=d, show_x_guidelines=d, show_y_guidelines=d)
        i = self._change_list_icon
        self.bind(_type=i)
        s = self._change_show_title_list
        self.bind(show_title_list=s)
        o = self._change_orientation
        self.bind(orientation=o)
        self.bind(size=self.on_size, pos=self.on_size)
        self._graph.bind(size=self.on_size, pos=self.on_size)

    def _unbind(self):
        u = self._update
        self.unbind(cords_x=u, cords_y=u, fields=u, min_x=u, max_x=u, min_y=u, max_y=u, step_y=u, high_precision=u)
        l = self._update_label_text
        self.unbind(label_x_text=l, label_y_text=l)
        d = self._draw_basic_graph
        self.unbind(guidelines_color=d, show_x_guidelines=d, show_y_guidelines=d)
        i = self._change_list_icon
        self.unbind(_type=i)
        s = self._change_show_title_list
        self.unbind(show_title_list=s)
        o = self._change_orientation
        self.unbind(orientation=o)
        os = self.on_size
        self.unbind(size=os, pos=os)
        self._graph.unbind(size=os, pos=os)

    def _add_title(self, title: str, color: Optional[list] = None):
        if color is None:
            color = [0, 0, 0, 0]
        self._title_list.add_title(title, color)

    def _get_icon(self) -> str:
        if self._type is not None:
            if self._type == 'line' or self._type == 'bar':
                icon = 'chart-line-variant' if self._type == 'line' else \
                       'chart-bar'
            else:
                raise Exception(f'The graph type need to be "line" or "bar", and not "{self._type}".')
            return icon
        return ''

    def _get_maxormin(self, axis: Literal['x', 'y'], max_or_min: Literal['max', 'min']) -> Union[int, float]:
        __hp = True if axis == 'x' else self.high_precision
        __default_list = self.cords_x if axis == 'x' else self.cords_y
        __default_max = self.max_x if axis == 'x' else self.max_y
        __default_min = self.min_x if axis == 'x' else self.min_y
        __min = __default_min if __default_min is not None else min(__default_list) if __default_list else None
        __max = __default_max if __default_max is not None else max(__default_list) if __default_list else None
        if __min is not None:
            if __max is not None:
                __max = __max if __hp else dround(__max)
            elif __default_list:
                __max = max(__default_list)
            else:
                __max = __min + 5
            __min = __min if __hp else int(__min)
        elif __default_list:
            if __max is not None:
                __max = __max if __hp else dround(__max)
            else:
                __max = max(__default_list)
            __min = min(__default_list)
        else:
            __max = __max if __hp else dround(__max)
            __min = __max + 5
        if max_or_min.lower() == 'max':
            return __max
        elif max_or_min.lower() == 'min':
            return __min
        else:
            raise ValueError('Invalid parameter: ' + max_or_min)

    def _get(self, axis: Literal['x', 'y']) -> list:
        __hp = True if axis == 'x' else self.high_precision
        __default_list = self.cords_x.copy() if axis == 'x' else self.cords_y.copy()
        __default_min = self.max_x if axis == 'x' else self.max_y
        __default_max = self.min_x if axis == 'x' else self.min_y
        if not __default_list and __default_min is None and __default_max is None:
            return [0, 1, 2, 3, 4]
        __min = self._get_maxormin(axis, 'min')
        __max = self._get_maxormin(axis, 'max')
        if __default_list:
            __default_list = self._over_remove(__default_list, __max, __min)
        if axis == 'y':
            myrange = drange if __hp else range
            __range = len(list(myrange(__min, __max + 1)))
            __step = __range / self.step_y if self.high_precision else __range // self.step_y
            __default_list = list(myrange(__min, __max, __step)) + [__max]
        return __default_list
    # endregion

    # region Bind Functions:
    def _update(self, *args):
        __x = self._get('x')
        __y = self._get('y')

        # Clean _xlabels_box widgets:
        for xlabel in self._xlabels:
            self._xlabels_box.remove_widget(xlabel)

        # Add _xlabels_box widgets:
        for idx, x_label_text in enumerate(__x):
            __pos_x = idx / (len(__x) - 1)
            __pos_x_key = 'center_x' if __pos_x != 0. and __pos_x != 1. else 'x' if __pos_x == 0. else 'right'
            if len(self._xlabels) <= idx:
                __new_label = MDLabel(adaptive_size=True)
                self._xlabels.append(__new_label)
            else:
                __new_label = self._xlabels[idx]
            self._xlabels[idx].text = str(__x[idx]) if len(self.fields) <= idx else self.fields[idx]
            self._xlabels[idx].pos_hint = {__pos_x_key: __pos_x, 'y': 0}
            self._xlabels_box.add_widget(__new_label)

        # Update _xlabels_box height:
        self._get_label_height()

        # Clean _ylabels_box widgets:
        for ylabel in self._ylabels:
            self._ylabels_box.remove_widget(ylabel)

        # Add _ylabels_box widgets:
        for idx, y_label_text in enumerate(__y):
            __pos_y = idx / (len(__y) - 1)
            __pos_y_key = 'center_y' if __pos_y != 0. and __pos_y != 1. else 'y' if __pos_y == 0. else 'top'
            if len(self._ylabels) <= idx:
                __new_label = MDLabel(adaptive_size=True)
                self._ylabels.append(__new_label)
            else:
                __new_label = self._ylabels[idx]
            self._ylabels[idx].text = str(__y[idx])
            self._ylabels[idx].pos_hint = {'x': 0, __pos_y_key: __pos_y}
            self._ylabels_box.add_widget(__new_label)

        # Update _ylabels_box width:
        self._get_label_width()

    def _update_label_text(self, *args):
        self._label_text(self.label_x_text, self._xlabel, self._xlabel_box)
        self._label_text(self.label_y_text, self._ylabel, self._ylabel_box)

    def _update_title_box_size(self, *args):
        # _l = len(self._title_list.children)
        # _x = metrics('20dp')
        # self._title_box.size = (self._title_list.min_size[0] + metrics(self._title_box.padding[0]) * _l + _x,
        #                         self._title_list.min_size[1] + metrics(self._title_box.padding[1]) * _l)
        pass

    def _change_list_icon(self, *args):
        if self._type is not None and self._title_list_item_icons:
            self._title_list.icon = self._get_icon()

    def _change_orientation(self, *args):
        self._title_box.orientation = 'vertical' if self.orientation == 'horizontal' else 'horizontal'

    def _change_show_title_list(self, *args):
        if self.show_title_list and (self._title_list_status is None or not self._title_list_status):
            self._change_orientation()
            if self.orientation == 'horizontal':
                self.add_widget(self._title_box)
            else:
                self.remove_widget(self._grid)
                self.add_widget(self._title_box)
                self.add_widget(self._grid)
        elif not self.show_title_list and self._title_list_status:
            self.remove_widget(self._title_box)
        self._title_list_status = self.show_title_list

    def _draw_basic_graph(self, *args):
        _g = self._graph
        _g.canvas.before.remove_group('guidelines')
        if self.show_x_guidelines:
            __x = self._get('x')
            with self._graph.canvas.before:
                Color(*self.guidelines_color, group='guidelines')
                for idx in range(len(__x)):
                    x = _g.width * idx / (len(__x) - 1)
                    __points = []
                    for _idx, x in enumerate([x, 0, x, _g.height]):
                        __even = _idx % 2 == 0
                        __points.append(x + (_g.pos[0] if __even else _g.pos[1]))
                    Line(points=__points, group='guidelines')
        if self.show_y_guidelines:
            __y = self._get('y')
            with self._graph.canvas.before:
                Color(*self.guidelines_color, group='guidelines')
                for idx in range(len(__y)):
                    y = _g.height * idx / (len(__y) - 1)
                    __points = []
                    for _idx, y in enumerate([0, y, _g.width, y]):
                        __even = _idx % 2 == 0
                        __points.append(y + (_g.pos[0] if __even else _g.pos[1]))
                    Line(points=__points, group='guidelines')

    def _get_label_height(self, *args):
        __height = 0
        if self._xlabels:
            for xlabel in self._xlabels:
                __height = max(metrics(xlabel.height), __height)
        self._xlabel.height = __height
        self._xlabels_box.height = __height

    def _get_label_width(self, *args):
        __width = 0
        if self._ylabels:
            for ylabel in self._ylabels:
                __width = max(metrics(ylabel.width), __width)
        self._ylabel.width = __width
        self._ylabels_box.width = __width
    # endregion

    # region Static Methods
    @staticmethod
    def _label_text(label_text: str, label: MDLabel, label_box: MDBoxLayout):
        if label.text == '' and label_text != '':
            label_box.add_widget(label)
        elif label.text != '' and label_text == '':
            label_box.remove_widget(label)
        label.text = label_text

    @staticmethod
    def _over_remove(array: list, maximum: Union[int, float], minimum: Union[int, float]) -> list:
        __array = array
        if max(maximum, max(__array)) > maximum or min(minimum, min(__array)) < minimum:
            for value in __array:
                __removed = False
                if maximum is not None:
                    if max(maximum, value) > maximum:
                        __array.remove(value)
                        __removed = True
                if minimum is not None and not __removed:
                    if min(minimum, value) < minimum:
                        __array.remove(value)
        return __array
    # endregion
