from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout,
    QTextEdit, QDialog, QSplitter, QStatusBar
)
from PyQt6.QtCore import Qt
import sys

class YellowBotWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        bot_layout = QGridLayout()
        self.setLayout(bot_layout)
        bot_layout.addWidget(QLabel('Bot'), 0, 0)
        bot_layout.addWidget(QPushButton('Bot stuff here'), 1, 0)
