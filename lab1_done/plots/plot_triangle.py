from PySide6.QtGui import QPen, QColor, QPainter, QPolygon, QBrush
from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
import numpy as np
from sympy import Float


class PlotTriangle:
    def __init__(self, x_values, y_values, function_input, widget_width, widget_height):
        self.function_input = function_input
        self.x_values = x_values
        self.unclear_value = y_values
        self.min_x = np.min(x_values)
        self.max_x = np.max(x_values)
        self.window_start = 75
        self.window_end = 5
        self.widget_width = widget_width - self.window_start - self.window_end
        self.widget_height = widget_height - self.window_start

        self.y_values = []
        self.x_grid = [[0] * len(y_values[0]) for _ in range(len(y_values))]
        for sublist in self.unclear_value:
            cleaned_sublist = [
                float(value) if isinstance(value, (int, float, Float)) else 0
                for value in sublist
            ]
            self.y_values.append(cleaned_sublist)

        self.y_values = np.array(y_values)
        negative_mask = y_values < 0

        # Маска для положительных значений
        positive_mask = y_values > 0

        # Создаем массивы, где отрицательные и положительные значения заменяются на 0, соответственно
        self.arr_negatives = np.where(negative_mask, y_values, 0)
        self.arr_positives = np.where(positive_mask, y_values, 0)
        sum_negatives = np.sum(self.arr_negatives, axis=0)
        sum_positives = np.sum(self.arr_positives, axis=0)
        self.max_y = np.max(sum_positives)
        self.min_y = np.min(sum_negatives)


        self.max_y_without_padd = self.max_y
        self.min_y_without_padd = self.min_y
        # Добавляем отступ для визуального комфорта
        y_range = self.max_y - self.min_y
        padding = y_range * 0.3
        self.min_y -= padding
        self.max_y += padding


        if self.min_y > 0:
            self.min_y = 0 - padding
        if self.max_y < 0:
            self.max_y = 0 + padding

        self.gap_ratio = 0.15

        num_bars = len(self.x_values)

        # Количество зазоров между столбцами — на 1 меньше, чем количество столбцов
        total_gap_count = num_bars - 1

        # Найдём общую ширину одного бара и одного зазора, так чтобы всё влезло
        group_width = self.widget_width / (num_bars + total_gap_count * self.gap_ratio)

        self.parallelepiped_bar = group_width
        self.gap_size = group_width * self.gap_ratio




    def calculate_x_mapped(self):
        for j in range(len(self.x_values)):
            x_start = j * (self.parallelepiped_bar + self.gap_size)  # Добавляем зазор между группами
            for i, y_data in enumerate(self.y_values):
                adjusted_x = self.calculate_parallelipiped_x(x_start)
                self.x_grid[i][j] = adjusted_x


    def x_widget(self, x, widget_width):
        return int((x - self.min_x) / (self.max_x - self.min_x) * widget_width)

    def y_widget(self, y, widget_height):
        return int(widget_height - (y - self.min_y) / (self.max_y - self.min_y) * widget_height)

    def draw_legend(self, painter):
        bar_styles = [
            QColor(210, 0, 107),
            QColor(255, 108, 0),
            QColor(0, 158, 142),
            QColor(149, 236, 0),
            QColor(100, 149, 237),
            QColor(220, 20, 60),
            QColor(123, 104, 238),
            QColor(255, 215, 0),
            QColor(70, 130, 180)
        ]
        text_offset = 20
        legend_start_x = 0
        legend_start_y = self.widget_height + self.window_start / 2 - text_offset / 2
        box_size = 15

        gap = 5

        # Вычисляем ширину каждой легенды
        item_widths = [
            box_size + text_offset + painter.fontMetrics().horizontalAdvance(item.text()) + gap
            for item in self.function_input
        ]
        total_width = sum(item_widths) - gap  # убираем лишний пробел после последнего элемента

        # Рисуем белый фон под легенду
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawRect(legend_start_x - 5, self.widget_height , total_width + 10, self.window_start)

        # Рисуем элементы легенды в ряд
        current_x = legend_start_x
        for i, item in enumerate(self.function_input):
            color = bar_styles[i % len(bar_styles)]
            painter.setBrush(QBrush(color))
            painter.drawRect(current_x, legend_start_y, box_size, box_size)
            painter.drawText(current_x + text_offset, legend_start_y + box_size // 2 + 5, item.text())
            current_x += item_widths[i]



    def draw_grid(self, painter, style):
        pen = QPen(style.grid_color)
        pen.setWidth(style.grid_width)
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)

        # Рисуем вертикальные линии сетки
        self.calculate_x_mapped()
        transorm_grid = np.array(self.x_grid).T

        for j in range(len(self.x_values)):
            x_mapped = np.mean(transorm_grid[j][:])
            painter.drawLine(x_mapped, 0, x_mapped, self.widget_height)

            label = f"{self.x_values[j]:.2f}"  # Format the label as needed
            painter.drawText(x_mapped + 5, self.widget_height - 5, label)

        # Рисуем горизонтальные линии сетки
        y_zero_mapped = self.y_widget(0, self.widget_height)
        max_value = float(np.max([abs(self.min_y_without_padd), self.max_y_without_padd]))


        # Горизонтальные линии
        step = max_value / 4
        y = 0
        while y < float(np.max([abs(self.min_y), self.max_y])):

            y += step

            # y_mapped = int(y_zero_mapped - y / self.max_y * y_zero_mapped)
            y_mapped = self.y_widget(y, self.widget_height)
            if y == 0:
                painter.drawLine(0, y_mapped, self.window_start + self.widget_width + self.window_end, y_mapped)

                label = f" {y:.2f}"  # Format the label as needed
                painter.drawText(5, y_mapped, label)
                continue
            if y_mapped > 0 :
                painter.drawLine(0, y_mapped, self.window_start + self.widget_width + self.window_end, y_mapped)

                label = f" {y:.2f}"  # Format the label as needed
                painter.drawText(5, y_mapped, label)

            horizont_mapped = y_zero_mapped + (y_zero_mapped - y_mapped)
            if horizont_mapped < self.widget_height:

                painter.drawLine(0, horizont_mapped, self.window_start + self.widget_width + self.window_end, horizont_mapped)

                label = f"-{y:.2f}"  # Format the label as needed
                painter.drawText(5, horizont_mapped, label)


        # Рисуем ось X
        pen.setStyle(Qt.SolidLine)
        pen.setColor(style.grid_black)
        painter.setPen(pen)
        painter.drawLine(0, y_zero_mapped, self.window_end + self.window_start + self.widget_width, y_zero_mapped)


    def calculate_parallelipiped_x(self, x_start):
        x_parallelipiped = self.window_start + x_start
        return x_parallelipiped

    def draw_parallelepiped(self, painter, adjusted_x, y_zero_mapped, y_data_value, piramide_bar):
        y = self.y_widget(y_data_value, self.widget_height)


        width = piramide_bar
        depth = piramide_bar // 8  # Глубина для создания 3D эффекта
        height = abs(self.y_zero_mapped - y)


        # Определяем координаты для передней грани
        if y_data_value >= 0:
            # Если значение положительное, рисуем выше оси OX
            front_top_left = QPoint(adjusted_x - width // 2, y_zero_mapped - height)
            front_top_right = QPoint(adjusted_x + width // 2, y_zero_mapped - height)
            front_bottom_left = QPoint(adjusted_x - width // 2, y_zero_mapped)
            front_bottom_right = QPoint(adjusted_x + width // 2, y_zero_mapped)

            # Определяем координаты для задней грани
            back_top_left = QPoint(adjusted_x - width // 2 + depth, y_zero_mapped - height - depth)
            back_top_right = QPoint(adjusted_x + width // 2 + depth, y_zero_mapped - height - depth)
            back_bottom_left = QPoint(adjusted_x - width // 2 + depth, y_zero_mapped - depth)
            back_bottom_right = QPoint(adjusted_x + width // 2 + depth, y_zero_mapped - depth)
        else:
            # Если значение отрицательное, рисуем ниже оси OX
            front_top_left = QPoint(adjusted_x - width // 2, y_zero_mapped)
            front_top_right = QPoint(adjusted_x + width // 2, y_zero_mapped)
            front_bottom_left = QPoint(adjusted_x - width // 2, y_zero_mapped + height)
            front_bottom_right = QPoint(adjusted_x + width // 2, y_zero_mapped + height)

            # Определяем координаты для задней грани
            back_top_left = QPoint(adjusted_x - width // 2 + depth, y_zero_mapped - depth)
            back_top_right = QPoint(adjusted_x + width // 2 + depth, y_zero_mapped - depth)
            back_bottom_left = QPoint(adjusted_x - width // 2 + depth, y_zero_mapped + height - depth)
            back_bottom_right = QPoint(adjusted_x + width // 2 + depth, y_zero_mapped + height - depth)

        # Рисуем переднюю грань
        painter.drawPolygon(QPolygon([
            front_top_left,
            front_top_right,
            front_bottom_right,
            front_bottom_left
        ]))

        # Рисуем верхнюю грань
        painter.drawPolygon(QPolygon([
            front_top_left,
            front_top_right,
            back_top_right,
            back_top_left
        ]))

        # Рисуем боковую грань (правую)
        painter.drawPolygon(QPolygon([
            front_top_right,
            front_bottom_right,
            back_bottom_right,
            back_top_right
        ]))

    def draw_plot(self, painter):
        bar_styles = [
            QColor(210, 0, 107),
            QColor(255, 108, 0),
            QColor(0, 158, 142),
            QColor(149, 236, 0),
            QColor(100, 149, 237),
            QColor(220, 20, 60),
            QColor(123, 104, 238),
            QColor(255, 215, 0),
            QColor(70, 130, 180)
        ]

        
        self.y_zero_mapped = self.y_widget(0, self.widget_height)

        for j in range(len(self.x_values)):
            x_start = j * (self.parallelepiped_bar + self.gap_size)
            column = self.y_values[:, j]

            # Разделяем индексы на отрицательные и положительные
            neg_indices = np.where(column < 0)[0]
            pos_indices = np.where(column >= 0)[0]

            # Отрицательные значения: от самых больших по модулю к самым маленьким
            neg_sorted_indices = np.sort(neg_indices)[::-1]

            # Положительные значения: от самых маленьких к самым большим
            pos_sorted_indices = np.sort(pos_indices)
            
            print(neg_sorted_indices, pos_sorted_indices)
            # Сначала рисуем отрицательные, потом положительные
            for i in np.concatenate((neg_sorted_indices, pos_sorted_indices)):
                y_data = self.y_values[i, j]  # Используем y_array с индексами
                bar_color = bar_styles[i % len(bar_styles)]
                painter.setBrush(bar_color)

                adjusted_x = self.calculate_parallelipiped_x(x_start)

                if y_data < 0:
                    # Берём накопление до текущего индекса среди отрицательных
                    arr = self.arr_negatives.T[j]
                    neg_stack = np.sum(arr[neg_sorted_indices[neg_sorted_indices < i]])  # Накопление среди отрицательных
                    y_zero_mapped = self.y_widget(neg_stack, self.widget_height)
                else:
                    arr = self.arr_positives.T[j]
                    # Накопление всех значений до текущего индекса
                    pos_stack = np.sum(arr[pos_sorted_indices[:pos_sorted_indices.tolist().index(i)]])
                    y_zero_mapped = self.y_widget(pos_stack, self.widget_height)

                self.draw_parallelepiped(painter, adjusted_x, y_zero_mapped, y_data, self.parallelepiped_bar)