import pygame
from mis_calles_game.pieces.piece import Piece
import math

# Clase para la pieza recta
class StraightPiece(Piece):
    # Definimos la ruta de la imagen y el tipo como variables de la clase
    IMAGE_PATH = "assets/straight_road.png"
    PIECE_TYPE = "Straight"

    def __init__(self, x, y, width, height, angle=0):
        # La clase base Piece ya se encarga de cargar la imagen
        super().__init__(x, y, width, height)
        self.angle = angle
        # Volvemos a llamar a update_snap_points por si el ángulo inicial no es 0
        self.update_snap_points()

    def update_snap_points(self):
        """Actualiza los puntos de encastre basados en la posición y rotación actual de la pieza."""
        center_x, center_y = self.rect.width // 2, self.rect.height // 2

        points = [
            (0, center_y),  # Izquierda
            (self.rect.width, center_y)  # Derecha
        ]

        rotated_points = []
        for x, y in points:
            rad_angle = math.radians(-self.angle)
            new_x = center_x + (x - center_x) * math.cos(rad_angle) - (y - center_y) * math.sin(rad_angle)
            new_y = center_y + (x - center_x) * math.sin(rad_angle) + (y - center_y) * math.cos(rad_angle)
            rotated_points.append((new_x, new_y))

        self.snap_points = rotated_points