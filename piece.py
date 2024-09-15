import pygame

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
        """Dibuja la pieza en la pantalla principal con detalles de carretera."""
        # Dibuja el fondo negro
        pygame.draw.rect(surface, (0, 0, 0), self.rect)

        if self.shape == 'rect':
            # Dibuja las líneas amarillas en los lados largos
            line_thickness = 10  # Grosor de las líneas de la carretera
            pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left, self.rect.top, self.rect.width, line_thickness))  # Línea amarilla superior
            pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left, self.rect.bottom - line_thickness, self.rect.width, line_thickness))  # Línea amarilla inferior

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

        elif self.shape == 'cross':
            # Dibuja las líneas amarillas para el cruce
            line_thickness = 10  # Grosor de las líneas de la carretera
            # Distancia de las líneas amarillas desde la línea punteada
            offset = 20  # Ajusta este valor según sea necesario para separar las líneas amarillas de la línea punteada

            # Líneas amarillas horizontales
            pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left, self.rect.top + self.rect.height // 2 - line_thickness // 2 - offset, self.rect.width, line_thickness))  # Línea amarilla horizontal superior
            pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left, self.rect.top + self.rect.height // 2 + line_thickness // 2 + offset, self.rect.width, line_thickness))  # Línea amarilla horizontal inferior

            # Líneas amarillas verticales
            pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left + self.rect.width // 2 - line_thickness // 2 - offset, self.rect.top, line_thickness, self.rect.height))  # Línea amarilla vertical izquierda
            pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left + self.rect.width // 2 + line_thickness // 2 + offset, self.rect.top, line_thickness, self.rect.height))  # Línea amarilla vertical derecha

            # Dibuja las líneas blancas punteadas en el centro
            num_dashes = 10  # Número de segmentos en la línea punteada
            dash_length = self.rect.width / (num_dashes * 2)
            for i in range(num_dashes):
                start_x = self.rect.left + (i * 2 * dash_length)
                end_x = start_x + dash_length
                pygame.draw.line(surface, (255, 255, 255), 
                                 (start_x, self.rect.top + self.rect.height // 2), 
                                 (end_x, self.rect.top + self.rect.height // 2), 
                                 3)  # Grosor de las líneas blancas
            num_dashes = 10  # Número de segmentos en la línea punteada
            dash_length = self.rect.height / (num_dashes * 2)
            for i in range(num_dashes):
                start_y = self.rect.top + (i * 2 * dash_length)
                end_y = start_y + dash_length
                pygame.draw.line(surface, (255, 255, 255), 
                                 (self.rect.left + self.rect.width // 2, start_y), 
                                 (self.rect.left + self.rect.width // 2, end_y), 
                                 3)  # Grosor de las líneas blancas

        # Dibuja los puntos de encaje
        for point in self.snap_points:
            global_x = self.rect.x + point[0]
            global_y = self.rect.y + point[1]
            pygame.draw.circle(surface, (255, 0, 0), (global_x, global_y), 5)

    def draw_catalog(self, surface):
        """Dibuja la pieza en el catálogo con detalles de carretera."""
        # Dibuja el fondo negro
        pygame.draw.rect(surface, (0, 0, 0), self.rect)

        if self.shape == 'rect':
            # Dibuja las líneas amarillas en los lados largos
            line_thickness = 10  # Grosor de las líneas de la carretera
            pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left, self.rect.top, self.rect.width, line_thickness))  # Línea amarilla superior
            pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left, self.rect.bottom - line_thickness, self.rect.width, line_thickness))  # Línea amarilla inferior

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

        elif self.shape == 'cross':
            # Dibuja las líneas amarillas para el cruce
            line_thickness = 10  # Grosor de las líneas de la carretera
            # Distancia de las líneas amarillas desde la línea punteada
            offset = 20  # Ajusta este valor según sea necesario para separar las líneas amarillas de la línea punteada

            # Líneas amarillas horizontales
            pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left, self.rect.top + self.rect.height // 2 - line_thickness // 2 - offset, self.rect.width, line_thickness))  # Línea amarilla horizontal superior
            pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left, self.rect.top + self.rect.height // 2 + line_thickness // 2 + offset, self.rect.width, line_thickness))  # Línea amarilla horizontal inferior

            # Líneas amarillas verticales
            pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left + self.rect.width // 2 - line_thickness // 2 - offset, self.rect.top, line_thickness, self.rect.height))  # Línea amarilla vertical izquierda
            pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(self.rect.left + self.rect.width // 2 + line_thickness // 2 + offset, self.rect.top, line_thickness, self.rect.height))  # Línea amarilla vertical derecha

            # Dibuja las líneas blancas punteadas en el centro
            num_dashes = 10  # Número de segmentos en la línea punteada
            dash_length = self.rect.width / (num_dashes * 2)
            for i in range(num_dashes):
                start_x = self.rect.left + (i * 2 * dash_length)
                end_x = start_x + dash_length
                pygame.draw.line(surface, (255, 255, 255), 
                                 (start_x, self.rect.top + self.rect.height // 2), 
                                 (end_x, self.rect.top + self.rect.height // 2), 
                                 3)  # Grosor de las líneas blancas
            num_dashes = 10  # Número de segmentos en la línea punteada
            dash_length = self.rect.height / (num_dashes * 2)
            for i in range(num_dashes):
                start_y = self.rect.top + (i * 2 * dash_length)
                end_y = start_y + dash_length
                pygame.draw.line(surface, (255, 255, 255), 
                                 (self.rect.left + self.rect.width // 2, start_y), 
                                 (self.rect.left + self.rect.width // 2, end_y), 
                                 3)  # Grosor de las líneas blancas

        # Dibuja los puntos de encaje
        for point in self.snap_points:
            global_x = self.rect.x + point[0]
            global_y = self.rect.y + point[1]
            pygame.draw.circle(surface, (255, 0, 0), (global_x, global_y), 5)
