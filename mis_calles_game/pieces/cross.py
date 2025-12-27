import pygame
from mis_calles_game.pieces.piece import Piece

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

    def get_paths(self):
        """Define rutas para el cruce: Rectas y Giros."""
        paths = []
        
        # Straight paths
        # Left <-> Right
        paths.append([(0, 60), (100, 60)])
        paths.append([(100, 40), (0, 40)])
        # Top <-> Bottom
        paths.append([(40, 0), (40, 100)]) # Down
        paths.append([(60, 100), (60, 0)]) # Up
        
        # Right Turns (assuming right-hand traffic logic)
        # Left -> Down
        paths.append([(0, 60), (40, 60), (40, 100)])
        # Bottom -> Right
        paths.append([(60, 100), (60, 60), (100, 60)])
        # Right -> Top
        paths.append([(100, 40), (60, 40), (60, 0)])
        # Top -> Left
        paths.append([(40, 0), (40, 40), (0, 40)])
        
        # Left Turns (Crossing traffic)
        # Left -> Top
        paths.append([(0, 60), (60, 60), (60, 0)])
        # Top -> Right
        paths.append([(40, 0), (40, 60), (100, 60)])
        # Right -> Bottom
        paths.append([(100, 40), (40, 40), (40, 100)])
        # Bottom -> Left
        paths.append([(60, 100), (60, 40), (0, 40)])
        
        return paths