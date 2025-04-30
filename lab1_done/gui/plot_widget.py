from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter
from plots import PlotStyle, PlotTriangle


class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.plot_base = None
        self.x_values = None
        self.y_values = None
        self.function_input = None

        self.setMinimumSize(600, 600)
        self.style = PlotStyle()

    def set_data(self, x_values, y_values, function_input):
        self.x_values = x_values
        self.y_values = y_values
        self.function_input = function_input
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Устанавливаем фон
        painter.setBrush(self.style.background_color)
        painter.drawRect(self.rect())

        # Проверяем, есть ли данные для отрисовки
        if self.x_values is None or self.y_values is None or self.function_input is None:
            painter.end()
            return

        self.plot_base = PlotTriangle(self.x_values, self.y_values, self.function_input, self.width(), self.height())

        self.plot_base.draw_grid(painter, self.style)
        # Рисуем график
        self.plot_base.draw_plot(painter)
        self.plot_base.draw_legend(painter)

        painter.end()
