# jmibarra/python-mis-calles-game/python-mis-calles-game-277952323df0b1e4a23e205892c6a01f2c59a922/pieces/long_straight_road.py

import pygame
from mis_calles_game.pieces.straight_road import StraightPiece # Reutilizamos la lógica de la pieza recta
import math

# Clase para la pieza recta larga
class LongStraightPiece(StraightPiece):
    # Definimos la nueva ruta de imagen y el tipo
    IMAGE_PATH = "assets/long_straight_road.png"
    PIECE_TYPE = "LongStraight"

    def __init__(self, x, y, width, height, angle=0):
        # Llamamos al init de la clase base (Piece)
        # pero ajustamos el ancho para que sea el doble que el alto
        super().__init__(x, y, width * 2, height, angle)

    def get_paths(self):
        """Define rutas para la pieza larga (doble ancho)."""
        paths = []
        
        # Horizontal (0/180) -> Ancho 200, Alto 100
        if self.angle == 0 or self.angle == 180:
             # Derecho
             paths.append([(0, 60), (200, 60)])
             # Izquierdo
             paths.append([(200, 40), (0, 40)])
        
        # Vertical (90/270) -> Ancho 100, Alto 200
        elif self.angle == 90 or self.angle == 270:
             # Baja
             paths.append([(40, 0), (40, 200)]) 
             # Sube
             paths.append([(60, 200), (60, 0)])
             
        return paths