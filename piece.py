import pygame
import math

class Piece:
    def __init__(self, x, y, width, height, shape):
        self.rect = pygame.Rect(x, y, width, height)
        self.shape = shape
        self.dragging = False
        self.snap_points = self.get_snap_points()

    def get_snap_points(self):
        """Devuelve los puntos de encaje específicos para cada tipo de pieza."""
        points = []
        if self.shape == 'rect':
            points = [
                (0, 0),
                (self.rect.width, 0),
                (0, self.rect.height),
                (self.rect.width, self.rect.height)
            ]
        elif self.shape == 'curve':
            points = [
                (self.rect.width / 2, 0),
                (self.rect.width, self.rect.height / 2),
                (self.rect.width / 2, self.rect.height),
                (0, self.rect.height / 2)
            ]
        elif self.shape == 'cross':
            points = [
                (self.rect.width / 2, 0),
                (self.rect.width, self.rect.height / 2),
                (self.rect.width / 2, self.rect.height),
                (0, self.rect.height / 2)
            ]
        return points


    def draw(self, surface):
        """Dibuja la pieza y sus puntos de encaje en el tablero principal."""
        # Dibuja la pieza
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        # Dibuja los puntos de encaje
        for point in self.snap_points:
            # Convertir puntos de encaje a coordenadas globales
            global_x = self.rect.x + point[0]
            global_y = self.rect.y + point[1]
            pygame.draw.circle(surface, (255, 0, 0), (global_x, global_y), 5)


    def draw_catalog(self, surface):
        """Dibuja la pieza y sus puntos de encaje en el catálogo."""
        # Dibuja la pieza
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        # Dibuja los puntos de encaje
        for point in self.snap_points:
            # Convertir puntos de encaje a coordenadas globales en el catálogo
            global_x = self.rect.x + point[0]
            global_y = self.rect.y + point[1]
            pygame.draw.circle(surface, (255, 0, 0), (global_x, global_y), 5)

