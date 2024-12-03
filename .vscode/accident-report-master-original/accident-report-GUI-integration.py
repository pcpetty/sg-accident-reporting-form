import sys
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QGroupBox,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt


# Custom Box Class
class MyCustomBox(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        label = QLabel("My Custom Box")
        button = QPushButton("Click Me")

        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)


# Group Box Example
def create_group_box():
    group_box = QGroupBox("My Group Box")
    layout = QVBoxLayout()
    label = QLabel("Hello, World!")
    button = QPushButton("Click Me")

    layout.addWidget(label)
    layout.addWidget(button)
    group_box.setLayout(layout)
    return group_box


# Main Window with Widgets
class WidgetsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Widgets Example")

        layout = QVBoxLayout()
        widgets = [
            QCheckBox(),
            QComboBox(),
            QDateEdit(),
            QDateTimeEdit(),
            QDial(),
            QDoubleSpinBox(),
            QFontComboBox(),
            QLabel("Label Example"),
            QLineEdit(),
            QProgressBar(),
            QPushButton("Push Button"),
            QRadioButton("Radio Button"),
            QSlider(Qt.Orientation.Horizontal),
            QSpinBox(),
            QTimeEdit(),
        ]

        for widget in widgets:
            layout.addWidget(widget)

        # Add Custom Box and Group Box
        layout.addWidget(MyCustomBox())
        layout.addWidget(create_group_box())

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


# ComboBox Example
class ComboBoxWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ComboBox Example")

        combobox1 = QComboBox()
        combobox1.addItems(["One", "Two", "Three", "Four"])

        combobox2 = QComboBox()
        combobox2.addItems(["A", "B", "C", "D"])

        combobox_with_icons = QComboBox()
        icon_penguin = QIcon("animal-penguin.png")
        icon_monkey = QIcon("animal-monkey.png")
        combobox_with_icons.addItem(icon_penguin, "Linux")
        combobox_with_icons.addItem(icon_monkey, "Monkey")

        layout = QVBoxLayout()
        layout.addWidget(combobox1)
        layout.addWidget(combobox2)
        layout.addWidget(combobox_with_icons)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


# Main Application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Choose which window to display
    window = WidgetsWindow() # or ComboBoxWindow() for ComboBox example
    combo_window = ComboBoxWindow()
    window.show()
    combo_window.show()
    sys.exit(app.exec())
