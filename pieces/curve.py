import pygame
import math
from pieces.piece import Piece

# Clase derivada para una curva
class CurvePiece(Piece):
    # Definimos la ruta de la imagen
    IMAGE_PATH = "assets/curve.png"

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        
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
        
        # Puntos de encastre para la curva en su posición original (0 grados)
        # Conecta la parte inferior con la izquierda
        points = [
            (self.rect.width // 2, self.rect.height),  # Abajo
            (0, self.rect.height // 2)                 # Izquierda
        ]
        
        rotated_points = []
        for x, y in points:
            # Rotamos cada punto alrededor del centro de la pieza
            rad_angle = math.radians(-self.angle) # Pygame rota en sentido antihorario
            new_x = center_x + (x - center_x) * math.cos(rad_angle) - (y - center_y) * math.sin(rad_angle)
            new_y = center_y + (x - center_x) * math.sin(rad_angle) + (y - center_y) * math.cos(rad_angle)
            rotated_points.append((new_x, new_y))

        self.snap_points = rotated_points

    def draw(self, surface):
        # Rotamos la imagen de la pieza
        rotated_surface = pygame.transform.rotate(self.image, self.angle)
        
        # Obtenemos el nuevo rectángulo para centrar la imagen rotada
        new_rect = rotated_surface.get_rect(center=self.rect.center)
        
        # Dibujamos la pieza en la pantalla
        surface.blit(rotated_surface, new_rect.topleft)
        
        # Dibujamos los puntos de encastre para ver cómo se mueven
        self.draw_snap_points(surface)