# jmibarra/python-mis-calles-game/python-mis-calles-game-277952323df0b1e4a23e205892c6a01f2c59a922/pieces/piece.py

import pygame

from mis_calles_game.resource_manager import ResourceManager

# Clase base Piece
class Piece:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.dragging = False
        self.angle = 0  # Ángulo de rotación de la pieza
        
        self.image = ResourceManager.get_image(self.IMAGE_PATH)

        if self.image:
             self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA) # Añadimos SRCALPHA para transparencia
            self.image.fill((0, 0, 0, 0)) # Transparente

        self.snap_points = []  # Inicializamos los puntos de encastre (relativos a la pieza)
        self.update_snap_points()  # Calculamos los puntos de encastre al crear la pieza

    def rotate(self):
        """Rota la pieza 90 grados."""
        self.angle = (self.angle + 90) % 360
        self.update_snap_points()

    def update_snap_points(self):
        """Método abstracto que debe ser implementado por las clases hijas para recalcular los puntos de encastre."""
        raise NotImplementedError("Este método debe ser implementado por las subclases.")

    def get_paths(self):
        """
        Devuelve una lista de rutas (listas de coordenadas) relativas a la pieza.
        Por defecto devuelve una lista vacía.
        """
        return []

    def get_global_snap_points(self):
        """Devuelve los puntos de encastre en coordenadas globales."""
        global_points = []
        for point in self.snap_points:
            global_points.append((self.rect.x + point[0], self.rect.y + point[1]))
        return global_points

    def draw(self, surface, show_snap_points=False, snap_point_colors=None):
        """Dibuja la pieza rotada en la pantalla."""
        rotated_surface = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_surface.get_rect(center=self.rect.center)
        surface.blit(rotated_surface, new_rect.topleft)
        
        if show_snap_points:
            self.draw_snap_points(surface, snap_point_colors) # Pasamos los colores

    def draw_snap_points(self, surface, snap_point_colors=None):
        """Dibuja los puntos de encastre para todas las piezas, con colores opcionales."""
        if snap_point_colors is None:
            snap_point_colors = [(255, 0, 0)] * len(self.snap_points) # Rojo por defecto para todos
        
        for i, point in enumerate(self.snap_points):
            global_x = int(self.rect.x + point[0]) # Asegurarse de que son enteros para pygame.draw.circle
            global_y = int(self.rect.y + point[1])
            
            color = snap_point_colors[i] if i < len(snap_point_colors) else (255, 0, 0)
            pygame.draw.circle(surface, color, (global_x, global_y), 5)

    def to_dict(self):
        """Serializa el estado de la pieza a un diccionario."""
        return {
            "type": self.PIECE_TYPE,
            "x": self.rect.x,
            "y": self.rect.y,
            "angle": self.angle
        }