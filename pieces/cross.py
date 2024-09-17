import pygame
from pieces.piece import Piece

# Clase derivada para un cruce
class CrossPiece(Piece):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def update_snap_points(self):
        """Actualiza los puntos de encastre basados en la posición actual de la pieza."""
        self.snap_points = [
            (self.rect.width // 2, 0),
            (self.rect.width, self.rect.height // 2),
            (self.rect.width // 2, self.rect.height),
            (0, self.rect.height // 2)
        ]
    def get_snap_points(self):
        return [
            (self.rect.width // 2, 0),
            (self.rect.width, self.rect.height // 2),
            (self.rect.width // 2, self.rect.height),
            (0, self.rect.height // 2)
        ]

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), self.rect)
    
                # Dibuja las líneas amarillas (banquinas)
        line_thickness = 10
        pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left, self.rect.top, self.rect.width // 4, line_thickness))  # Línea superior
        pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left, self.rect.bottom - line_thickness, self.rect.width // 4, line_thickness))  # Línea inferior
        pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left + (self.rect.width // 4 * 3), self.rect.top, self.rect.width // 4, line_thickness))  # Línea superior
        pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left + (self.rect.width // 4 * 3), self.rect.bottom - line_thickness, self.rect.width // 4, line_thickness)) 

                # Dibuja la línea blanca punteada en el centro
        num_dashes = 10
        dash_length = self.rect.width / (num_dashes * 2)
        for i in range(num_dashes):
            start_x = self.rect.left + (i * 2 * dash_length)
            end_x = start_x + dash_length
            pygame.draw.line(surface, (255, 255, 255), (start_x, self.rect.top + self.rect.height // 2), (end_x, self.rect.top + self.rect.height // 2), 3)

        for i in range(num_dashes):
            start_y = self.rect.top + (i * 2 * dash_length)  # Posición inicial en el eje y
            end_y = start_y + dash_length  # Posición final en el eje y
            pygame.draw.line(surface, (255, 255, 255), (self.rect.left + self.rect.width // 2, start_y), (self.rect.left + self.rect.width // 2, end_y), 3)

        # Dibujar un punto blanco en el centro de la pieza
        center_x = self.rect.left + self.rect.width // 2
        center_y = self.rect.top + self.rect.height // 2
        pygame.draw.circle(surface, (255, 255, 255), (center_x, center_y), 6)

        self.draw_snap_points(surface)
        