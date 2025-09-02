import pygame
from pieces.piece import Piece
import math

# Clase para la pieza recta
class StraightPiece(Piece):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def update_snap_points(self):
        """Actualiza los puntos de encastre basados en la posición y rotación actual de la pieza."""
        center_x, center_y = self.rect.width // 2, self.rect.height // 2
        
        points = [
            (0, center_y),  # Izquierda
            (self.rect.width, center_y)  # Derecha
        ]
        
        rotated_points = []
        for x, y in points:
            # Rotar el punto alrededor del centro de la pieza
            rad_angle = math.radians(-self.angle) # Pygame rota en sentido antihorario
            new_x = center_x + (x - center_x) * math.cos(rad_angle) - (y - center_y) * math.sin(rad_angle)
            new_y = center_y + (x - center_x) * math.sin(rad_angle) + (y - center_y) * math.cos(rad_angle)
            rotated_points.append((new_x, new_y))

        self.snap_points = rotated_points


    def draw(self, surface):
        # Crea una superficie temporal para dibujar la pieza sin rotar
        piece_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        
        # Dibujar la carretera (pieza recta)
        pygame.draw.rect(piece_surface, (0, 0, 0), (0, 0, self.rect.width, self.rect.height))

        # Dibuja las líneas amarillas (banquinas)
        line_thickness = 10
        pygame.draw.rect(piece_surface, (255, 255, 0), pygame.Rect(0, 0, self.rect.width, line_thickness))
        pygame.draw.rect(piece_surface, (255, 255, 0), pygame.Rect(0, self.rect.height - line_thickness, self.rect.width, line_thickness))

        # Dibuja la línea blanca punteada en el centro
        num_dashes = 10
        dash_length = self.rect.width / (num_dashes * 2)
        for i in range(num_dashes):
            start_x = i * 2 * dash_length
            end_x = start_x + dash_length
            pygame.draw.line(piece_surface, (255, 255, 255), (start_x, self.rect.height // 2), (end_x, self.rect.height // 2), 3)

        # Rota la superficie de la pieza
        rotated_surface = pygame.transform.rotate(piece_surface, self.angle)
        
        # Obtiene el nuevo rectángulo de la superficie rotada para posicionarla correctamente
        new_rect = rotated_surface.get_rect(center=self.rect.center)
        
        # Dibuja la superficie rotada en la pantalla principal
        surface.blit(rotated_surface, new_rect.topleft)
        
        # Dibuja los puntos de encastre
        self.draw_snap_points(surface)