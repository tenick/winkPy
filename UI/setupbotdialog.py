from cgitb import enable
from gc import isenabled

from PyQt6 import QtGui

from PyQt6.QtWidgets import (
    QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QDialog, QRadioButton, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal

class SetupBotDialog(QDialog):
    done_setup = pyqtSignal()

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.resize(100, 100)
        self.setWindowTitle('Wink setup before proceeding')
        # enable custom window hint
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.CustomizeWindowHint)

        # disable (but not hide) close button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        # radio button group
        bots_groupbox = QGroupBox('Choose Bot Strategy')
        bots_groupbox_layout = QHBoxLayout()
        bots_groupbox.setLayout(bots_groupbox_layout)

        yellow_bot_radio_btn = QRadioButton('Yellow Bot')
        yellow_bot_radio_btn.setChecked(True)

        blue_bot_radio_btn = QRadioButton('Blue Bot')
        blue_bot_radio_btn.setDisabled(True)
        bots_groupbox_layout.addWidget(yellow_bot_radio_btn)
        bots_groupbox_layout.addWidget(blue_bot_radio_btn)

        layout.addWidget(bots_groupbox)

        # finished setup widgets
        setup_label = QLabel('If done setting up wink, click the button below')

        setup_done_btn = QPushButton('Done setting up!')
        setup_done_btn.clicked.connect(self.close)

        layout.addWidget(setup_label)
        layout.addWidget(setup_done_btn)
    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.done_setup.emit()
        return super().closeEvent(a0)


    