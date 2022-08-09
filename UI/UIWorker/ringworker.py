import time
from Wink.ring import Bet

from Wink.ringdriver import RingDriver, RingState

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


class RingWorker(QObject):
    stop = pyqtSignal()
    renew_bet_history = pyqtSignal()
    # why use object instead of specific type (ring.Bet, in this case doesn't work) 
    # https://stackoverflow.com/questions/46973384/pyqt5-wrong-conversion-of-int-object-when-using-custom-signal
    on_new_bet_result = pyqtSignal(object)
    ring_state_changed = pyqtSignal(object)

    def __init__(self) -> None:
        super().__init__()
        self.ring_driver = RingDriver()
        self.started = False

    def start_ring(self):
        self.started = True
        self.ring_driver.start()
    
    def stop_ring(self):
        self.started = False
        self.ring_driver.stop()
        self.stop.emit()
    
    @pyqtSlot()
    def ring_loop(self):
        # if current game state = can bet
            # wait for current game state = can't bet
        if self.ring_driver.GetCurrentRingState() == RingState.CAN_BET:
            self.renew_bet_history.emit()
            self.ring_driver.wait_for_ring_state(RingState.CANT_BET)
            self.ring_state_changed.emit(RingState.CANT_BET)

        # bot loop:
        while self.started:
            # wait for can bet state
            if self.ring_driver.GetCurrentRingState() == RingState.CANT_BET:
                self.ring_driver.wait_for_ring_state(RingState.CAN_BET)
                self.ring_state_changed.emit(RingState.CAN_BET)


            # get bet history to check latest result
            # send result to betting strategy, get resulting bet amount and bet multiplier
            # bet the resulting bet amount and bet multiplier
            resulting_bet : Bet = self.ring_driver.get_history()[-1]
            self.on_new_bet_result.emit(resulting_bet)

            # wait for can't bet state
            if self.ring_driver.GetCurrentRingState() == RingState.CAN_BET:
                self.ring_driver.wait_for_ring_state(RingState.CANT_BET)
                self.ring_state_changed.emit(RingState.CANT_BET)
            
            # sleep
            time.sleep(0.05) # 50 ms

        
