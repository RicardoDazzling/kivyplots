from kivy.graphics import PushMatrix, PopMatrix, Rotate
from kivy.metrics import dp, sp, pt, mm, cm, inch
from typing import Union, Optional
import decimal


def drange(start: Union[int, float], stop: Optional[Union[int, float]] = None, step: Optional[Union[int, float]] = None):
    if start is not None and stop is None and step is None:
        __start = 0
        __stop = start
        __step = 1
    elif start is not None and stop is not None and step is None:
        __start = start
        __stop = stop
        __step = 1
    elif start is not None and stop is not None and step is not None:
        __start = start
        __stop = stop
        __step = step
    else:
        raise ValueError('Invalid drange arguments.')
    if isinstance(__start, int) and isinstance(__stop, int) and isinstance(__step, int):
        for idx in range(__start, __stop, __step):
            yield idx
    else:
        while __start < __stop:
            yield float(__start)
            __start += decimal.Decimal(__step)


def dround(double: float) -> int:
    string = str(double)
    sub = string.split('.')[1]
    integer = int(sub)
    if integer != 0:
        return int(string.split('.')[0]) + 1
    else:
        return int(string.split('.')[0])


def rotate(widget, angle: int = 90):
    with widget.canvas.before:
        PushMatrix()
        Rotate(angle=angle, origin=widget.center)
    with widget.canvas.after:
        PopMatrix()


def metrics(metric: Union[str, int, float]) -> Union[int, float]:
    if isinstance(metric, int) or isinstance(metric, float):
        return metric
    _tests = {'dp': dp, 'sp': sp, 'pt': pt, 'mm': mm, 'cm': cm, 'inch': inch}
    for key, value in _tests.items():
        if key in metric:
            return value(metric.replace(key, ''))
    raise ValueError(f'The "metric" argument is unknown: {metric} ({type(metric)})')
        