import json
from pieces.cross import CrossPiece
from pieces.straight_road import StraightPiece
from pieces.curve import CurvePiece
from pieces.t_road import TRoadPiece

# Un diccionario para mapear los nombres de las piezas a sus clases
PIECE_CLASSES = {
    "Cross": CrossPiece,
    "Straight": StraightPiece,
    "Curve": CurvePiece,
    "TRoad": TRoadPiece
}
PIECE_SIZE = 100  # Asumimos un tamaño constante para las piezas
DEFAULT_FILENAME = "mi_pista.json" # Nombre de archivo por defecto

def save_track(placed_pieces):
    """Guarda la pista actual y devuelve un mensaje de estado."""
    track_data = [piece.to_dict() for piece in placed_pieces]
    try:
        with open(DEFAULT_FILENAME, 'w') as f:
            json.dump(track_data, f, indent=4)
        print(f"Pista guardada exitosamente en {DEFAULT_FILENAME}")
        return f"Pista guardada en {DEFAULT_FILENAME}"
    except IOError as e:
        print(f"Error al guardar la pista: {e}")
        return f"Error al guardar la pista: {e}"

def load_track():
    """Carga una pista desde el archivo por defecto y devuelve una lista de piezas."""
    try:
        with open(DEFAULT_FILENAME, 'r') as f:
            track_data = json.load(f)

        loaded_pieces = []
        for piece_data in track_data:
            piece_type = piece_data.get("type")
            if piece_type in PIECE_CLASSES:
                piece_class = PIECE_CLASSES[piece_type]
                piece = piece_class(
                    x=piece_data["x"],
                    y=piece_data["y"],
                    width=PIECE_SIZE,
                    height=PIECE_SIZE,
                    angle=piece_data["angle"]
                )
                loaded_pieces.append(piece)
            else:
                print(f"Tipo de pieza desconocido en el archivo: {piece_type}")
        print(f"Pista cargada exitosamente desde {DEFAULT_FILENAME}")
        return loaded_pieces
    except FileNotFoundError:
        print(f"No se encontró el archivo de guardado '{DEFAULT_FILENAME}'. Coloca algunas piezas y presiona 'G' para crear uno.")
        return None
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error al cargar la pista: {e}")
        return None