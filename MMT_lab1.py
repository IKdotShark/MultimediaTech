from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QLineEdit, QPushButton, QMessageBox)
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt
import sys


def f1(a, b, n):
    step = 1 / n
    num_steps = int((b - a) * n) + 1
    x = [a + i * step for i in range(num_steps)]
    y = [xi for xi in x]
    return x, y, "y = x"


def f2(a, b, n):
    step = 1 / n
    num_steps = int((b - a) * n) + 1
    x = [a + i * step for i in range(num_steps)]
    y = [xi ** 2 for xi in x]
    return x, y, "y = x^2"


def f3(a, b, n):
    step = 1 / n
    num_steps = int((b - a) * n) + 1
    x = [a + i * step for i in range(num_steps) if a + i * step != 0]
    y = [1 / xi for xi in x]
    return x, y, "y = 1/x"


functions = {1: f1, 2: f2, 3: f3}


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

        all_x = [x for func_data in self.data.values() for x in func_data[0]]
        all_y = [y for func_data in self.data.values() for y in func_data[1] if y is not None]
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)

        scale_x = graph_width / (max_x - min_x) if max_x != min_x else 1
        scale_y = graph_height / (max_y - min_y) if max_y != min_y else 1

        center_x = margin - min_x * scale_x
        center_y = height - margin + min_y * scale_y

        painter.setPen(QPen(Qt.lightGray, 1, Qt.DashLine))
        step_x = (max_x - min_x) / 10 if max_x != min_x else 1
        step_y = (max_y - min_y) / 10 if max_y != min_y else 1
        for i in range(11):
            x = margin + i * (graph_width / 10)
            y = height - margin - i * (graph_height / 10)
            painter.drawLine(x, margin, x, height - margin)
            painter.drawLine(margin, y, width - margin, y)
            painter.drawText(x - 10, height - margin + 15, f"{min_x + i * step_x:.2f}")
            painter.drawText(margin - 30, y + 5, f"{min_y + i * step_y:.2f}")

        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(margin, height - margin, width - margin, height - margin)
        painter.drawLine(margin, margin, margin, height - margin)

        colors = [Qt.red, Qt.green, Qt.blue]
        for idx, (func_id, (x_vals, y_vals, label)) in enumerate(self.data.items()):
            pen = QPen(colors[idx % len(colors)])
            pen.setWidth(2)
            painter.setPen(pen)

            for x, y in zip(x_vals, y_vals):
                if y is None:
                    continue
                px = margin + (x - min_x) * scale_x
                py = height - margin - (y - min_y) * scale_y
                painter.drawRect(px - 3, py, 6, height - margin - py)

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
        self.input_n.setPlaceholderText("Введите n (деления на единицу)")
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
            if a >= b or n <= 0 or any(fid not in functions for fid in func_ids):
                raise ValueError

            data = {}
            for fid in func_ids:
                x_vals, y_vals, label = functions[fid](a, b, n)
                data[fid] = (x_vals, y_vals, label)

            self.graph_window = GraphWidget(data)
            self.graph_window.resize(800, 600)
            self.graph_window.show()

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректные данные.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())