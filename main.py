import sys
import os
import pygame
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame)
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtCore import QTimer, QSize

# Importamos toda la lógica de nuestro juego
from pieces.cross import CrossPiece
from pieces.straight_road import StraightPiece
from pieces.curve import CurvePiece
from pieces.t_road import TRoadPiece
from utils import snap_to_closest
from file_manager import save_track, load_track

# --- Constantes del Juego ---
GAME_WIDTH, GAME_HEIGHT = 1600, 1000
CATALOG_WIDTH = 200
WHITE = (255, 255, 255)
PIECE_SIZE = 100 # Tamaño estándar de las piezas

class GameWidget(QWidget):
    """El widget que contiene nuestro lienzo de Pygame y su lógica."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(GAME_WIDTH, GAME_HEIGHT)

        # Incrustamos Pygame en este widget
        os.environ['SDL_WINDOWID'] = str(int(self.winId()))
        pygame.init()
        self.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

        # --- Estado del Juego ---
        self.placed_pieces = []
        self.selected_piece = None
        self.offset_x, self.offset_y = 0, 0
    
    def run_game_frame(self):
        """Dibuja un único fotograma del juego."""
        self.screen.fill(WHITE)
        
        # Muestra los puntos de encastre de todas las piezas si se está arrastrando una
        show_points = self.selected_piece is not None
        for piece in self.placed_pieces:
            piece.draw(self.screen, show_snap_points=show_points)
        
        if self.selected_piece:
            self.selected_piece.draw(self.screen, show_snap_points=True)

        pygame.display.update()

    # --- Métodos para manejar la Interacción del Mouse ---
    # PyQt captura los eventos del mouse sobre este widget, y nosotros los usamos
    # para controlar la lógica de Pygame.

    def mousePressEvent(self, event):
        mouse_x, mouse_y = int(event.position().x()), int(event.position().y())
        
        # Botón izquierdo: Seleccionar o arrastrar pieza
        if event.button().name == 'LeftButton':
            clicked_on_piece = False
            for piece in self.placed_pieces:
                if piece.rect.collidepoint(mouse_x, mouse_y):
                    self.selected_piece = piece
                    self.offset_x = piece.rect.x - mouse_x
                    self.offset_y = piece.rect.y - mouse_y
                    clicked_on_piece = True
                    break
            
            # Si no se hizo clic en una pieza existente y tenemos una "flotante"
            # (desde el catálogo), la colocamos.
            if not clicked_on_piece and self.selected_piece:
                self.place_selected_piece()

        # Botón derecho: Eliminar pieza
        elif event.button().name == 'RightButton':
            for piece in self.placed_pieces:
                if piece.rect.collidepoint(mouse_x, mouse_y):
                    self.placed_pieces.remove(piece)
                    del piece
                    break
    
    def mouseMoveEvent(self, event):
        if self.selected_piece:
            mouse_x, mouse_y = int(event.position().x()), int(event.position().y())
            self.selected_piece.rect.x = mouse_x + self.offset_x
            self.selected_piece.rect.y = mouse_y + self.offset_y

    def mouseReleaseEvent(self, event):
        if self.selected_piece and event.button().name == 'LeftButton':
            self.place_selected_piece()

    def place_selected_piece(self):
        """Lógica para colocar la pieza seleccionada en el tablero."""
        if self.selected_piece:
            snap_to_closest(self.selected_piece, self.placed_pieces)
            if self.selected_piece not in self.placed_pieces:
                self.placed_pieces.append(self.selected_piece)
            self.selected_piece = None
            
    def create_piece_from_catalog(self, piece_class):
        """Crea una nueva pieza para que siga al cursor."""
        mouse_pos = pygame.mouse.get_pos()
        self.selected_piece = piece_class(mouse_pos[0], mouse_pos[1], PIECE_SIZE, PIECE_SIZE)

class MainWindow(QMainWindow):
    """La ventana principal de nuestra aplicación híbrida."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Juego de Calles (PyQt + Pygame)")
        
        self.setup_menu()

        # --- Layout Principal ---
        main_layout = QHBoxLayout()
        self.game_widget = GameWidget()
        main_layout.addWidget(self.game_widget)
        
        # Separador visual
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

        # --- Creación del Catálogo con Widgets de PyQt ---
        catalog_layout = QVBoxLayout()
        catalog_label = QLabel("Catálogo")
        catalog_layout.addWidget(catalog_label)

        # Definimos las piezas del catálogo
        catalog_items = [
            {"label": "Recta", "icon": "assets/straight_road.png", "class": StraightPiece},
            {"label": "Curva", "icon": "assets/curve.png", "class": CurvePiece},
            {"label": "Cruce", "icon": "assets/cross.png", "class": CrossPiece},
            {"label": "Cruce en T", "icon": "assets/t_road.png", "class": TRoadPiece},
        ]

        for item in catalog_items:
            button = QPushButton(item["label"])
            if os.path.exists(item["icon"]):
                button.setIcon(QIcon(QPixmap(item["icon"])))
                button.setIconSize(QSize(64, 64))
            
            # Conectamos el clic del botón a una función que crea la pieza correspondiente
            button.clicked.connect(lambda checked, pc=item["class"]: self.game_widget.create_piece_from_catalog(pc))
            catalog_layout.addWidget(button)

        catalog_layout.addStretch() # Empuja los botones hacia arriba
        
        catalog_container = QWidget()
        catalog_container.setFixedWidth(CATALOG_WIDTH)
        catalog_container.setLayout(catalog_layout)
        main_layout.addWidget(catalog_container)
        
        # Contenedor central
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # --- Bucle del Juego con QTimer ---
        self.timer = QTimer(self)
        self.timer.setInterval(33)  # ~30 FPS
        self.timer.timeout.connect(self.game_widget.run_game_frame)
        self.timer.start()

    def setup_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Archivo")

        new_action = QAction("Nuevo", self)
        new_action.triggered.connect(self.nuevo_juego)

        open_action = QAction("Abrir", self)
        open_action.triggered.connect(self.abrir_juego)

        save_action = QAction("Guardar", self)
        save_action.triggered.connect(self.guardar_juego)

        quit_action = QAction("Cerrar", self)
        quit_action.triggered.connect(QApplication.instance().quit)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

    # --- Funciones conectadas al Menú ---
    def nuevo_juego(self):
        print("Función 'Nuevo' activada.")
        self.game_widget.placed_pieces.clear() # Limpia el tablero

    def abrir_juego(self):
        print("Función 'Abrir' activada.")
        loaded_pieces = load_track()
        if loaded_pieces is not None:
            self.game_widget.placed_pieces = loaded_pieces

    def guardar_juego(self):
        print("Función 'Guardar' activada.")
        save_track(self.game_widget.placed_pieces)


# --- Punto de Entrada de la Aplicación ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())