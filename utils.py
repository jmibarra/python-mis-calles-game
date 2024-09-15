import math
import pygame
# Distancia mínima para que una pieza se considere "cerca" de otra
SNAP_DISTANCE = 300

def snap_to_closest(piece, placed_pieces):
    """Encaja la pieza en el punto más cercano de otras piezas si es posible, y evita la superposición."""
    best_snap = None
    min_distance = float('inf')

    for other_piece in placed_pieces:
        if other_piece == piece:
            continue

        for point in piece.snap_points:
            for other_point in other_piece.snap_points:
                if are_points_close(point, other_point):
                    distance = abs((piece.rect.x + point[0]) - (other_piece.rect.x + other_point[0])) + \
                               abs((piece.rect.y + point[1]) - (other_piece.rect.y + other_point[1]))
                    
                    if distance < min_distance:
                        min_distance = distance
                        best_snap = (other_piece, other_point, point)

    if best_snap and min_distance < SNAP_DISTANCE:  # Ajusta el umbral si es necesario
        other_piece, other_point, point = best_snap
        new_x = other_piece.rect.x + other_point[0] - point[0]
        new_y = other_piece.rect.y + other_point[1] - point[1]

        # Verifica si la nueva posición no causa superposición
        new_rect = pygame.Rect(new_x, new_y, piece.rect.width, piece.rect.height)
        overlap = any(new_rect.colliderect(p.rect) for p in placed_pieces if p != piece)

        if not overlap:
            piece.rect.x = new_x
            piece.rect.y = new_y



def are_points_close(point1, point2, threshold=10):
    """Verifica si dos puntos están cerca uno del otro."""
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) < threshold
