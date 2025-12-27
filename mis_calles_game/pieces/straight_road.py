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

        # Si asumimos que la imagen original es Horizontal (0 grados = Horizontal)
        # Entonces 0/180 deben tener puntos izquierda/derecha.
        points = []
        if self.angle == 0 or self.angle == 180:
             points = [(0, center_y), (self.rect.width, center_y)]
        elif self.angle == 90 or self.angle == 270:
             points = [(center_x, 0), (center_x, self.rect.height)]
        
        # Nota: La lógica anterior de rotación manual de puntos era redundante si definimos los puntos explícitamente por ángulo
        # Simplificamos asignando directamente según el ángulo visual final
        
        # Debemos asegurar que los puntos sean relativos (x, y)
        self.snap_points = points

    def get_paths(self):
        """Define rutas rectas según el ángulo."""
        paths = []
        
        # Ahora 0/180 es Horizontal
        if self.angle == 0 or self.angle == 180:
             # Carril "Derecha" (Top lane in standard view?)
             # Vamos a centralizarlos un poco más: 40 y 60
             paths.append([(0, 60), (100, 60)])
             # Carril "Izquierda"
             paths.append([(100, 40), (0, 40)])
        
        # Ahora 90/270 es Vertical
        elif self.angle == 90 or self.angle == 270:
             # Carril "Baja"
             paths.append([(40, 0), (40, 100)]) 
             # Carril "Sube"
             paths.append([(60, 100), (60, 0)])
             
        return paths