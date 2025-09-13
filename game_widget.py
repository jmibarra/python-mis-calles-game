import os
import pygame
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

from utils import snap_to_closest
from constants import (GAME_WIDTH, GAME_HEIGHT, BACKGROUND_IMAGE_PATH,
                         DEFAULT_SNAP_COLOR, HIGHLIGHT_COLOR, SNAP_DISTANCE,
                         SNAP_ANIMATION_DURATION)

class GameWidget(QWidget):
    """El widget que contiene nuestro lienzo de Pygame y su lógica."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(GAME_WIDTH, GAME_HEIGHT)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        os.environ['SDL_WINDOWID'] = str(int(self.winId()))
        pygame.init()
        
        self.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

        try:
            original_bg_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
            self.background_image = pygame.transform.scale(original_bg_image, (GAME_WIDTH, GAME_HEIGHT))
        except pygame.error:
            print(f"Error: No se pudo cargar la imagen de fondo en {BACKGROUND_IMAGE_PATH}")
            self.background_image = None
        
        self.placed_pieces = []
        self.selected_piece = None
        self.offset_x, self.offset_y = 0, 0

        self.snap_animation_timer = 0
        self.snap_animation_pos = (0, 0)
    
    def run_game_frame(self):
        """Dibuja un único fotograma del juego. Llamado por el QTimer."""
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill((100, 200, 100)) 
        
        show_points = self.selected_piece is not None
        
        for piece in self.placed_pieces:
            snap_point_colors = [DEFAULT_SNAP_COLOR] * len(piece.snap_points)
            
            if self.selected_piece:
                global_snap_points_placed = piece.get_global_snap_points()
                global_snap_points_selected = self.selected_piece.get_global_snap_points()

                for i, global_point_placed in enumerate(global_snap_points_placed):
                    for global_point_selected in global_snap_points_selected:
                        dist_sq = (global_point_placed[0] - global_point_selected[0])**2 + \
                                  (global_point_placed[1] - global_point_selected[1])**2
                        
                        if dist_sq < SNAP_DISTANCE**2:
                            snap_point_colors[i] = HIGHLIGHT_COLOR
                            break
            
            piece.draw(self.screen, show_snap_points=show_points, snap_point_colors=snap_point_colors)
        
        if self.selected_piece:
            self.selected_piece.draw(self.screen, show_snap_points=True) 

        if self.snap_animation_timer > 0:
            self.snap_animation_timer -= 1
            
            alpha = int(255 * (self.snap_animation_timer / SNAP_ANIMATION_DURATION))
            radius = int(20 * (1 - self.snap_animation_timer / SNAP_ANIMATION_DURATION)) + 5
            
            temp_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, (255, 255, 255, alpha), (radius, radius), radius) 
            
            self.screen.blit(temp_surface, (self.snap_animation_pos[0] - radius, self.snap_animation_pos[1] - radius))

        pygame.display.update()

    def keyPressEvent(self, event):
        """Captura las pulsaciones de teclas cuando este widget tiene el foco."""
        if event.key() == Qt.Key.Key_R:
            if self.selected_piece:
                self.selected_piece.rotate()
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