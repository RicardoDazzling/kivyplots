from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tooltip import MDTooltip
from kivymd.color_definitions import colors
from kivy.properties import ListProperty, BooleanProperty, ColorProperty
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Ellipse, Line, Mesh
from kivy.utils import get_color_from_hex
from typing import Optional, Union, Tuple, Dict
from .mdchart import MDChart


class MDLineMark(MDFloatLayout, MDTooltip):

    color = ColorProperty([0, 0, 0, 0])

    def __init__(self, color: Optional[list] = None, tooltip_text: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if tooltip_text is not None:
            self.tooltip_text = tooltip_text
        if color is not None:
            self.color = color
        _f = self._draw_ellipse
        self.bind(color=_f, size=_f, pos=_f)

    def _draw_ellipse(self, *args):
        self.canvas.remove_group('mark_ellipses')
        with self.canvas:
            Color(*self.color, group='mark_ellipses')
            Ellipse(pos=self.pos, size=self.size, group='mark_ellipses')


class MDLineChart(MDChart):

    # region Properties
    plots = ListProperty([])
    mark = BooleanProperty(False)
    line = BooleanProperty(True)
    fill = BooleanProperty(False)
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
                 mark: Optional[bool] = None, line: Optional[bool] = None,
                 fill: Optional[bool] = None,
                 **kwargs):
        self._type = 'line'
        super().__init__(label_x_text=label_x_text, label_y_text=label_y_text, cords_x=cords_x, fields=fields,
                         cords_y=cords_y, min_x=min_x, max_x=max_x, min_y=min_y, max_y=max_y, step_y=step_y,
                         high_precision=high_precision, guidelines_color=guidelines_color,
                         show_x_guidelines=show_x_guidelines, show_y_guidelines=show_y_guidelines, **kwargs)
        if mark is not None:
            self.mark = mark
        if line is not None:
            self.line = line
        if fill is not None:
            self.fill = fill
        self._type = 'line'
        self._marks = []
        self._positions = []
        _f = self._draw
        self.bind(plots=_f, mark=_f, line=_f, fill=_f, size=_f, pos=_f)
        __colors = colors.copy()

        __colors.pop('Light')
        __colors.pop('Dark')
        self._palettes = list(__colors.keys())
    # endregion

    # region Public Methods:
    def plot(self, y: Union[list, tuple], title: Optional[str] = None):
        self._unbind()
        __y = list(y)
        for y in __y:
            if not isinstance(y, int) and not isinstance(y, float):
                raise TypeError(f'The y value need to be from "int" or "float" types, and not "{type(y)}".')
            if self.min_y is None:
                self.min_y = y if self.high_precision else int(y)
            elif y < self.min_y:
                if self.max_y is None:
                    self.max_y = self.min_y
                    self.min_y = y if self.high_precision else int(y)
                else:
                    self.min_y = y if self.high_precision else int(y)
            elif self.max_y is None:
                self.max_y = y if self.high_precision else int(y)
            elif y > self.max_y:
                self.max_y = y if self.high_precision else int(y)
        self.plots.append(__y)
        self._bind()
        self._update()
        if title is not None:
            self._add_title(title, list(self._get_color(len(self.plots))))
            self.show_title_list = True

    def on_size(self, *args):
        super().on_size(*args)
        if self.plots:
            self._draw(draw_basic=False)
    # endregion

    # region Protected Methods:
    def _get_pos(self, xy: Tuple[Union[int, float], Union[int, float]]) -> Tuple[Union[int, float], Union[int, float]]:
        __x = xy[0]
        __max = self._get_maxormin('x', 'max')
        __min = self._get_maxormin('x', 'min')
        __length = __max - __min
        __pos_x = 0 if __length == 0 else (__x - __min) / __length if self.high_precision else (__x - __min) // __length
        __y = xy[1]
        __max = self._get_maxormin('y', 'max')
        __min = self._get_maxormin('y', 'min')
        __length = __max - __min
        __pos_y = 0 if __length == 0 else (__y - __min) / __length if self.high_precision else (__y - __min) // __length
        return __pos_x, __pos_y

    def _get_xy(self, plot: list) -> list:
        __xy = [(x, y) for x, y in enumerate(plot)]
        return __xy

    def _get_positions(self, plot: list) -> list:
        __xy = self._get_xy(plot)
        __positions = [(self._get_pos(xy)) for xy in __xy]
        return __positions

    def _get_color(self, idx: int) -> tuple:
        __cpi = 0
        if len(self.plots) <= __cpi or len(self.plots) <= len(self._palettes) - 1 - __cpi:
            __cpi = self._palettes.index(self.theme_cls.primary_palette)  # Color Palette Index
        __ph = self.theme_cls.primary_hue  # Primary Hue
        return get_color_from_hex(colors[self._palettes[__cpi + idx]][__ph])

    def _get_graph_pos(self, plot: Optional[list] = None, positions: Optional[list] = None) -> list:
        if positions is None:
            if plot is None:
                raise ValueError('The plot or the positions arguments need to be specified.')
            positions = self._get_positions(plot)
        graph_pos = [(p[0] * self._graph.width + self._graph.pos[0], p[1] * self._graph.height + self._graph.pos[1])
                     for p in positions]
        __return = []
        for graph_pos_xy in graph_pos:
            __return += list(graph_pos_xy)
        return __return
    # endregion

    # region Bind Methods:
    def _draw(self, *args, draw_basic: bool = True):
        __graph = self._graph
        __canvas = self._graph.canvas
        __canvas.remove_group('lines')
        __canvas.before.remove_group('mesh')

        if draw_basic:
            self._draw_basic_graph()  # Draw guidelines, if existed.

        __cpi = self._palettes.index(self.theme_cls.primary_palette)  # Color Palette Index
        if len(self.plots) > __cpi or len(self.plots) > len(self._palettes) - 1 - __cpi:
            __cpi = 0
        __ph = self.theme_cls.primary_hue  # Primary Hue
        for idx, plot in enumerate(self.plots):
            __color = get_color_from_hex(colors[self._palettes[__cpi + idx]][__ph])
            __positions = self._get_positions(plot=plot)
            __graph_position = self._get_graph_pos(positions=__positions)
            # Draw Line:
            if self.line:
                with __canvas:
                    Color(*__color, group='lines')
                    Line(points=__graph_position, width=2, group='lines')
            # Draw Fill:
            if self.fill:
                __tcolor = __color.copy()
                __tcolor = __tcolor[:3]
                gp = __graph_position.copy()
                __min_gp = __graph.pos[1]  # min graph y position
                _1 = [gp[-2], __min_gp] if __min_gp != gp[-1] else []
                _2 = [gp[0], __min_gp] if __min_gp != gp[1] else []
                gp = _2 + gp + _1 + _2
                ver, idc = self._get_vertices(gp)
                with __canvas.before:
                    Color(*__tcolor, 0.1, group='mesh')
                    Mesh(mode='triangle_fan', vertices=ver, indices=idc, group='mesh')
            # Draw Mark
            if self.mark:
                __xy = self._get_xy(plot=plot)
                __marks = []
                if len(self._marks) > idx:
                    __marks = self._marks[idx]
                for point_idx in range(len(plot)):
                    if len(__marks) > point_idx:
                        __mark = __marks[point_idx]
                    else:
                        if self.fields:
                            __tooltip_text = f'{self.fields[__xy[point_idx][0]]}: {__xy[point_idx][1]}.'
                        else:
                            x = 'x' if self.label_x_text is None or self.label_x_text.strip() == ''\
                                else self.label_x_text
                            y = 'y' if self.label_y_text is None or self.label_y_text.strip() == ''\
                                else self.label_y_text
                            __tooltip_text = f'{x}: {__xy[point_idx][0]};\n{y}: {__xy[point_idx][1]}.'
                        __mark = MDLineMark(size_hint=(None, None), size=(10,10), color=__color,
                                            tooltip_text=__tooltip_text)
                        __marks.append(__mark)
                        self._graph.add_widget(__mark)
                    __mark.pos_hint = {'center_x': __positions[point_idx][0], 'center_y': __positions[point_idx][1]}
                __cpi += 1
                if len(self._marks) > idx:
                    self._marks[idx] = __marks
                else:
                    self._marks.append(__marks)
    # endregion

    # region Static Methods:
    @staticmethod
    def _get_vertices(points: list) -> (list, list):
        __indice = []
        __vertices = []
        for idx in range(0, len(points), 2):
            __indice.append(idx // 2)
            __vertices.append(points[idx])
            __vertices.append(points[idx + 1])
            __vertices.append(0)
            __vertices.append(0)
        return __vertices, __indice
    # endregion
