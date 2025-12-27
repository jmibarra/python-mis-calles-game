import os
import pygame
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

from mis_calles_game.utils import snap_to_closest, find_best_snap_match
from mis_calles_game.resource_manager import ResourceManager
from mis_calles_game.constants import (GAME_WIDTH, GAME_HEIGHT, BACKGROUND_IMAGE_PATH,
                         DEFAULT_SNAP_COLOR, HIGHLIGHT_COLOR, SNAP_DISTANCE,
                         SNAP_ANIMATION_DURATION)

class GameWidget(QWidget):
    """El widget que contiene nuestro lienzo de Pygame y su lógica."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(GAME_WIDTH, GAME_HEIGHT)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        os.environ['SDL_WINDOWID'] = str(int(self.winId()))
        
        # 1. Inicializar Pygame y el mezclador de sonidos
        pygame.init()
        pygame.mixer.init()
        
        # 2. Cargar los sonidos
        self.click_sound = ResourceManager.get_sound("assets/sounds/click_sound.wav")
        self.rotate_sound = ResourceManager.get_sound("assets/sounds/rotate_sound.wav")
        self.erase_sound = ResourceManager.get_sound("assets/sounds/erase_sound.wav")

        self.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

        original_bg_image = ResourceManager.get_image(BACKGROUND_IMAGE_PATH)
        if original_bg_image:
             self.background_image = pygame.transform.scale(original_bg_image, (GAME_WIDTH, GAME_HEIGHT))
        else:
            self.background_image = None
        
        self.placed_pieces = []
        self.selected_piece = None
        self.offset_x, self.offset_y = 0, 0

        self.snap_animation_timer = 0
        self.snap_animation_pos = (0, 0)
    
    def run_game_frame(self):
        """El bucle principal del juego: Actualiza estado y dibuja."""
        self.update_game_state()
        self.draw_game()
        
    def update_game_state(self):
        """Actualiza la lógica del juego (sin dibujar)."""
        # Aquí iría lógica de actualización de físicas si la hubiera
        pass

    def draw_game(self):
        """Dibuja el estado actual del juego en la pantalla."""
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill((100, 200, 100)) 
        
        show_points = self.selected_piece is not None
        
        # Pre-calculamos el mejor snap match para el selected_piece
        best_snap_match = None
        if self.selected_piece:
             best_snap_match = find_best_snap_match(self.selected_piece, self.placed_pieces)

        for piece in self.placed_pieces:
            snap_point_colors = [DEFAULT_SNAP_COLOR] * len(piece.snap_points)
            
            # Si hay un match, resaltamos el punto específico en la pieza colocada
            if best_snap_match and best_snap_match['other_piece_rect'] == piece.rect:
                 # Necesitamos encontrar el índice del punto en la pieza para cambiar su color
                 # Como other_piece_snap_point es una tupla, la comparamos
                 for i, pt in enumerate(piece.snap_points):
                     if pt == best_snap_match['other_piece_snap_point']:
                         snap_point_colors[i] = HIGHLIGHT_COLOR
                         break
            
            piece.draw(self.screen, show_snap_points=show_points, snap_point_colors=snap_point_colors)
        
        if self.selected_piece:
            self.selected_piece.draw(self.screen, show_snap_points=True) 
        
        self.draw_snap_animation()

        pygame.display.update()

    def draw_snap_animation(self):
         if self.snap_animation_timer > 0:
            self.snap_animation_timer -= 1
            
            alpha = int(255 * (self.snap_animation_timer / SNAP_ANIMATION_DURATION))
            radius = int(20 * (1 - self.snap_animation_timer / SNAP_ANIMATION_DURATION)) + 5
            
            temp_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, (255, 255, 255, alpha), (radius, radius), radius) 
            
            self.screen.blit(temp_surface, (self.snap_animation_pos[0] - radius, self.snap_animation_pos[1] - radius))

    def keyPressEvent(self, event):
        """Captura las pulsaciones de teclas cuando este widget tiene el foco."""
        if event.key() == Qt.Key.Key_R:
            if self.selected_piece:
                self.selected_piece.rotate()
                # --- INICIO DE LA MODIFICACIÓN ---
                # 3. Reproducir sonido de rotación
                if self.rotate_sound:
                    self.rotate_sound.play()
                # --- FIN DE LA MODIFICACIÓN ---
        self.run_game_frame()

    def mousePressEvent(self, event):
        mouse_x, mouse_y = int(event.position().x()), int(event.position().y())
        
        if event.button().name == 'LeftButton':
            clicked_on_piece = False
            for piece in self.placed_pieces:
                if piece.rect.collidepoint(mouse_x, mouse_y):
                    self.selected_piece = piece
                    self.offset_x = piece.rect.x - mouse_x
                    self.offset_y = piece.rect.y - mouse_y
                    clicked_on_piece = True
                    break
            
            if not clicked_on_piece and self.selected_piece:
                self.place_selected_piece()

        elif event.button().name == 'RightButton':
            for piece in self.placed_pieces:
                if piece.rect.collidepoint(mouse_x, mouse_y):
                    self.placed_pieces.remove(piece)
                    del piece
                    self.selected_piece = None
                    if self.erase_sound:
                        self.erase_sound.play()
                    break
        self.run_game_frame()

    def mouseMoveEvent(self, event):
        if self.selected_piece:
            mouse_x, mouse_y = int(event.position().x()), int(event.position().y())
            self.selected_piece.rect.x = mouse_x + self.offset_x
            self.selected_piece.rect.y = mouse_y + self.offset_y
        self.run_game_frame()
        
    def mouseReleaseEvent(self, event):
        if self.selected_piece and event.button().name == 'LeftButton':
            snapped = self.place_selected_piece() 
            
            if snapped:
                # 3. Reproducir sonido de encastre
                if self.click_sound:
                    self.click_sound.play()
                self.snap_animation_timer = SNAP_ANIMATION_DURATION
                self.snap_animation_pos = self.selected_piece.rect.center
            
            self.selected_piece = None
        self.run_game_frame()

    def place_selected_piece(self):
        """
        Lógica para colocar la pieza seleccionada en el tablero, aplicando encastre.
        Devuelve True si la pieza se encastró a otra, False en caso contrario.
        """
        if self.selected_piece:
            original_x, original_y = self.selected_piece.rect.x, self.selected_piece.rect.y
            
            snap_to_closest(self.selected_piece, self.placed_pieces)
            
            snapped_successfully = (original_x != self.selected_piece.rect.x or original_y != self.selected_piece.rect.y)

            if self.selected_piece not in self.placed_pieces:
                self.placed_pieces.append(self.selected_piece)
            
            return snapped_successfully
        return False
            
    def create_piece_from_catalog(self, piece_class):
        """Crea una nueva pieza de un tipo dado y la asigna como la pieza seleccionada."""
        self.setFocus()
        mouse_pos = pygame.mouse.get_pos()
        self.selected_piece = piece_class(mouse_pos[0], mouse_pos[1], 100, 100) # PIECE_SIZE
        self.run_game_frame()