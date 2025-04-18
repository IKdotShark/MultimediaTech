import sys
import math
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QDoubleSpinBox, QLabel, QPushButton, QLineEdit
)
from PySide6.QtGui import QPainter, QPen, QBrush, QFont, QColor, QFontMetrics
from PySide6.QtCore import Qt, QPointF

# Категории данных для гистограммы (аналоги функций из исходного кода)
categories_data = {
    "1": {"name": "Категория A", "values": [5, 7, 3, 8, 2]},
    "2": {"name": "Категория B", "values": [3, 4, 6, 2, 5]},
    "3": {"name": "Категория C", "values": [2, 5, 4, 3, 6]},
    "4": {"name": "Категория D", "values": [4, 3, 5, 6, 3]},
    "5": {"name": "Категория E", "values": [6, 2, 7, 4, 5]},
    "6": {"name": "Категория F", "values": [3, 6, 2, 5, 4]},
    "7": {"name": "Категория G", "values": [7, 3, 5, 2, 6]},
    "8": {"name": "Категория H", "values": [2, 5, 3, 6, 4]},
    "9": {"name": "Категория I", "values": [4, 6, 3, 5, 2]}
}


class StackedHistogramWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 600)

        # Настройки аналогичны исходному коду
        self.x_min = 0
        self.x_max = 10
        self.num_bins = 5
        self.selected_categories = []

        # Цвета для категорий
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

    def update_settings(self, x_min, x_max, num_bins, selected_categories):
        self.x_min = x_min
        self.x_max = x_max
        self.num_bins = num_bins
        self.selected_categories = selected_categories[:9]  # Максимум 9 категорий
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

            for cat in self.selected_categories:
                if cat in categories_data:
                    # Используем циклическое повторение значений, если их не хватает
                    values = categories_data[cat]["values"]
                    value = values[bin_idx % len(values)]
                    total += value
                    bin_data[cat] = total

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
        painter.drawText(W - margin - 30, H - margin + 30, "Категории")

        # Подпись оси Y
        painter.drawText(margin - 30, margin + 10, "Значения")

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

        # 3) Рисуем stacked гистограмму с 3D-эффектом
        bar_width = bin_width * 0.8
        bar_spacing = bin_width * 0.1
        depth = 10  # Глубина для 3D-эффекта

        for bin_idx in range(self.num_bins):
            x = margin + bin_idx * bin_width + bar_spacing
            prev_height = 0

            for cat in self.selected_categories:
                if cat in data[bin_idx]:
                    value = data[bin_idx][cat]
                    height = value * plot_height / max_value

                    # Высота текущего сегмента
                    segment_height = height - prev_height

                    # Рисуем переднюю часть сегмента
                    color = self.color_map.get(cat, QColor(Qt.gray))
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

        for cat in self.plot_widget.selected_categories:
            if cat in categories_data:
                color = self.plot_widget.color_map.get(cat, QColor(Qt.gray))
                name = categories_data[cat]["name"]

                # Квадратик с цветом категории
                marker_size = 15
                painter.setBrush(color)
                painter.setPen(color)
                painter.drawRect(x_pos, y_pos - marker_size, marker_size, marker_size)

                # Название категории
                painter.setPen(Qt.black)
                text_width = fm.horizontalAdvance(name)
                painter.drawText(x_pos + marker_size + 5, y_pos - marker_size // 2 + fm.ascent() // 2, name)

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

        # Количество столбцов (аналог количества точек)
        self.num_bins_spin = QDoubleSpinBox()
        self.num_bins_spin.setRange(2, 100)
        self.num_bins_spin.setValue(5)
        layout.addWidget(QLabel("Количество столбцов (N):"))
        layout.addWidget(self.num_bins_spin)

        # Выбор категорий (аналог выбора функций)
        self.categories_input = QLineEdit()
        self.categories_input.setPlaceholderText("Введите номера категорий (1-9), например: 1 3 5")
        layout.addWidget(QLabel("Категории:"))
        layout.addWidget(self.categories_input)

        # Кнопка применения
        apply_button = QPushButton("Применить")
        apply_button.clicked.connect(self.apply_settings)
        layout.addWidget(apply_button)

        self.setLayout(layout)

    def apply_settings(self):
        selected_categories = [
            cat.strip() for cat in self.categories_input.text().split()
            if cat.strip() in categories_data
        ]
        x_min = self.x_min_spin.value()
        x_max = self.x_max_spin.value()
        num_bins = int(self.num_bins_spin.value())

        self.plot_widget.update_settings(x_min, x_max, num_bins, selected_categories)
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