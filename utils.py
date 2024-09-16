import math
import pygame

# Distancia mínima para que una pieza se considere "cerca" de otra
SNAP_DISTANCE = 300

def snap_to_closest(piece, placed_pieces):
    """Encaja la pieza en el punto más cercano de otras piezas si es posible."""
    best_snap = None
    min_distance = float('inf')

    # Verifica que la pieza tenga puntos de encastre
    if not piece.snap_points:
        print("La pieza no tiene puntos de encastre.")
        return

    for other_piece in placed_pieces:
        if other_piece == piece or not other_piece.snap_points:
            continue  # Ignora la misma pieza o piezas sin puntos de encastre

        for point in piece.snap_points:
            for other_point in other_piece.snap_points:
                if are_points_close(point, other_point):
                    # Calcular distancia entre los puntos
                    distance = math.sqrt((piece.rect.x + point[0] - (other_piece.rect.x + other_point[0])) ** 2 +
                                         (piece.rect.y + point[1] - (other_piece.rect.y + other_point[1])) ** 2)
                    
                    if distance < min_distance:
                        min_distance = distance
                        best_snap = (other_piece, other_point, point)

    # Si se encuentra el mejor punto de encastre y está dentro del rango
    if best_snap and min_distance < SNAP_DISTANCE:
        other_piece, other_point, point = best_snap
        print(f"Punto de encastre cercano encontrado: {other_piece.rect.x}")
        print 
        new_x = other_piece.rect.x + other_point[1] *2
        new_y = other_piece.rect.y

        # Actualizar la posición de la pieza para que se toque correctamente
        piece.rect.x = new_x
        piece.rect.y = new_y
    else:
        print(f"No se encontró punto de encastre cercano. Distancia mínima encontrada: {min_distance}")


def are_points_close(point1, point2, threshold=10):
    """Verifica si dos puntos están cerca uno del otro."""
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) < threshold

