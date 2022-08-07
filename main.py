import os, sys

path1 = os.path.join(os.path.dirname(__file__), 'Wink')
path2 = os.path.join(os.path.dirname(__file__), 'UI')
path3 = os.path.join(os.path.dirname(__file__), 'UI', 'UIWorker')
sys.path.append(path1)
sys.path.append(path2)
sys.path.append(path3)

from UI.ringwindow import RingWindow
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    window = RingWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()









