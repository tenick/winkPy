from math import ceil
from Wink.ring import Bet
from Strategy.strategy_base import Strategy

from PyQt6.QtCore import pyqtSignal


class YellowStrategy(Strategy):
    # signals to update bot UI statuses
    on_new_counter = pyqtSignal(int)
    on_new_trx_size = pyqtSignal(int)
    
    def __init__(self, entry_counter_signal: int, starting_trx_size: int, trx_size_increase_on_lose_streak: int, trx_size_increase_percentage: int) -> None:
        super().__init__()
        # strategy inputs
        self.entry_counter_signal = entry_counter_signal
        self.starting_trx_size = starting_trx_size
        self.trx_size_increase_on_lose_streak = trx_size_increase_on_lose_streak
        self.trx_size_increase_percentage = trx_size_increase_percentage

        # status variables
        self.current_counter = 0
        self.current_trx_size = starting_trx_size
        self.current_lose_streak = 0
        
    def ring_result(self, bet: Bet):
        # update counter
        if bet == Bet.X50:
            # check if currently betting, reaching here means the bet won
            if self.current_counter >= self.entry_counter_signal:
                self.on_win.emit()

            # reset inputs
            self.current_counter = 0
            self.current_trx_size = self.starting_trx_size
            self.on_new_trx_size.emit(self.current_trx_size)
            self.current_lose_streak = 0

        else:
            # check if currently betting, reaching here means the bet lost
            if self.current_counter >= self.entry_counter_signal:
                self.current_lose_streak = self.current_lose_streak + 1
                self.on_lose.emit()

                # check if have to increase trx size
                if self.current_lose_streak % self.trx_size_increase_on_lose_streak == 0:
                    # calculate new trx size
                    multiplier = 1 + self.trx_size_increase_percentage / 100
                    self.current_trx_size = ceil(self.current_trx_size * multiplier)

                    self.on_new_trx_size.emit(self.current_trx_size)
                
            self.current_counter = self.current_counter + 1

        self.on_new_counter.emit(self.current_counter)


        # check if have to bet
        if self.current_counter >= self.entry_counter_signal:
            self.do_bet.emit(self.current_trx_size, Bet.X50)

        
    
