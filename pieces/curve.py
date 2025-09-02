# jmibarra/python-mis-calles-game/python-mis-calles-game-40e86d4dccabf522f95e116356a5f2bf66ee0576/pieces/curve.py
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
            (self.rect.width // 2, 0),  # Punto en el centro inferior
            (self.rect.width, self.rect.height // 2)  # Punto en el centro izquierdo
        ]

    def get_snap_points(self):
        return [
            (self.rect.width // 2, 0),  # Punto en el centro inferior
            (self.rect.width, self.rect.height // 2)
        ]

    def draw(self, surface):
        # Dibuja el fondo negro de la pieza
        pygame.draw.rect(surface, (0, 0, 0), self.rect)

        # --- Definiciones Geométricas Basadas en los Snap Points ---
        line_thickness = 10

        # El radio de la línea punteada central es la distancia desde el centro
        # a cualquiera de los snap points.
        # Distancia a (0, 50) = sqrt((100-0)^2 + (0-50)^2) = sqrt(12500)
        # Esto es incorrecto. Vamos a la versión anterior que funcionaba visualmente
        # y la ajustamos.
        
        # El centro de la curva está en la esquina superior derecha
        center_point = self.rect.topright
        radius_outer = self.rect.width
        # El radio interior define el ancho de la calzada
        radius_inner = self.rect.width - (self.rect.width - 2 * line_thickness) # radio interior = 20

        # Ángulos para el cuadrante inferior-izquierdo (de 90 a 180 grados)
        start_angle = math.pi / 2
        stop_angle = math.pi
        num_segments = 20

        # --- Calcula los puntos para la forma de la calzada ---
        outer_points = []
        inner_points = []
        for i in range(num_segments + 1):
            angle = start_angle + (i / num_segments) * (stop_angle - start_angle)
            outer_points.append((
                center_point[0] + math.cos(angle) * radius_outer,
                center_point[1] + math.sin(angle) * radius_outer
            ))
            inner_points.append((
                center_point[0] + math.cos(angle) * radius_inner,
                center_point[1] + math.sin(angle) * radius_inner
            ))

        # --- Dibuja los componentes de la pista ---

        # 1. Dibuja la calzada de color gris oscuro
        polygon_points = outer_points + inner_points[::-1]
        pygame.draw.polygon(surface, (70, 70, 70), polygon_points)

        # 2. Dibuja las banquinas amarillas (bordes)
        pygame.draw.lines(surface, (255, 255, 0), False, outer_points, line_thickness)
        pygame.draw.lines(surface, (255, 255, 0), False, inner_points, line_thickness)
        
        # 3. Dibuja la línea central punteada
        # El radio debe ser el promedio para que quede centrada
        center_radius = (radius_outer + radius_inner) / 2
        num_dashes = 8
        
        for i in range(num_dashes * 2):
            if i % 2 == 0:
                angle1 = start_angle + (i / (num_dashes * 2)) * (stop_angle - start_angle)
                angle2 = start_angle + ((i + 1) / (num_dashes * 2)) * (stop_angle - start_angle)
                
                start_pos = (center_point[0] + math.cos(angle1) * center_radius, center_point[1] + math.sin(angle1) * center_radius)
                end_pos = (center_point[0] + math.cos(angle2) * center_radius, center_point[1] + math.sin(angle2) * center_radius)
                
                pygame.draw.line(surface, (255, 255, 255), start_pos, end_pos, 3)

        # 4. Dibuja los puntos de encastre
        self.draw_snap_points(surface)