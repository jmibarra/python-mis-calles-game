import pygame
import math
from pieces.piece import Piece

# Clase derivada para una curva
class CurvePiece(Piece):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def update_snap_points(self):
        """Actualiza los puntos de encastre basados en la posición actual de la pieza."""
        self.snap_points = [
            (self.rect.width // 2, self.rect.height),  # Punto en el centro inferior
            (0, self.rect.height // 2)  # Punto en el centro izquierdo
        ]

    def get_snap_points(self):
        return [
            (self.rect.width // 2, self.rect.height),  # Punto en el centro inferior
            (0, self.rect.height // 2)
        ]

    def draw(self, surface):
        # Dibujar la carretera curva con un fondo negro
        pygame.draw.rect(surface, (0, 0, 0), self.rect)

        # Dibujar las líneas amarillas en los bordes de la carretera curva
        line_thickness = 10
        center_x, center_y = self.rect.left + self.rect.width // 2, self.rect.top + self.rect.height // 2

        # Dibujar los bordes amarillos de la curva usando arcos
        pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left, self.rect.top, self.rect.width // 2, line_thickness))  # Línea superior
        pygame.draw.arc(surface, (255, 255, 0), (self.rect.left, self.rect.top , self.rect.width, self.rect.height), 0, 1.57, line_thickness)
          # Borde inferior izquierdo
        #pygame.draw.arc(surface, (255, 255, 0), (self.rect.left + line_thickness, self.rect.top + line_thickness, self.rect.width - 2 * line_thickness, self.rect.height - 2 * line_thickness), 1.57, 3.14, line_thickness)  # Borde interno

        # Dibujar la línea punteada blanca en el centro de la curva
        num_dashes = 10
        dash_length = (self.rect.width + self.rect.height) / (num_dashes * 2)

        for i in range(num_dashes):
            angle = 0 + i * (1.57) / num_dashes  # Interpolación entre los ángulos
            start_x = center_x + (self.rect.width // 2 - line_thickness) * math.cos(angle)
            start_y = center_y + (self.rect.height // 2 - line_thickness) * math.sin(angle)
            end_x = center_x + (self.rect.width // 2 - line_thickness) * math.cos(angle + (0 - 1.57) / num_dashes)
            end_y = center_y + (self.rect.height // 2 - line_thickness) * math.sin(angle + (0 - 1.57) / num_dashes)

            pygame.draw.line(surface, (255, 255, 255), (start_x, start_y), (end_x, end_y), 3)

        # Dibujar los puntos de encastre
        self.draw_snap_points(surface)
