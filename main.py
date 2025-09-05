import sys
import os
import pygame
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QTimer

# Importamos toda la lógica de nuestro juego
from pieces.cross import CrossPiece
from pieces.straight_road import StraightPiece
from pieces.curve import CurvePiece
from pieces.t_road import TRoadPiece
from utils import snap_to_closest
from catalog import create_catalog
from file_manager import save_track, load_track

# --- Constantes del Juego ---
GAME_WIDTH, GAME_HEIGHT = 1600, 1000
CATALOG_WIDTH = 200
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)

class GameWidget(QWidget):
    """El widget que contendrá nuestro lienzo de Pygame."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(GAME_WIDTH, GAME_HEIGHT)

        # El truco para incrustar Pygame: le decimos que dibuje en este widget.
        os.environ['SDL_WINDOWID'] = str(int(self.winId()))
        pygame.init()
        self.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

        # --- Variables del estado del juego ---
        self.placed_pieces = []
        self.selected_piece = None
        self.offset_x, self.offset_y = 0, 0

    def run_game_logic(self):
        """Esta función contiene la lógica de dibujo de un fotograma de Pygame."""
        # Manejo de eventos de Pygame (lo adaptaremos más adelante)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # En lugar de salir, delegamos el cierre a la app de PyQt
                QApplication.instance().quit()
                return

        self.screen.fill(WHITE)

        show_points = self.selected_piece is not None
        for piece in self.placed_pieces:
            piece.draw(self.screen, show_snap_points=show_points)
        
        if self.selected_piece:
            self.selected_piece.draw(self.screen, show_snap_points=True)

        pygame.display.update()

class MainWindow(QMainWindow):
    """La ventana principal de nuestra aplicación híbrida."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Juego de Calles (PyQt + Pygame)")
        
        self.setup_menu()

        main_layout = QHBoxLayout()

        self.game_widget = GameWidget()
        main_layout.addWidget(self.game_widget)

        catalog_layout = QVBoxLayout()
        
        # Contenedor central y asignación de layouts
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # --- El nuevo "Bucle del Juego" ---
        # Usamos un QTimer que llamará a la lógica de Pygame cada 33 ms (~30 FPS)
        self.timer = QTimer(self)
        self.timer.setInterval(33)
        self.timer.timeout.connect(self.game_widget.run_game_logic)
        self.timer.start()

    def setup_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Archivo")

        new_action = QAction("Nuevo", self)

        open_action = QAction("Abrir", self)

        save_action = QAction("Guardar", self)

        quit_action = QAction("Cerrar", self)
        quit_action.triggered.connect(QApplication.instance().quit)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())