import pygame

class StraightRoadPiece:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.snap_points = self.get_snap_points()

    def get_snap_points(self):
        """Devuelve los puntos de encaje para la carretera recta."""
        return [
            (0, 0), 
            (self.rect.width, 0), 
            (0, self.rect.height), 
            (self.rect.width, self.rect.height)
        ]

    def draw(self, surface):
        """Dibuja la carretera recta con líneas amarillas y blancas."""
        # Dibuja el fondo negro
        pygame.draw.rect(surface, (0, 0, 0), self.rect)

        # Dibuja las líneas amarillas en los lados largos
        line_thickness = 10  # Grosor de las líneas de la carretera
        pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left, self.rect.top, line_thickness, self.rect.height))  # Línea amarilla izquierda
        pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.right - line_thickness, self.rect.top, line_thickness, self.rect.height))  # Línea amarilla derecha

        # Dibuja la línea blanca punteada en el centro
        num_dashes = 10  # Número de segmentos en la línea punteada
        dash_length = self.rect.width / (num_dashes * 2)
        for i in range(num_dashes):
            start_x = self.rect.left + (i * 2 * dash_length)
            end_x = start_x + dash_length
            pygame.draw.line(surface, (255, 255, 255), 
                             (start_x, self.rect.top + self.rect.height // 2), 
                             (end_x, self.rect.top + self.rect.height // 2), 
                             3)  # Grosor de las líneas blancas

        # Dibuja los puntos de encaje
        for point in self.snap_points:
            global_x = self.rect.x + point[0]
            global_y = self.rect.y + point[1]
            pygame.draw.circle(surface, (255, 0, 0), (global_x, global_y), 5)
