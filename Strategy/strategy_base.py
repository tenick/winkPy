from Wink.ring import Bet
from PyQt6.QtCore import QObject, pyqtSignal

from abc import ABC, abstractmethod

class ABCQObjectMeta(type(ABC), type(QObject)):
    pass

class Strategy(ABC, QObject, metaclass=ABCQObjectMeta):
    win = pyqtSignal()
    lose = pyqtSignal()
    do_bet = pyqtSignal(object, object) # bet_trx_amount, bet_multiplier
    
    @abstractmethod
    def ring_result(self, bet: Bet):
        """Called whenever a new ring result is added to bet history
        
        Parameters
        ----------
        bet : Bet
            The bet multiplier of the latest result (e.g. 2x, 3x, 5x or 50x)
        """
        pass
    
