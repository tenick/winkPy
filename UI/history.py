from typing import Iterable
from collections import deque

from Wink import ring as Ring

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout
)
from PyQt6.QtCore import Qt



class BetHistoryWidget(QWidget):
    def __init__(self, bet_history: Iterable[Ring.Bet] = []) -> None:
        super().__init__()
        self.history_limit: int = 25
        self.bet_history: deque = deque[Ring.Bet](bet_history)
        self.layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # initial draw
        self.redraw()
        
    def __adjust_history_to_limit(self):
        while len(self.bet_history) > self.history_limit:
            self.bet_history.popleft()

    def add_new_bet_to_history(self, bet: Ring.Bet):
        self.__adjust_history_to_limit()
        
        self.bet_history.append(bet)

    def clear_history(self):
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().deleteLater()

    def redraw(self):
        self.__adjust_history_to_limit()

        self.clear_history()

        for bet in self.bet_history:
            hist_label = QLabel()
            hist_label.setStyleSheet(f'background-color: {Ring.BetToColor(bet)}; width: 100px; border-radius: 5px')
            self.layout.addWidget(hist_label)
