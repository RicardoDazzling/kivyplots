# KivyPlots

KivyPlots is a Python library for show beautiful and dynamics plots inside kivy. Now only is available line plots and bars.

## How it seans:

**MDBars:**
![MDBars](https://github.com/RicardoDazzling/kivyplots/blob/main/screenshots/bars_screenshot.png?raw=true)

**MDLineChart:**
![MDBars](https://github.com/RicardoDazzling/kivyplots/blob/main/screenshots/linechart_screenshot.png?raw=true)

## Usage

```python
from kivyplots import MDLineChart

_range = list(range(5))
self.chart = MDLineChart(cords_x=_range, fill=True, mark=True,
                         size_hint=(1, 1), show_x_guidelines=True, show_y_guidelines=True)
self.chart.plot(_range, 'Example')
_range.reverse()
self.chart.plot(_range, 'Example2')
self.chart.plot([4, 4.5, 3, 4.5, 4], 'Example3')
```
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
