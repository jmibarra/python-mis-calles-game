import pygame
from piece import Piece

class StraightPiece(Piece):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def get_snap_points(self):
        return [
            (0, self.rect.height // 2),  # Puntos en los extremos de la recta
            (self.rect.width, self.rect.height // 2)
        ]

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), self.rect)

        # Dibuja las líneas amarillas
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

        # Dibuja los puntos de encaje
        for point in self.snap_points:
            global_x = self.rect.x + point[0]
            global_y = self.rect.y + point[1]
            pygame.draw.circle(surface, (255, 0, 0), (global_x, global_y), 5)