from Wink.ring import Bet
from Strategy.strategy_base import Strategy


class YellowStrategy(Strategy):
    def __init__(self, entry_counter_signal, starting_trx_size, trx_size_increase_on_lose_streak, trx_size_increase_percentage) -> None:
        self.entry_counter_signal = entry_counter_signal
        self.starting_trx_size = starting_trx_size
        self.trx_size_increase_on_lose_streak = trx_size_increase_on_lose_streak
        self.trx_size_increase_percentage = trx_size_increase_percentage
        
    def ring_result(self, bet: Bet):
        pass
    
