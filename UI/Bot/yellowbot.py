from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout,
    QTextEdit, QSplitter, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
import sys

from Strategy import YellowStrategy

class YellowBotWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.__init_UI()
        

    def __init_UI(self):
        # main bot layout
        self.strategy = YellowStrategy(150, 10, 30, 100)
        self.bot_layout = QVBoxLayout()
        self.setLayout(self.bot_layout)

        # Bot configuration group
        self.bot_config_groupbox = QGroupBox('Yellow Bot Configuration')
        bot_config_groupbox_layout = QGridLayout()
        self.bot_config_groupbox.setLayout(bot_config_groupbox_layout)

        self.entry_counter_signal_lbl = QLabel('Entry Counter Signal:')
        self.entry_counter_signal_txtBox = QLineEdit()
        self.entry_counter_signal_txtBox.setValidator(QIntValidator())

        self.starting_trx_size_lbl = QLabel('Starting TRX Size:')
        self.starting_trx_size_txtBox = QLineEdit()
        self.starting_trx_size_txtBox.setValidator(QIntValidator())

        self.trx_size_increase_on_lose_streak_lbl = QLabel('Increase TRX Size On Amount of Loss:')
        self.trx_size_increase_on_lose_streak_txtBox = QLineEdit()
        self.trx_size_increase_on_lose_streak_txtBox.setValidator(QIntValidator())

        self.trx_size_increase_percentage_lbl = QLabel('Increase TRX Size by Percentage of:')
        self.trx_size_increase_percentage_txtBox = QLineEdit()
        self.trx_size_increase_percentage_txtBox.setValidator(QIntValidator())

        bot_config_groupbox_layout.addWidget(self.entry_counter_signal_lbl, 0, 0)
        bot_config_groupbox_layout.addWidget(self.entry_counter_signal_txtBox, 0, 1)

        bot_config_groupbox_layout.addWidget(self.starting_trx_size_lbl, 1, 0)
        bot_config_groupbox_layout.addWidget(self.starting_trx_size_txtBox, 1, 1)

        bot_config_groupbox_layout.addWidget(self.trx_size_increase_on_lose_streak_lbl, 2, 0)
        bot_config_groupbox_layout.addWidget(self.trx_size_increase_on_lose_streak_txtBox, 2, 1)

        bot_config_groupbox_layout.addWidget(self.trx_size_increase_percentage_lbl, 3, 0)
        bot_config_groupbox_layout.addWidget(self.trx_size_increase_percentage_txtBox, 3, 1)

        self.bot_layout.addWidget(self.bot_config_groupbox)

        # Bot status group
        self.bot_status_groupbox = QGroupBox('Yellow Bot Status')
        bot_status_groupbox_layout = QGridLayout()
        self.bot_status_groupbox.setLayout(bot_status_groupbox_layout)

        self.current_counter_lbl = QLabel('Current Counter:')
        self.current_counter_value_lbl = QLabel('0')

        self.current_trx_size_lbl = QLabel('Current TRX Size:')
        self.current_trx_size_value_lbl = QLabel('10')

        self.current_lose_streak_lbl = QLabel('Current Lose Streak:')
        self.current_lose_streak_value_lbl = QLabel('0')

        bot_status_groupbox_layout.addWidget(self.current_counter_lbl, 0, 0)
        bot_status_groupbox_layout.addWidget(self.current_counter_value_lbl, 0, 1)

        bot_status_groupbox_layout.addWidget(self.current_trx_size_lbl, 1, 0)
        bot_status_groupbox_layout.addWidget(self.current_trx_size_value_lbl, 1, 1)

        bot_status_groupbox_layout.addWidget(self.current_lose_streak_lbl, 2, 0)
        bot_status_groupbox_layout.addWidget(self.current_lose_streak_value_lbl, 2, 1)

        self.bot_layout.addWidget(self.bot_status_groupbox)
