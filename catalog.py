from pieces.cross import CrossPiece
from pieces.straight_road import StraightPiece
from pieces.curve import CurvePiece
from pieces.t_road import TRoadPiece


def create_catalog():
    """Función que devuelve el catálogo de piezas."""
    return [ 
        CrossPiece(850, 175, 100, 100), # Cruce
        StraightPiece(850, 50, 100, 100), # Calle recta corta
        CurvePiece(850, 300, 100, 100),  # Curva
        TRoadPiece(850, 425, 100, 100), # Cruce en T
    ]
