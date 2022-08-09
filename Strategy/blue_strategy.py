from Wink.ring import Bet
from Strategy.strategy_base import Strategy
from PyQt6.QtCore import pyqtSignal


class BlueStrategy(Strategy):

    def ring_result(self, bet: Bet):
        raise NotImplementedError("Blue strategy not yet implemented!")
    
