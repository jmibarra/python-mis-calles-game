# jmibarra/python-mis-calles-game/python-mis-calles-game-277952323df0b1e4a23e205892c6a01f2c59a922/pieces/piece.py

import pygame

# Clase base Piece
class Piece:
    # Diccionario para almacenar las imágenes ya cargadas y no leerlas del disco repetidamente
    _images_cache = {}

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.dragging = False
        self.angle = 0  # Ángulo de rotación de la pieza
        
        # Cargar la imagen usando la ruta definida en la clase hija
        if self.IMAGE_PATH not in Piece._images_cache:
            try:
                original_image = pygame.image.load(self.IMAGE_PATH).convert_alpha()
                Piece._images_cache[self.IMAGE_PATH] = original_image
            except pygame.error:
                print(f"Error: No se pudo cargar la imagen en {self.IMAGE_PATH}")
                Piece._images_cache[self.IMAGE_PATH] = None
        
        original_image = Piece._images_cache[self.IMAGE_PATH]

        if original_image:
            self.image = pygame.transform.scale(original_image, (width, height))
        else:
            # Si la imagen no se pudo cargar, creamos una superficie negra
            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill((0, 0, 0))

        self.snap_points = []  # Inicializamos los puntos de encastre
        self.update_snap_points()  # Calculamos los puntos de encastre al crear la pieza

    def rotate(self):
        """Rota la pieza 90 grados."""
        self.angle = (self.angle + 90) % 360
        self.update_snap_points()

    def update_snap_points(self):
        """Método abstracto que debe ser implementado por las clases hijas para recalcular los puntos de encastre."""
        raise NotImplementedError("Este método debe ser implementado por las subclases.")

    def draw(self, surface, show_snap_points=False):
        """Dibuja la pieza rotada en la pantalla."""
        rotated_surface = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_surface.get_rect(center=self.rect.center)
        surface.blit(rotated_surface, new_rect.topleft)
        
        if show_snap_points:
            self.draw_snap_points(surface)

    def draw_snap_points(self, surface):
        """Dibuja los puntos de encastre para todas las piezas."""
        for point in self.snap_points:
            global_x = self.rect.x + point[0]
            global_y = self.rect.y + point[1]
            pygame.draw.circle(surface, (255, 0, 0), (global_x, global_y), 5)

    def to_dict(self):
        """Serializa el estado de la pieza a un diccionario."""
        return {
            "type": self.PIECE_TYPE,
            "x": self.rect.x,
            "y": self.rect.y,
            "angle": self.angle
        }