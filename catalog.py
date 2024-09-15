from pieces.cross import CrossPiece
from pieces.straight_road import StraightPiece
from pieces.curve import CurvePiece

def create_catalog():
    """Función que devuelve el catálogo de piezas."""
    return [
        StraightPiece(850, 20, 100, 100), # Calle recta corta
        CrossPiece(850, 120, 100, 100), # Cruce
        CurvePiece(850, 250, 100, 100)  # Curva
    ]
