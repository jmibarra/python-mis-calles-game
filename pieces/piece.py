import pygame

# Clase base Piece
class Piece:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.dragging = False
        self.snap_points = self.get_snap_points()

    def get_snap_points(self):
        """Método abstracto que debe ser implementado por las clases hijas."""
        raise NotImplementedError("Este método debe ser implementado por las subclases.")

    def draw(self, surface):
        """Método abstracto para dibujar la pieza en la pantalla."""
        raise NotImplementedError("Este método debe ser implementado por las subclases.")

    def draw_catalog(self, surface):
        """Dibuja la pieza en el catálogo con detalles comunes."""
        self.draw(surface)  # En muchos casos puede ser igual que dibujar en la pantalla principal.
