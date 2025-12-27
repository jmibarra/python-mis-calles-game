import pygame
import math
from mis_calles_game.pieces.piece import Piece

# Clase derivada para una curva
class CurvePiece(Piece):
    # Definimos la ruta de la imagen
    IMAGE_PATH = "assets/curve.png"
    PIECE_TYPE = "Curve"

    def __init__(self, x, y, width, height, angle=0):
        super().__init__(x, y, width, height)
        self.angle = angle
    
    def update_snap_points(self):
        """Actualiza los puntos de encastre basados en la posición y rotación actual de la pieza."""
        center_x, center_y = self.rect.width // 2, self.rect.height // 2
        
        points = [
            (self.rect.width // 2, self.rect.height),  # Abajo
            (0, self.rect.height // 2)                 # Izquierda
        ]
        
        rotated_points = []
        for x, y in points:
            rad_angle = math.radians(-self.angle)
            new_x = center_x + (x - center_x) * math.cos(rad_angle) - (y - center_y) * math.sin(rad_angle)
            new_y = center_y + (x - center_x) * math.sin(rad_angle) + (y - center_y) * math.cos(rad_angle)
            rotated_points.append((new_x, new_y))

        self.snap_points = rotated_points

    def get_paths(self):
        """Define rutas para la curva. Usamos las rutas base de 0 grados y las rotamos."""
        # Angle 0: Connects Left and Bottom.
        # Lane 1 (Outer? Left->Bottom): (0, 60) -> (60, 60) -> (60, 100)
        # Lane 2 (Inner? Bottom->Left): (40, 100) -> (40, 40) -> (0, 40)
        
        base_paths = [
            [(0, 60), (60, 60), (60, 100)],
            [(40, 100), (40, 40), (0, 40)]
        ]
        
        # Center for rotation
        center_x, center_y = self.rect.width // 2, self.rect.height // 2
        
        transformed_paths = []
        for path in base_paths:
            new_path = []
            for x, y in path:
                # Same rotation logic as snap points
                rad_angle = math.radians(-self.angle)
                new_x = center_x + (x - center_x) * math.cos(rad_angle) - (y - center_y) * math.sin(rad_angle)
                new_y = center_y + (x - center_x) * math.sin(rad_angle) + (y - center_y) * math.cos(rad_angle)
                new_path.append((new_x, new_y))
            transformed_paths.append(new_path)
            
        return transformed_paths