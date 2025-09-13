import pygame
from pieces.piece import Piece

# Clase derivada para un cruce
class CrossPiece(Piece):
    # Definimos la ruta de la imagen como una variable de la clase
    IMAGE_PATH = "assets/cross.png"
    PIECE_TYPE = "Cross"

    def __init__(self, x, y, width, height, angle=0):
        super().__init__(x, y, width, height)
        self.angle = angle
        self.update_snap_points()

    def update_snap_points(self):
        """Actualiza los puntos de encastre basados en la posición actual de la pieza."""
        # Los puntos de encastre no cambian con la rotación en un cruce simétrico
        self.snap_points = [
            (self.rect.width // 2, 0),                    # Arriba
            (self.rect.width, self.rect.height // 2),     # Derecha
            (self.rect.width // 2, self.rect.height),     # Abajo
            (0, self.rect.height // 2)                    # Izquierda
        ]