import json
from mis_calles_game.pieces.cross import CrossPiece
from mis_calles_game.pieces.straight_road import StraightPiece
from mis_calles_game.pieces.curve import CurvePiece
from mis_calles_game.pieces.t_road import TRoadPiece
from mis_calles_game.pieces.long_straight_road import LongStraightPiece
from mis_calles_game.constants import PIECE_SIZE

# Diccionario para mapear los nombres de las piezas a sus clases
PIECE_CLASSES = {
    "Cross": CrossPiece,
    "Straight": StraightPiece,
    "Curve": CurvePiece,
    "TRoad": TRoadPiece,
    "LongStraight": LongStraightPiece
}

def save_track(placed_pieces, filepath):
    track_data = [piece.to_dict() for piece in placed_pieces]
    try:
        with open(filepath, 'w') as f:
            json.dump(track_data, f, indent=4)
        print(f"Pista guardada exitosamente en {filepath}")
        return f"Pista guardada en {filepath}"
    except IOError as e:
        print(f"Error al guardar la pista: {e}")
        return f"Error al guardar la pista: {e}"

def load_track(filepath):
    try:
        with open(filepath, 'r') as f:
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
        print(f"Pista cargada exitosamente desde {filepath}")
        return loaded_pieces
    except FileNotFoundError:
        print(f"No se encontró el archivo de guardado '{filepath}'.")
        return None
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error al cargar la pista: {e}")
        return None