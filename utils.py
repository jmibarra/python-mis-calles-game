import math
import pygame

# Distancia mínima para que una pieza se considere "cerca" de otra
SNAP_DISTANCE = 50

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
            # Coordenadas globales del punto de la pieza que se está moviendo
            point_global = (piece.rect.x + point[0], piece.rect.y + point[1])

            for other_point in other_piece.snap_points:
                # Coordenadas globales del punto de la pieza que ya está en el tablero
                other_point_global = (other_piece.rect.x + other_point[0], other_piece.rect.y + other_point[1])
                
                # Calcular distancia entre los puntos globales
                distance = math.sqrt((point_global[0] - other_point_global[0]) ** 2 +
                                     (point_global[1] - other_point_global[1]) ** 2)
                
                if distance < min_distance:
                    min_distance = distance
                    # Guardamos la información necesaria para el ajuste
                    best_snap = {
                        "piece_snap_point": point,
                        "other_piece_rect": other_piece.rect,
                        "other_piece_snap_point": other_point
                    }

    # Si se encuentra el mejor punto de encastre y está dentro del rango
    if best_snap and min_distance < SNAP_DISTANCE:
        print(f"Se encontró punto de encastre cercano. Distancia mínima: {min_distance}")
        
        # Extraemos la información del mejor punto de anclaje
        piece_snap_point = best_snap["piece_snap_point"]
        other_piece_rect = best_snap["other_piece_rect"]
        other_piece_snap_point = best_snap["other_piece_snap_point"]

        # Calculamos la nueva posición de la pieza para que los puntos coincidan
        new_x = other_piece_rect.x + other_piece_snap_point[0] - piece_snap_point[0]
        new_y = other_piece_rect.y + other_piece_snap_point[1] - piece_snap_point[1]

        # Actualizar la posición de la pieza
        piece.rect.x = new_x
        piece.rect.y = new_y
    else:
        print(f"No se encontró punto de encastre cercano. Distancia mínima encontrada: {min_distance}")


def are_points_close(point1, point2, threshold=50):
    """Verifica si dos puntos están cerca uno del otro."""
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) < threshold