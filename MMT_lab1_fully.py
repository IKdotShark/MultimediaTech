import sys
import math
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QDoubleSpinBox, QLabel, QPushButton, QLineEdit
)
from PySide6.QtGui import QPainter, QPen, QBrush, QFont, QColor, QFontMetrics
from PySide6.QtCore import Qt, QPointF

# Функции для гистограммы
def func1(x):
    """f1(x) = x"""
    return x

def func2(x):
    """f2(x) = x^2"""
    return x**2

def func3(x):
    """f3(x) = 1/x (с разрывом в 0)"""
    if x == 0 or abs(x) < 1e-10:
        return None
    return 1/x

def func4(x):
    """f4(x) = sin(x)"""
    return math.sin(x)

def func5(x):
    """f5(x) = cos(x)"""
    return math.cos(x)

def func6(x):
    """f6(x) = 2*sin(x)"""
    return 2*math.sin(x)

def func7(x):
    """f7(x) = e^(-x^2)"""
    return math.exp(-x*x)

def func8(x):
    """f8(x) = ln(x), только для x>0"""
    if x <= 0:
        return None
    return math.log(x)

def func9(x):
    """f9(x) = x^3"""
    return x**3

# Словарь функций
functions_map = {
    "1": (func1, "f(x) = x"),
    "2": (func2, "f(x) = x²"),
    "3": (func3, "f(x) = 1/x"),
    "4": (func4, "f(x) = sin(x)"),
    "5": (func5, "f(x) = cos(x)"),
    "6": (func6, "f(x) = 2*sin(x)"),
    "7": (func7, "f(x) = e^(-x²)"),
    "8": (func8, "f(x) = ln(x)"),
    "9": (func9, "f(x) = x³")
}


class StackedHistogramWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 600)

        # Настройки по умолчанию
        self.x_min = 0
        self.x_max = 10
        self.num_bins = 5
        self.selected_functions = []

        # Цвета для функций
        self.color_map = {
            "1": QColor(Qt.blue),
            "2": QColor(Qt.green),
            "3": QColor(Qt.red),
            "4": QColor(Qt.magenta),
            "5": QColor(Qt.darkCyan),
            "6": QColor(Qt.darkYellow),
            "7": QColor(Qt.darkBlue),
            "8": QColor(Qt.darkGreen),
            "9": QColor(Qt.darkRed)
        }

    def update_settings(self, x_min, x_max, num_bins, selected_functions):
        self.x_min = x_min
        self.x_max = x_max
        self.num_bins = num_bins
        self.selected_functions = selected_functions[:9]  # Максимум 9 функций
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        W, H = self.width(), self.height()

        # Отступы
        margin = 50
        plot_width = W - 2 * margin
        plot_height = H - 2 * margin

        # Рассчитываем ширину столбца
        bin_width = plot_width / self.num_bins

        # Подготовка данных
        data = []
        max_value = 0

        # Генерируем данные для каждого столбца
        for bin_idx in range(self.num_bins):
            bin_data = {}
            total = 0

            # Вычисляем середину интервала для текущего столбца
            x = self.x_min + (bin_idx + 0.5) * (self.x_max - self.x_min) / self.num_bins

            for func_id in self.selected_functions:
                if func_id in functions_map:
                    func = functions_map[func_id][0]
                    try:
                        value = func(x)
                        if value is not None:
                            # margin_top = 70  # Увеличиваем верхний отступvalue = abs(value)  # Берем модуль значения
                            total += value
                            bin_data[func_id] = total
                    except:
                        pass  # Игнорируем ошибки вычислений

            if total > max_value:
                max_value = total
            data.append(bin_data)

        if max_value == 0:
            max_value = 1  # Чтобы избежать деления на ноль

        # 1) Рисуем фон
        painter.fillRect(self.rect(), Qt.white)

        # 2) Оси и сетка
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        # Ось X
        painter.drawLine(margin, H - margin, W - margin, H - margin)

        # Ось Y
        painter.drawLine(margin, H - margin, margin, margin)

        # Подписи осей
        font = QFont()
        font.setPointSize(12)
        painter.setFont(font)

        # Подпись оси X
        painter.drawText(W - margin - 30, H - margin + 30, "X")

        # Подпись оси Y
        painter.drawText(margin - 30, margin + 10, "Y")

        # Деления и подписи на оси X
        for i in range(self.num_bins + 1):
            x = margin + i * bin_width
            painter.drawLine(x, H - margin, x, H - margin + 5)
            label = f"{self.x_min + i * (self.x_max - self.x_min) / self.num_bins:.1f}"
            painter.drawText(x - 15, H - margin + 20, label)

        # Деления и подписи на оси Y
        y_ticks = 5
        for i in range(y_ticks + 1):
            value = i * max_value / y_ticks
            y = H - margin - i * plot_height / y_ticks
            painter.drawLine(margin, y, margin - 5, y)
            painter.drawText(margin - 45, y + 5, f"{value:.1f}")

        for i in range(y_ticks + 1):
            value = i * max_value / y_ticks
            y = H - margin - i * plot_height / y_ticks
            painter.setPen(QPen(Qt.lightGray, 1, Qt.DashLine))  # Линии сетки
            painter.drawLine(margin, y, W - margin, y)  # Горизонтальная линия
            painter.setPen(QPen(Qt.black, 1))  # Возвращаем черный цвет для текста
            painter.drawLine(margin, y, margin - 5, y)  # Маленькая черта на оси Y
            painter.drawText(margin - 45, y + 5, f"{value:.1f}")

        # Добавляем вертикальные линии сетки
        for i in range(self.num_bins + 1):
            x = margin + i * bin_width
            painter.setPen(QPen(Qt.lightGray, 1, Qt.DashLine))  # Линии сетки
            painter.drawLine(x, H - margin, x, margin)  # Вертикальная линия
            painter.setPen(QPen(Qt.black, 1))  # Возвращаем черный цвет для текста

        # 3) Рисуем stacked гистограмму с 3D-эффектом
        bar_width = bin_width * 0.8
        bar_spacing = bin_width * 0.1
        depth = 10  # Глубина для 3D-эффекта

        for bin_idx in range(self.num_bins):
            x = margin + bin_idx * bin_width + bar_spacing
            prev_height = 0

            for func_id in self.selected_functions:
                if func_id in data[bin_idx]:
                    value = data[bin_idx][func_id]
                    height = value * plot_height / max_value

                    # Высота текущего сегмента
                    segment_height = height - prev_height

                    # Рисуем переднюю часть сегмента
                    color = self.color_map.get(func_id, QColor(Qt.gray))
                    painter.setBrush(QBrush(color, Qt.SolidPattern))
                    painter.setPen(QPen(color.darker(), 1))
                    painter.drawRect(x, H - margin - height, bar_width, segment_height)

                    # Рисуем верхнюю грань
                    top_polygon = [
                        QPointF(x, H - margin - height),
                        QPointF(x + depth, H - margin - height - depth),
                        QPointF(x + bar_width + depth, H - margin - height - depth),
                        QPointF(x + bar_width, H - margin - height),
                    ]
                    painter.setBrush(QBrush(color.lighter(), Qt.SolidPattern))
                    painter.drawPolygon(top_polygon)

                    # Рисуем боковую грань
                    side_polygon = [
                        QPointF(x + bar_width, H - margin - height),
                        QPointF(x + bar_width + depth, H - margin - height - depth),
                        QPointF(x + bar_width + depth, H - margin - prev_height - depth),
                        QPointF(x + bar_width, H - margin - prev_height),
                    ]
                    painter.setBrush(QBrush(color.darker(), Qt.SolidPattern))
                    painter.drawPolygon(side_polygon)

                    prev_height = height


class LegendWidget(QWidget):
    def __init__(self, plot_widget):
        super().__init__()
        self.plot_widget = plot_widget
        self.setMinimumSize(400, 50)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.white)

        x_pos = 10
        y_pos = self.height() // 2
        gap = 20

        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)
        fm = QFontMetrics(font)

        for func_id in self.plot_widget.selected_functions:
            if func_id in functions_map:
                color = self.plot_widget.color_map.get(func_id, QColor(Qt.gray))
                formula = functions_map[func_id][1]

                # Квадратик с цветом функции
                marker_size = 15
                painter.setBrush(color)
                painter.setPen(color)
                painter.drawRect(x_pos, y_pos - marker_size, marker_size, marker_size)

                # Формула функции
                painter.setPen(Qt.black)
                text_width = fm.horizontalAdvance(formula)
                painter.drawText(x_pos + marker_size + 5, y_pos - marker_size // 2 + fm.ascent() // 2, formula)

                x_pos += marker_size + text_width + gap


class SettingsWindow(QWidget):
    def __init__(self, plot_widget, legend_widget):
        super().__init__()
        self.setWindowTitle("Настройки гистограммы")
        layout = QVBoxLayout()

        self.plot_widget = plot_widget
        self.legend_widget = legend_widget

        # X min
        self.x_min_spin = QDoubleSpinBox()
        self.x_min_spin.setRange(-1000, 1000)
        self.x_min_spin.setValue(0)
        layout.addWidget(QLabel("X min:"))
        layout.addWidget(self.x_min_spin)

        # X max
        self.x_max_spin = QDoubleSpinBox()
        self.x_max_spin.setRange(-1000, 1000)
        self.x_max_spin.setValue(10)
        layout.addWidget(QLabel("X max:"))
        layout.addWidget(self.x_max_spin)

        # Количество столбцов
        self.num_bins_spin = QDoubleSpinBox()
        self.num_bins_spin.setRange(2, 100)
        self.num_bins_spin.setValue(5)
        layout.addWidget(QLabel("Количество столбцов (N):"))
        layout.addWidget(self.num_bins_spin)

        # Выбор функций
        self.functions_input = QLineEdit()
        self.functions_input.setPlaceholderText("Введите номера функций (1-9), например: 1 3 5")
        layout.addWidget(QLabel("Функции:"))
        layout.addWidget(self.functions_input)

        # Кнопка применения
        apply_button = QPushButton("Применить")
        apply_button.clicked.connect(self.apply_settings)
        layout.addWidget(apply_button)

        self.setLayout(layout)

    def apply_settings(self):
        selected_functions = [
            func_id.strip() for func_id in self.functions_input.text().split()
            if func_id.strip() in functions_map
        ]
        x_min = self.x_min_spin.value()
        x_max = self.x_max_spin.value()
        num_bins = int(self.num_bins_spin.value())

        self.plot_widget.update_settings(x_min, x_max, num_bins, selected_functions)
        self.legend_widget.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Гистограмма с накоплением")
        self.setGeometry(100, 100, 1000, 700)

        self.plot_widget = StackedHistogramWidget()
        self.legend_widget = LegendWidget(self.plot_widget)
        self.settings_window = SettingsWindow(self.plot_widget, self.legend_widget)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # График
        main_layout.addWidget(self.plot_widget, stretch=1)

        # Легенда
        main_layout.addWidget(self.legend_widget, stretch=0)

        # Кнопка настроек
        settings_button = QPushButton("Настройки")
        settings_button.clicked.connect(self.settings_window.show)
        main_layout.addWidget(settings_button)

        self.setCentralWidget(main_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())