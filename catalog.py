from piece import Piece

def create_catalog():
    """Función que devuelve el catálogo de piezas."""
    return [
        Piece(850, 50, 100, 50, "rect"),    # Calle recta corta
        Piece(850, 120, 100, 100, "cross"), # Cruce
        Piece(850, 250, 100, 100, "curve")  # Curva
    ]
