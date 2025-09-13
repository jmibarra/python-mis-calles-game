# main.py

import sys
from PyQt6.QtWidgets import QApplication
from mis_calles_game.ui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())