from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QLabel, QLineEdit, QPushButton, QMessageBox)
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt, QPointF
import sys
import math

# Определение функций
def f1(a, b, n):
    x = [a + i * (b - a) / (n - 1) for i in range(n)]
    y = [xi for xi in x]
    return x, y, "Простая функция: y = x"

def f2(a, b, n):
    x = [a + i * (b - a) / (n - 1) for i in range(n)]
    y = [xi ** 2 for xi in x]
    return x, y, "Сложная функция: y = x^2"

def f3(a, b, n):
    x = [a + i * (b - a) / (n - 1) for i in range(n)]
    y = [1 / xi if xi != 0 else 0 for xi in x]
    return x, y, "Функция с точкой разрыва: y = 1/x"

functions = {
    1: f1,
    2: f2,
    3: f3
}

class GraphWidget(QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width, height = self.width(), self.height()
        margin = 40
        graph_width = width - 2 * margin
        graph_height = height - 2 * margin

        center_x = width // 2
        center_y = height // 2
        grid_step = 40

        # Определение глобальных границ для всех графиков
        all_x = [x for func_data in self.data.values() for x in func_data[0]]
        all_y = [y for func_data in self.data.values() for y in func_data[1]]
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)

        # Рисуем сетку и подписи осей
        pen = QPen(Qt.lightGray, 1, Qt.DashLine)
        painter.setPen(pen)
        for i in range(-10, 11):
            x = center_x + i * grid_step
            y = center_y - i * grid_step

            painter.drawLine(x, 0, x, height)  # Вертикальные линии
            painter.drawLine(0, y, width, y)  # Горизонтальные линии

            if i != 0:
                painter.drawText(x - 10, center_y + 20, str(i))  # Подписи по оси X
                painter.drawText(center_x + 10, y + 5, str(-i))  # Подписи по оси Y

        # Оси координат
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(0, center_y, width, center_y)  # Ось X
        painter.drawLine(center_x, 0, center_x, height)  # Ось Y

        colors = [Qt.red, Qt.green, Qt.blue]
        for idx, (func_id, (x_vals, y_vals, label)) in enumerate(self.data.items()):
            pen = QPen(colors[idx % len(colors)])
            pen.setWidth(2)
            painter.setPen(pen)

            prev_point = None
            for x, y in zip(x_vals, y_vals):
                px = center_x + x * grid_step
                py = center_y - y * grid_step

                if prev_point and abs(prev_point.y() - py) < height:  # Проверка разрыва
                    painter.drawLine(prev_point, QPointF(px, py))
                prev_point = QPointF(px, py)

            painter.drawText(margin, margin + 20 * idx, label)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("График функций")

        layout = QVBoxLayout()

        self.input_a = QLineEdit()
        self.input_a.setPlaceholderText("Введите a")
        layout.addWidget(self.input_a)

        self.input_b = QLineEdit()
        self.input_b.setPlaceholderText("Введите b")
        layout.addWidget(self.input_b)

        self.input_n = QLineEdit()
        self.input_n.setPlaceholderText("Введите n (кол-во точек)")
        layout.addWidget(self.input_n)

        self.input_funcs = QLineEdit()
        self.input_funcs.setPlaceholderText("Введите номера функций (например: 1,2)")
        layout.addWidget(self.input_funcs)

        self.plot_button = QPushButton("Построить график")
        self.plot_button.clicked.connect(self.plot_graph)
        layout.addWidget(self.plot_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def plot_graph(self):
        try:
            a = float(self.input_a.text())
            b = float(self.input_b.text())
            n = int(self.input_n.text())
            func_ids = [int(f.strip()) for f in self.input_funcs.text().split(',') if f.strip().isdigit()]
            if a >= b or n <= 1 or any(fid not in functions for fid in func_ids):
                raise ValueError

            data = {}
            for fid in func_ids:
                x_vals, y_vals, label = functions[fid](a, b, n)
                data[fid] = (x_vals, y_vals, label)

            self.graph_window = GraphWidget(data)
            self.graph_window.resize(800, 600)
            self.graph_window.show()

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректные данные.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
