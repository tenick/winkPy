from Wink.ring import Bet
import UI
from UIWorker.ringworker import RingWorker

from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QSplitter, QStatusBar
)
from PyQt6.QtCore import QThread, pyqtSlot

from Wink.ringdriver import RingState


class RingWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.__init_UI()
        self.resize(700, 500)
        self.setWindowTitle('Wink Bot')
        self.setStyleSheet('''
            QWidget { 
                font-family: "Lucida Console", "Courier New", monospace; 
                font-size: 15px;
                color: white;
                background-color: #121229;
            } 
            QPushButton::hover { 
                background-color: #BBB; 
                color: #222; 
            }
            QPushButton { 
                background-color: #333; 
                color: white; 
                padding: 10px 20px; 
                font-weight: 600;
            }
        ''')
        # background workers
        self.ring_worker = RingWorker()  # no parent!
        self.ring_worker_thread = QThread()  # no parent!

        self.ring_worker.moveToThread(self.ring_worker_thread)

        self.ring_worker.stop.connect(self.ring_worker_thread.quit)
        self.ring_worker.renew_bet_history.connect(self.__renew_bet_history)
        self.ring_worker.add_bet_to_history.connect(self.__add_bet_to_history)
        self.ring_worker.ring_state_changed.connect(self.__ring_state_changed)

        self.ring_worker_thread.started.connect(self.ring_worker.ring_loop)
        
    
    def __init_UI(self):
        # main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        # start ring button
        self.start_btn = QPushButton('Start Ring')
        self.start_btn.clicked.connect(self.start)
        main_layout.addWidget(self.start_btn)

        # bot widget
        self.bot_widget = UI.YellowBotWidget()

        # history widget
        self.history_widget = UI.BetHistoryWidget([
            Bet.X2, Bet.X3, Bet.X5, Bet.X50
        ])
        self.history_widget.redraw()

        # horizontal splitter between bot and history cell
        splitter = QSplitter()
        splitter.addWidget(self.bot_widget)
        splitter.addWidget(self.history_widget)
        splitter.setStyleSheet('QSplitter::handle { background-color:#555; }')

        main_layout.addWidget(splitter)

        # status bar
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet('background-color: #DDD; color: black; font-weight: 800')
        self.status_bar.showMessage('bot not running')
        self.status_bar.setMaximumHeight(30)
        main_layout.addWidget(self.status_bar)

        # start bot dialog
        self.setup_bot_dialog = UI.SetupBotDialog(self)
        self.setup_bot_dialog.done_setup.connect(self.__done_bot_setup)

    def start(self):
        if not self.ring_worker.started:
            self.ring_worker.start_ring()

            self.start_btn.setText('Stop Ring')
            self.status_bar.showMessage('Ring Started')

            # run set up bot dialog
            # setup consists of logging into TRX account, closing disclaimer or anything that covers screen that can cause ElementNotClickable error
            self.setup_bot_dialog.exec()
        else:
            self.ring_worker.stop_ring()

            self.status_bar.showMessage('Ring and Bot Stopped')
            self.start_btn.setText('Start Ring')

    @pyqtSlot()
    def __done_bot_setup(self):
        self.ring_worker.ring_driver.init_ring()

        self.status_bar.showMessage('Bot Started')
        self.__renew_bet_history()
        
        self.ring_worker_thread.start()

    @pyqtSlot()
    def __renew_bet_history(self):
        new_hist = self.ring_worker.ring_driver.get_history()
        self.history_widget.bet_history = new_hist
        self.history_widget.redraw()

    @pyqtSlot(Bet)
    def __add_bet_to_history(self, bet: Bet):
        self.history_widget.add_new_bet_to_history(bet)
        self.history_widget.redraw()
    
    @pyqtSlot(RingState)
    def __ring_state_changed(self, state: RingState):
        match state:
            case RingState.CAN_BET:
                self.status_bar.showMessage('Bot Betting Phase')
            case RingState.CANT_BET:
                self.status_bar.showMessage('Bot Waiting For Betting Phase...')

        


