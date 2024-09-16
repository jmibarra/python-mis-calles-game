import pygame
from pieces.piece import Piece


# Clase para la pieza recta
class StraightPiece(Piece):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def update_snap_points(self):
        """Actualiza los puntos de encastre basados en la posición actual de la pieza."""
        self.snap_points = [
            (0, self.rect.height // 2),  # Punto en el extremo izquierdo de la recta
            (self.rect.width, self.rect.height // 2)  # Punto en el extremo derecho de la recta
        ]

    def draw(self, surface):
        # Dibujar la carretera (pieza recta)
        pygame.draw.rect(surface, (0, 0, 0), self.rect)

        # Dibuja las líneas amarillas (banquinas)
        line_thickness = 10
        pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left, self.rect.top, self.rect.width, line_thickness))  # Línea superior
        pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left, self.rect.bottom - line_thickness, self.rect.width, line_thickness))  # Línea inferior

        # Dibuja la línea blanca punteada en el centro
        num_dashes = 10
        dash_length = self.rect.width / (num_dashes * 2)
        for i in range(num_dashes):
            start_x = self.rect.left + (i * 2 * dash_length)
            end_x = start_x + dash_length
            pygame.draw.line(surface, (255, 255, 255), (start_x, self.rect.top + self.rect.height // 2), (end_x, self.rect.top + self.rect.height // 2), 3)

        # Dibuja los puntos de encastre
        self.draw_snap_points(surface)
