# jmibarra/python-mis-calles-game/python-mis-calles-game-277952323df0b1e4a23e205892c6a01f2c59a922/pieces/long_straight_road.py

import pygame
from pieces.straight_road import StraightPiece # Reutilizamos la lógica de la pieza recta
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