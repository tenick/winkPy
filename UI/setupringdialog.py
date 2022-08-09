from cgitb import enable
from gc import isenabled

from PyQt6 import QtGui

from PyQt6.QtWidgets import (
    QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QDialog, QRadioButton, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal

class SetupRingDialog(QDialog):
    done_setup = pyqtSignal(int)

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
        self.bots_groupbox = QGroupBox('Choose Bot Strategy')
        bots_groupbox_layout = QHBoxLayout()
        self.bots_groupbox.setLayout(bots_groupbox_layout)

        yellow_bot_radio_btn = QRadioButton('Yellow Bot')
        yellow_bot_radio_btn.setChecked(True)

        blue_bot_radio_btn = QRadioButton('Blue Bot')
        bots_groupbox_layout.addWidget(yellow_bot_radio_btn)
        bots_groupbox_layout.addWidget(blue_bot_radio_btn)

        layout.addWidget(self.bots_groupbox)

        # finished setup widgets
        setup_label = QLabel('If done setting up wink, click the button below')

        setup_done_btn = QPushButton('Done setting up!')
        setup_done_btn.clicked.connect(self.close)

        layout.addWidget(setup_label)
        layout.addWidget(setup_done_btn)
    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        # find out which bot was selected
        selected = 0
        for i, btn in enumerate(filter(lambda qObj: isinstance(qObj, QRadioButton), self.bots_groupbox.children())):
            if btn.isChecked():
                selected = i + 1
                break
        self.done_setup.emit(selected)
        return super().closeEvent(a0)


    