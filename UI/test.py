from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout,
    QTextEdit, QDialog, QSplitter, QProgressBar
)
from PyQt6.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QThread
import sys
import time

#https://stackoverflow.com/questions/6783194/background-thread-with-qthread-in-pyqt
class Test(QWidget):
    def __init__(self) -> None:
        super().__init__()
        bot_layout = QGridLayout()
        self.setLayout(bot_layout)
        bot_layout.addWidget(QLabel('Bot'), 0, 0)
        bot_layout.addWidget(QPushButton('Bot stuff here'), 1, 0)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(1)
        self.progress_bar.setMaximum(100)

        bot_layout.addWidget(self.progress_bar)

        # 1 - create Worker and Thread inside the Form
        self.obj = Worker()  # no parent!
        self.thread = QThread()  # no parent!

        # 2 - Move the Worker object to the Thread object
        self.obj.moveToThread(self.thread)

        # 3 - Connect Worker`s Signals to Form method slots to post data.
        self.obj.intReady.connect(self.onIntReady)


        # 4 - Connect Worker Signals to the Thread slots
        self.obj.finished.connect(self.thread.quit)

        # 5 - Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.obj.procCounter)

        # * - Thread finished signal will close the app if you want!
        #self.thread.finished.connect(app.exit)

        # 6 - Start the thread
        self.thread.start()
    
    def onIntReady(self, num):
        self.progress_bar.setValue(num)



class Worker(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(int)


    @pyqtSlot()
    def procCounter(self): # A slot takes no params
        for i in range(1, 101):
            time.sleep(1/10)
            self.intReady.emit(i)

        self.finished.emit()


app = QApplication(sys.argv)
window = Test()
window.show()
sys.exit(app.exec())