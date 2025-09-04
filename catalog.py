from pieces.cross import CrossPiece
from pieces.straight_road import StraightPiece
from pieces.curve import CurvePiece
from pieces.t_road import TRoadPiece


def create_catalog(width):
    """Función que devuelve el catálogo de piezas."""
    catalog_x = width - 150  # Posición X base para las piezas del catálogo
    return [ 
        CrossPiece(catalog_x, 175, 100, 100), # Cruce
        StraightPiece(catalog_x, 50, 100, 100), # Calle recta corta
        CurvePiece(catalog_x, 300, 100, 100),  # Curva
        TRoadPiece(catalog_x, 425, 100, 100), # Cruce en T
    ]