import pygame
import math
from pieces.piece import Piece

# Clase derivada para una curva
class CurvePiece(Piece):
    # Definimos la ruta de la imagen
    IMAGE_PATH = "assets/curve.png"
    PIECE_TYPE = "Curve"

    def __init__(self, x, y, width, height, angle=0):
        super().__init__(x, y, width, height)
        self.angle = angle
        
        # Cargamos la imagen desde la ruta de la clase
        try:
            self.original_image = pygame.image.load(CurvePiece.IMAGE_PATH).convert_alpha()
            self.image = pygame.transform.scale(self.original_image, (width, height))
        except pygame.error:
            print(f"Error: No se pudo cargar la imagen en {CurvePiece.IMAGE_PATH}")
            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill((0, 0, 0))
    
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

    def draw(self, surface, show_snap_points=False):
        rotated_surface = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_surface.get_rect(center=self.rect.center)
        surface.blit(rotated_surface, new_rect.topleft)
        
        if show_snap_points:
            self.draw_snap_points(surface)