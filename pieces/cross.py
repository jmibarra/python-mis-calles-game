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
        
        # Cargamos la imagen usando la ruta definida en la clase
        try:
            self.original_image = pygame.image.load(CrossPiece.IMAGE_PATH).convert_alpha()
            self.image = pygame.transform.scale(self.original_image, (width, height))
        except pygame.error:
            # Si la imagen no se encuentra, creamos una superficie negra
            print(f"Error: No se pudo cargar la imagen en {CrossPiece.IMAGE_PATH}")
            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill((0, 0, 0))
        
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

    def draw(self, surface):
        # La pieza de cruce no necesita rotar visualmente si la imagen es simétrica,
        rotated_surface = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_surface.get_rect(center=self.rect.center)
        surface.blit(rotated_surface, new_rect.topleft)
        
        # Dibuja los puntos de encastre para depuración
        self.draw_snap_points(surface)