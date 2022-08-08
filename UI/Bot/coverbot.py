from ctypes import alignment
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QLineEdit, QVBoxLayout, QHBoxLayout,
)
from PyQt6.QtCore import Qt
import sys

class CoverBotWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        cover_layout = QVBoxLayout()
        cover_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(cover_layout)

        self.center_label = QLabel()
        self.center_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.center_label.setText('Wink Bot')
        self.center_label.setStyleSheet('font-size: 30px; font-weight: 800')
        
        cover_layout.addWidget(self.center_label)
