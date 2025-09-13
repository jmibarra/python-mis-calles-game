import sys
import os
import pygame
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QFileDialog)
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtCore import QTimer, QSize, Qt

# Importamos toda la lógica del juego
from pieces.cross import CrossPiece
from pieces.straight_road import StraightPiece
from pieces.curve import CurvePiece
from pieces.t_road import TRoadPiece
from pieces.long_straight_road import LongStraightPiece
from utils import snap_to_closest
from file_manager import save_track, load_track

# --- Constantes del Juego ---
GAME_WIDTH, GAME_HEIGHT = 1600, 1000
CATALOG_WIDTH = 200
WHITE = (255, 255, 255)
PIECE_SIZE = 100
BACKGROUND_IMAGE_PATH = "assets/grass_background.png" # Asegúrate de que esta ruta sea correcta

# --- Constantes para los puntos de encastre mejorados ---
SNAP_DISTANCE = 20 # Distancia máxima para que dos puntos se consideren conectados (en píxeles)
HIGHLIGHT_COLOR = (0, 255, 0) # Color verde para puntos de encastre cercanos/compatibles
DEFAULT_SNAP_COLOR = (255, 0, 0) # Color rojo para puntos de encastre normales

class GameWidget(QWidget):
    """El widget que contiene nuestro lienzo de Pygame y su lógica."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(GAME_WIDTH, GAME_HEIGHT)
       
        # Permite que el widget reciba eventos de teclado
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Incrustamos Pygame en este widget de PyQt6
        # 'SDL_WINDOWID' es una variable de entorno que Pygame usa para renderizar en una ventana existente.
        os.environ['SDL_WINDOWID'] = str(int(self.winId()))
        pygame.init() # Inicializa Pygame
        
        # Configura la pantalla de Pygame para renderizar dentro de este widget
        self.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

        # --- Cargar y escalar la imagen de fondo UNA SOLA VEZ al inicio ---
        try:
            original_bg_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
            self.background_image = pygame.transform.scale(original_bg_image, (GAME_WIDTH, GAME_HEIGHT))
        except pygame.error:
            print(f"Error: No se pudo cargar la imagen de fondo en {BACKGROUND_IMAGE_PATH}")
            self.background_image = None
        
        # --- Estado del Juego ---
        self.placed_pieces = [] # Lista de piezas ya colocadas en el tablero
        self.selected_piece = None # La pieza que el usuario está arrastrando actualmente
        self.offset_x, self.offset_y = 0, 0 # Offset para arrastrar la pieza desde el punto de clic

        # --- Variables para la animación de encastre ---
        self.snap_animation_timer = 0 # Contador para la duración restante de la animación
        self.snap_animation_pos = (0, 0) # Posición donde se mostrará la animación
        self.SNAP_ANIMATION_DURATION = 15 # Duración de la animación en fotogramas (aprox. 0.5 segundos con timer de 33ms)
    
    def run_game_frame(self):
        """Dibuja un único fotograma del juego. Llamado por el QTimer."""
        # --- Dibujar la imagen de fondo primero ---
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            # Si no se pudo cargar la imagen de fondo, usa un color verde sólido
            self.screen.fill((100, 200, 100)) 
        
        # Determinar si mostrar los puntos de encastre (solo si hay una pieza seleccionada)
        show_points = self.selected_piece is not None
        
        # Recorrer todas las piezas ya colocadas para dibujarlas y comprobar conexiones
        for piece in self.placed_pieces:
            # Por defecto, todos los puntos de encastre son rojos
            snap_point_colors = [DEFAULT_SNAP_COLOR] * len(piece.snap_points)
            
            # Si hay una pieza seleccionada arrastrándose, comprobamos si sus puntos se acercan a los de esta pieza
            if self.selected_piece:
                # Obtenemos los puntos globales de la pieza colocada
                global_snap_points_placed = piece.get_global_snap_points()
                
                # Obtenemos los puntos globales de la pieza seleccionada
                global_snap_points_selected = self.selected_piece.get_global_snap_points()

                # Iteramos sobre cada punto de la pieza colocada
                for i, global_point_placed in enumerate(global_snap_points_placed):
                    # Comprobamos si alguno de los puntos de la pieza seleccionada está cerca
                    for global_point_selected in global_snap_points_selected:
                        # Calculamos la distancia al cuadrado (más eficiente que la raíz cuadrada)
                        dist_sq = (global_point_placed[0] - global_point_selected[0])**2 + \
                                  (global_point_placed[1] - global_point_selected[1])**2
                        
                        # Si están lo suficientemente cerca, resaltamos el punto de la pieza colocada
                        if dist_sq < SNAP_DISTANCE**2:
                            snap_point_colors[i] = HIGHLIGHT_COLOR # Cambiar a verde
                            break # Ya encontramos una conexión para este punto, pasar al siguiente
            
            # Dibujar la pieza colocada con sus puntos de encastre (posiblemente resaltados)
            piece.draw(self.screen, show_snap_points=show_points, snap_point_colors=snap_point_colors)
        
        # Dibujar la pieza que el usuario está arrastrando (si existe)
        if self.selected_piece:
            # La pieza arrastrándose siempre muestra sus puntos y en su color por defecto (rojo)
            self.selected_piece.draw(self.screen, show_snap_points=True) 

        # --- Lógica de la animación de encastre ---
        if self.snap_animation_timer > 0:
            self.snap_animation_timer -= 1 # Decrementar el contador de la animación
            
            # Calcular transparencia (alpha) y radio para el efecto de desvanecimiento
            # El alpha va de 255 (totalmente visible) a 0 (transparente)
            alpha = int(255 * (self.snap_animation_timer / self.SNAP_ANIMATION_DURATION))
            # El radio crece desde 5 hasta 25
            radius = int(20 * (1 - self.snap_animation_timer / self.SNAP_ANIMATION_DURATION)) + 5
            
            # Crear una superficie temporal con canal alfa para dibujar el círculo transparente
            temp_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            # Dibujar un círculo blanco con el alpha calculado en el centro de la superficie temporal
            pygame.draw.circle(temp_surface, (255, 255, 255, alpha), (radius, radius), radius) 
            
            # Blitear la superficie temporal en la posición de la animación en la pantalla principal
            self.screen.blit(temp_surface, (self.snap_animation_pos[0] - radius, self.snap_animation_pos[1] - radius))

        # Actualizar la pantalla de Pygame para mostrar todos los dibujos
        pygame.display.update()

    def keyPressEvent(self, event):
        """Captura las pulsaciones de teclas cuando este widget tiene el foco."""
        if event.key() == Qt.Key.Key_R:
            if self.selected_piece:
                self.selected_piece.rotate()
        # Puedes añadir aquí más atajos de teclado si lo deseas
        # elif event.key() == Qt.Key.Key_S: # Ejemplo: para alternar la visibilidad de todos los puntos de encastre
        #    self.show_all_snap_points = not self.show_all_snap_points
        self.run_game_frame() # Forzar un redibujado tras la rotación

    # --- Métodos para manejar la Interacción del Mouse ---
    def mousePressEvent(self, event):
        mouse_x, mouse_y = int(event.position().x()), int(event.position().y())
        
        if event.button().name == 'LeftButton':
            clicked_on_piece = False
            for piece in self.placed_pieces:
                if piece.rect.collidepoint(mouse_x, mouse_y):
                    self.selected_piece = piece
                    # Calcular el offset para un arrastre suave
                    self.offset_x = piece.rect.x - mouse_x
                    self.offset_y = piece.rect.y - mouse_y
                    clicked_on_piece = True
                    break
            
            # Si no se hizo clic en una pieza existente y hay una pieza seleccionada (arrastrándose desde el catálogo)
            if not clicked_on_piece and self.selected_piece:
                self.place_selected_piece() # Intenta colocar la pieza si no clicó en ninguna existente

        elif event.button().name == 'RightButton':
            # Si se hace clic derecho sobre una pieza, la eliminamos
            for piece in self.placed_pieces:
                if piece.rect.collidepoint(mouse_x, mouse_y):
                    self.placed_pieces.remove(piece)
                    del piece # Asegurarse de liberar la memoria de la pieza eliminada
                    self.selected_piece = None # Deseleccionar por si era la que teníamos seleccionada
                    break
        self.run_game_frame() # Forzar un redibujado tras cada evento de ratón

    def mouseMoveEvent(self, event):
        if self.selected_piece:
            mouse_x, mouse_y = int(event.position().x()), int(event.position().y())
            # Actualizar la posición de la pieza seleccionada con el offset
            self.selected_piece.rect.x = mouse_x + self.offset_x
            self.selected_piece.rect.y = mouse_y + self.offset_y
        self.run_game_frame() # Forzar un redibujado mientras se mueve el ratón

    def mouseReleaseEvent(self, event):
        if self.selected_piece and event.button().name == 'LeftButton':
            # Intentar encastrar y colocar la pieza. 'snapped' será True si se encastró.
            snapped = self.place_selected_piece() 
            
            if snapped:
                # Si hubo encastre, activar la animación
                self.snap_animation_timer = self.SNAP_ANIMATION_DURATION
                self.snap_animation_pos = self.selected_piece.rect.center # Posición central para la animación
            
            self.selected_piece = None # La pieza ya está colocada o deseleccionada
        self.run_game_frame() # Forzar un redibujado tras soltar el botón

    def place_selected_piece(self):
        """
        Lógica para colocar la pieza seleccionada en el tablero, aplicando encastre.
        Devuelve True si la pieza se encastró a otra, False en caso contrario.
        """
        if self.selected_piece:
            original_x, original_y = self.selected_piece.rect.x, self.selected_piece.rect.y
            
            # Aplicar la lógica de encastre para mover la pieza a la posición más cercana
            snap_to_closest(self.selected_piece, self.placed_pieces)
            
            # Comprobar si la pieza realmente cambió de posición debido al encastre
            snapped_successfully = (original_x != self.selected_piece.rect.x or original_y != self.selected_piece.rect.y)

            # Si la pieza no estaba en la lista de piezas colocadas, la añadimos
            if self.selected_piece not in self.placed_pieces:
                self.placed_pieces.append(self.selected_piece)
            
            return snapped_successfully # Devolver si hubo un encastre real
        return False # No hay pieza seleccionada, así que no hubo encastre
            
    def create_piece_from_catalog(self, piece_class):
        """Crea una nueva pieza de un tipo dado y la asigna como la pieza seleccionada."""
        self.setFocus() # Asegura que el GameWidget tenga el foco para eventos de teclado
        mouse_pos = pygame.mouse.get_pos() # Obtiene la posición actual del ratón en la ventana de Pygame
        # Crea una nueva instancia de la pieza en la posición del ratón
        self.selected_piece = piece_class(mouse_pos[0], mouse_pos[1], PIECE_SIZE, PIECE_SIZE)
        self.run_game_frame() # Redibujar para mostrar la nueva pieza siguiendo al ratón


class MainWindow(QMainWindow):
    """La ventana principal de nuestra aplicación híbrida PyQt6 + Pygame."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Juego de Calles (PyQt + Pygame)")
        # Variable para guardar la ruta del archivo actual que se está editando
        self.current_track_path = None
        
        self.setup_menu() # Configura el menú de Archivo

        # --- Configuración del layout principal ---
        main_layout = QHBoxLayout()
        
        # El widget principal donde se dibuja el juego de Pygame
        self.game_widget = GameWidget()
        main_layout.addWidget(self.game_widget)
        
        # Un separador visual entre el juego y el catálogo
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

        # --- Configuración del catálogo de piezas ---
        catalog_layout = QVBoxLayout()
        catalog_label = QLabel("Catálogo")
        catalog_layout.addWidget(catalog_label)

        # Definición de las piezas disponibles en el catálogo
        catalog_items = [
            {"label": "Recta", "icon": "assets/straight_road.png", "class": StraightPiece},
            {"label": "Recta Larga", "icon": "assets/long_straight_road.png", "class": LongStraightPiece},
            {"label": "Curva", "icon": "assets/curve.png", "class": CurvePiece},
            {"label": "Cruce", "icon": "assets/cross.png", "class": CrossPiece},
            {"label": "Cruce en T", "icon": "assets/t_road.png", "class": TRoadPiece},
        ]

        # Crear un botón para cada pieza del catálogo
        for item in catalog_items:
            button = QPushButton(item["label"])
            if os.path.exists(item["icon"]): # Asegurarse de que el icono existe
                button.setIcon(QIcon(QPixmap(item["icon"])))
                button.setIconSize(QSize(64, 64)) # Ajustar tamaño del icono
            
            # Conectar el clic del botón a la creación de una nueva pieza
            button.clicked.connect(lambda checked, pc=item["class"]: self.game_widget.create_piece_from_catalog(pc))
            catalog_layout.addWidget(button)

        catalog_layout.addStretch() # Empuja los botones hacia arriba

        # Contenedor para el catálogo con un ancho fijo
        catalog_container = QWidget()
        catalog_container.setFixedWidth(CATALOG_WIDTH)
        catalog_container.setLayout(catalog_layout)
        main_layout.addWidget(catalog_container)
        
        # Establecer el layout principal en el widget central de la ventana
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # --- QTimer para el bucle de juego de Pygame ---
        self.timer = QTimer(self)
        self.timer.setInterval(33) # Aproximadamente 30 FPS (1000ms / 30 = 33.33ms)
        self.timer.timeout.connect(self.game_widget.run_game_frame) # Llama a run_game_frame cada 33ms
        self.timer.start() # Iniciar el timer

    def setup_menu(self):
        """Configura la barra de menú con las opciones de archivo."""
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Archivo")

        new_action = QAction("Nuevo", self)
        new_action.triggered.connect(self.nuevo_juego)

        open_action = QAction("Abrir", self)
        open_action.triggered.connect(self.abrir_juego)

        save_action = QAction("Guardar", self)
        save_action.triggered.connect(self.guardar_juego)
        
        save_as_action = QAction("Guardar Como...", self)
        save_as_action.triggered.connect(self.guardar_juego_como)

        quit_action = QAction("Cerrar", self)
        quit_action.triggered.connect(QApplication.instance().quit)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

    def nuevo_juego(self):
        """Reinicia el tablero de juego."""
        print("Función 'Nuevo' activada.")
        self.game_widget.placed_pieces.clear() # Limpiar todas las piezas
        self.current_track_path = None # Resetea la ruta del archivo actual
        self.game_widget.run_game_frame() # Forzar redibujado

    def abrir_juego(self):
        """Carga una pista de juego desde un archivo JSON."""
        print("Función 'Abrir' activada.")
        # Abre el diálogo para seleccionar un archivo JSON
        filepath, _ = QFileDialog.getOpenFileName(self, "Abrir Pista", "", "Archivos de Pista (*.json)")
        
        if filepath: # Si el usuario seleccionó un archivo
            loaded_pieces = load_track(filepath) # Cargar las piezas desde el archivo
            if loaded_pieces is not None:
                self.game_widget.placed_pieces = loaded_pieces # Asignar las piezas cargadas al widget de juego
                self.current_track_path = filepath # Guardar la ruta del archivo actual
                self.game_widget.run_game_frame() # Forzar redibujado

    def guardar_juego(self):
        """Guarda la pista actual. Si es nueva, pregunta dónde guardarla."""
        print("Función 'Guardar' activada.")
        if self.current_track_path:
            # Si ya hay una ruta, guardar directamente
            save_track(self.game_widget.placed_pieces, self.current_track_path)
        else:
            # Si no, llamar a "Guardar Como..." para elegir la ubicación
            self.guardar_juego_como()

    def guardar_juego_como(self):
        """Guarda la pista actual en una nueva ubicación o con un nuevo nombre."""
        print("Función 'Guardar Como...' activada.")
        # Abre el diálogo para elegir la ubicación y nombre del archivo
        filepath, _ = QFileDialog.getSaveFileName(self, "Guardar Pista", "", "Archivos de Pista (*.json)")
        
        if filepath: # Si el usuario eligió una ubicación
             # Asegurar que la extensión sea .json
            if not filepath.endswith('.json'):
                filepath += '.json'
            save_track(self.game_widget.placed_pieces, filepath) # Guardar la pista
            self.current_track_path = filepath # Actualizar la ruta del archivo actual


# --- Punto de Entrada de la Aplicación ---
if __name__ == '__main__':
    app = QApplication(sys.argv) # Crea la aplicación PyQt6
    window = MainWindow() # Crea la ventana principal
    window.show() # Muestra la ventana
    sys.exit(app.exec()) # Inicia el bucle de eventos de la aplicación