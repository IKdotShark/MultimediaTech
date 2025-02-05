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

        painter.setPen(QPen(Qt.lightGray, 1, Qt.DashLine))
        step_x = graph_width / 10
        step_y = graph_height / 10
        for i in range(11):
            x = margin + i * step_x
            painter.drawLine(x, margin, x, height - margin)
            y = margin + i * step_y
            painter.drawLine(margin, y, width - margin, y)

        painter.setPen(QPen(Qt.black, 2))
        x_axis_y = margin + graph_height / 2
        y_axis_x = margin + graph_width / 2
        painter.drawLine(margin, x_axis_y, width - margin, x_axis_y)
        painter.drawLine(y_axis_x, margin, y_axis_x, height - margin)

        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)

        colors = [Qt.red, Qt.green, Qt.blue]
        for idx, (func_id, (x_vals, y_vals, label)) in enumerate(self.data.items()):
            pen = QPen(colors[idx % len(colors)])
            pen.setWidth(2)
            painter.setPen(pen)

            min_x, max_x = min(x_vals), max(x_vals)
            min_y, max_y = min(y_vals), max(y_vals)

            prev_point = None
            for x, y in zip(x_vals, y_vals):
                px = margin + ((x - min_x) / (max_x - min_x)) * graph_width if max_x != min_x else margin
                py = margin + graph_height - ((y - min_y) / (max_y - min_y)) * graph_height if max_y != min_y else margin
                if prev_point:
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
