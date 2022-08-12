from curses.ascii import isdigit
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout,
    QTextEdit, QSplitter, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QIntValidator
import sys

from Strategy import YellowStrategy
from Strategy.strategy_base import Strategy

class YellowBotWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # add the corresponding strategy for this bot widget
        self.strategy: YellowStrategy = YellowStrategy(5, 10, 30, 100)
        self.__init_UI()

        
        # listen to strategy signals to update UI accordingly
        self.strategy.on_new_counter.connect(self.__on_new_counter)
        self.strategy.on_new_trx_size.connect(self.__on_new_trx_size)
        self.strategy.on_win.connect(self.__on_win)
        self.strategy.on_lose.connect(self.__on_lose)


    def __init_UI(self):
        # main bot layout
        self.bot_layout = QVBoxLayout()
        self.setLayout(self.bot_layout)

        # Bot configuration group
        self.bot_config_groupbox = QGroupBox('Yellow Bot Configuration')
        bot_config_groupbox_layout = QGridLayout()
        self.bot_config_groupbox.setLayout(bot_config_groupbox_layout)

        self.entry_counter_signal_lbl = QLabel('Entry Counter Signal:')
        self.entry_counter_signal_txtBox = QLineEdit()
        self.entry_counter_signal_txtBox.setText(str(self.strategy.entry_counter_signal))
        self.entry_counter_signal_txtBox.setValidator(QIntValidator())

        self.starting_trx_size_lbl = QLabel('Starting TRX Size:')
        self.starting_trx_size_txtBox = QLineEdit()
        self.starting_trx_size_txtBox.setText(str(self.strategy.starting_trx_size))
        self.starting_trx_size_txtBox.setValidator(QIntValidator())

        self.trx_size_increase_on_lose_streak_lbl = QLabel('Increase TRX Size On Amount of Loss:')
        self.trx_size_increase_on_lose_streak_txtBox = QLineEdit()
        self.trx_size_increase_on_lose_streak_txtBox.setText(str(self.strategy.trx_size_increase_on_lose_streak))
        self.trx_size_increase_on_lose_streak_txtBox.setValidator(QIntValidator())

        self.trx_size_increase_percentage_lbl = QLabel('Increase TRX Size by Percentage of:')
        self.trx_size_increase_percentage_txtBox = QLineEdit()
        self.trx_size_increase_percentage_txtBox.setText(str(self.strategy.trx_size_increase_percentage))
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

    def update_strategy_inputs_with_UI_values(self):
        if self.entry_counter_signal_txtBox.text().isdigit():
            self.strategy.entry_counter_signal = int(self.entry_counter_signal_txtBox.text())
        else:
            self.entry_counter_signal_txtBox.setText(str(self.strategy.entry_counter_signal))
        
        if self.starting_trx_size_txtBox.text().isdigit():
            self.strategy.starting_trx_size = int(self.starting_trx_size_txtBox.text())
        else:
            self.starting_trx_size_txtBox.setText(str(self.strategy.starting_trx_size))

        if self.trx_size_increase_on_lose_streak_txtBox.text().isdigit():
            self.strategy.trx_size_increase_on_lose_streak = int(self.trx_size_increase_on_lose_streak_txtBox.text())
        else:
            self.trx_size_increase_on_lose_streak_txtBox.setText(str(self.strategy.trx_size_increase_on_lose_streak))

        if self.trx_size_increase_percentage_txtBox.text().isdigit():
            self.strategy.trx_size_increase_percentage = int(self.trx_size_increase_percentage_txtBox.text())
        else:
            self.trx_size_increase_percentage_txtBox.setText(str(self.strategy.trx_size_increase_percentage))

    @pyqtSlot(int)
    def __on_new_counter(self, counter):
        self.current_counter_value_lbl.setText(str(counter))

    @pyqtSlot(int)
    def __on_new_trx_size(self, trx_size):
        self.current_trx_size_value_lbl.setText(str(trx_size))

    @pyqtSlot()
    def __on_win(self):
        self.current_lose_streak_value_lbl.setText("0")

    @pyqtSlot()
    def __on_lose(self):
        self.current_lose_streak_value_lbl.setText(str(int(self.current_lose_streak_value_lbl.text()) + 1))