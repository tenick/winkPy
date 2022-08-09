from Wink.ring import Bet
import UI
from UIWorker.ringworker import RingWorker

from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QSplitter, QStatusBar, QStackedWidget
)
from PyQt6.QtCore import QThread, pyqtSlot

from Wink.ringdriver import RingState


class RingWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.__init_UI()
        self.resize(800, 500)
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
        self.ring_worker.on_new_bet_result.connect(self.__on_new_bet_result)
        self.ring_worker.ring_state_changed.connect(self.__ring_state_changed)

        self.ring_worker_thread.started.connect(self.ring_worker.ring_loop)
        
    
    def __init_UI(self):
        # main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        # buttons stack (buttons shown per state change)
        self.button_stack = QStackedWidget()
        self.button_stack.setMinimumHeight(50)
        self.button_stack.setMaximumHeight(50)

        self.start_ring_btn = QPushButton('Start Ring')
        self.start_ring_btn.clicked.connect(self.start_ring)

        self.start_bot_btn = QPushButton('Start Bot')
        self.start_bot_btn.clicked.connect(self.start_bot)

        self.stop_btn = QPushButton('Stop')
        self.stop_btn.clicked.connect(self.stop)
        
        self.button_stack.addWidget(self.start_ring_btn)
        self.button_stack.addWidget(self.start_bot_btn)
        self.button_stack.addWidget(self.stop_btn)
        main_layout.addWidget(self.button_stack)

        # bot stack widget
        self.bot_stack = QStackedWidget()

        self.bot_stack_cover = UI.Bot.CoverBotWidget()
        self.yellow_bot_widget = UI.Bot.YellowBotWidget()
        self.blue_bot_widget = UI.Bot.BlueBotWidget()
        self.bot_stack.addWidget(self.bot_stack_cover)
        self.bot_stack.addWidget(self.yellow_bot_widget)
        self.bot_stack.addWidget(self.blue_bot_widget)

        # history widget
        self.history_widget = UI.BetHistoryWidget([
            Bet.X2, Bet.X3, Bet.X5, Bet.X50
        ])
        self.history_widget.redraw()

        # horizontal splitter between bot and history cell
        self.bot_and_history_splitter = QSplitter()
        self.bot_and_history_splitter.addWidget(self.bot_stack)
        self.bot_and_history_splitter.addWidget(self.history_widget)
        self.bot_and_history_splitter.setStyleSheet('QSplitter::handle { background-color:#555; }')

        main_layout.addWidget(self.bot_and_history_splitter)

        # status bar
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet('background-color: #DDD; color: black; font-weight: 800')
        self.status_bar.showMessage('bot not running')
        self.status_bar.setMaximumHeight(30)
        main_layout.addWidget(self.status_bar)

        # start bot dialog
        self.setup_ring_dialog = UI.SetupRingDialog(self)
        self.setup_ring_dialog.done_setup.connect(self.__done_ring_setup)

    @pyqtSlot()
    def start_ring(self):
        self.ring_worker.start_ring()

        self.status_bar.showMessage('Ring Started')

        # run set up bot dialog
        # setup consists of logging into TRX account, closing disclaimer or anything that covers screen that can cause ElementNotClickable error
        self.setup_ring_dialog.exec()

        self.button_stack.setCurrentIndex(1)
    
    @pyqtSlot()
    def start_bot(self):
        self.button_stack.setCurrentIndex(2)

        self.__renew_bet_history()
        
        self.ring_worker_thread.start()
    
    @pyqtSlot()
    def stop(self):
        self.ring_worker.stop_ring()

        self.button_stack.setCurrentIndex(0)

        self.status_bar.showMessage('Ring and Bot Stopped')

    @pyqtSlot(int)
    def __done_ring_setup(self, selected_bot_index):
        self.bot_stack.setCurrentIndex(selected_bot_index)

        # start bot button styling based on selected bot
        match selected_bot_index:
            case 1:
                self.start_bot_btn.setText('Start Yellow Bot')
                self.start_bot_btn.setStyleSheet('''
                    QPushButton::hover { background-color: #ffeec2; }
                    QPushButton { background-color: #fbb709; color: black;}
                ''')
            case 2:
                self.start_bot_btn.setText('Start Blue Bot')
                self.start_bot_btn.setStyleSheet('''
                    QPushButton::hover { background-color: #bde3ff; }
                    QPushButton { background-color: #0094ff; color: black;}
                ''')

        self.ring_worker.ring_driver.init_ring()

        self.status_bar.showMessage('Ring Started')

    @pyqtSlot()
    def __renew_bet_history(self):
        new_hist = self.ring_worker.ring_driver.get_history()
        self.history_widget.bet_history = new_hist
        self.history_widget.redraw()

    @pyqtSlot(Bet)
    def __on_new_bet_result(self, bet: Bet):
        self.history_widget.add_new_bet_to_history(bet)
        self.history_widget.redraw()
    
    @pyqtSlot(RingState)
    def __ring_state_changed(self, state: RingState):
        match state:
            case RingState.CAN_BET:
                self.status_bar.showMessage('Bot Betting Phase')
            case RingState.CANT_BET:
                self.status_bar.showMessage('Bot Waiting For Betting Phase...')

        


