from pieces.cross import CrossPiece
from pieces.straight_road import StraightPiece
from pieces.curve import CurvePiece
from pieces.t_road import TRoadPiece


def create_catalog():
    """Función que devuelve el catálogo de piezas."""
    return [ 
        CrossPiece(1650, 175, 100, 100), # Cruce
        StraightPiece(1650, 50, 100, 100), # Calle recta corta
        CurvePiece(1650, 300, 100, 100),  # Curva
        TRoadPiece(1650, 425, 100, 100), # Cruce en T
    ]
