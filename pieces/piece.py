import pygame

# Clase base Piece
class Piece:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.dragging = False
        self.angle = 0  # Ángulo de rotación de la pieza
        self.snap_points = []  # Inicializamos los puntos de encastre
        self.update_snap_points()  # Calculamos los puntos de encastre al crear la pieza

    def rotate(self):
        """Rota la pieza 90 grados."""
        self.angle = (self.angle + 90) % 360
        self.update_snap_points()

    def update_snap_points(self):
        """Método abstracto que debe ser implementado por las clases hijas para recalcular los puntos de encastre."""
        raise NotImplementedError("Este método debe ser implementado por las subclases.")

    def draw(self, surface):
        """Método abstracto para dibujar la pieza en la pantalla."""
        raise NotImplementedError("Este método debe ser implementado por las subclases.")

    def draw_catalog(self, surface):
        """Dibuja la pieza en el catálogo con detalles comunes."""
        self.draw(surface)  # En muchos casos puede ser igual que dibujar en la pantalla principal.

    def draw_snap_points(self, surface):
        """Dibuja los puntos de encastre para todas las piezas."""
        for point in self.snap_points:
            global_x = self.rect.x + point[0]
            global_y = self.rect.y + point[1]
            pygame.draw.circle(surface, (255, 0, 0), (global_x, global_y), 5)