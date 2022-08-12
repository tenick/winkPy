import os, sys

path1 = os.path.join(os.path.dirname(__file__), 'Strategy')
path2 = os.path.join(os.path.dirname(__file__), 'Wink')
path3 = os.path.join(os.path.dirname(__file__), 'UI')
path4 = os.path.join(os.path.dirname(__file__), 'UI', 'UIWorker')
path5 = os.path.join(os.path.dirname(__file__), 'UI', 'Bot')
sys.path.append(path1)
sys.path.append(path2)
sys.path.append(path3)
sys.path.append(path4)
sys.path.append(path5)

from UI.mainwindow import MainWindow
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
