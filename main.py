import pygame
import sys
import os
import psutil

from pieces.cross import CrossPiece
from pieces.straight_road import StraightPiece
from pieces.curve import CurvePiece
from pieces.t_road import TRoadPiece
from utils import snap_to_closest
from catalog import create_catalog

# Inicializar Pygame
pygame.init()

# Definir tamaño de la ventana
WIDTH, HEIGHT = 1000, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Pistas de Autos")

# Definir colores
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (135, 206, 235)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

# Definir la posición y tamaño del catálogo
CATALOG_WIDTH = 200
CATALOG_HEIGHT = HEIGHT

# Crear el catálogo de piezas (ajustado a las clases hijas)
catalog = create_catalog()

# Lista de piezas que se han colocado en el tablero
placed_pieces = []

# Definir un reloj para controlar la tasa de frames por segundo
clock = pygame.time.Clock()

# Monitoreo de uso de memoria
process = psutil.Process(os.getpid())

# Fuente para el texto
font = pygame.font.SysFont(None, 36)

# Bucle principal del juego
running = True
selected_piece = None  # Para saber qué pieza está siendo arrastrada o seleccionada
offset_x, offset_y = 0, 0  # Variables para manejar el desplazamiento del mouse

while running:
    # Limitar a 30 frames por segundo
    clock.tick(30)

    # Monitorear el uso de memoria
    #print(f"Uso de memoria: {process.memory_info().rss / 1024 ** 2:.2f} MB")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and selected_piece:
                selected_piece.rotate()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse button down")
            mouse_x, mouse_y = event.pos
            if event.button == 1:  # Botón izquierdo
                clicked_on_piece = False

                for piece in placed_pieces:
                    if piece.rect.collidepoint(event.pos):
                        selected_piece = piece
                        selected_piece.dragging = True
                        offset_x = selected_piece.rect.x - mouse_x
                        offset_y = selected_piece.rect.y - mouse_y
                        clicked_on_piece = True
                        break

                if not clicked_on_piece:
                    for piece in catalog:
                        if piece.rect.collidepoint(event.pos):
                            # Crear una nueva instancia de la pieza seleccionada según su tipo
                            if isinstance(piece, StraightPiece):
                                selected_piece = StraightPiece(mouse_x, mouse_y, piece.rect.width, piece.rect.height)
                            elif isinstance(piece, CurvePiece):
                                selected_piece = CurvePiece(mouse_x, mouse_y, piece.rect.width, piece.rect.height)
                            elif isinstance(piece, CrossPiece):
                                selected_piece = CrossPiece(mouse_x, mouse_y, piece.rect.width, piece.rect.height)
                            elif isinstance(piece, TRoadPiece):
                                selected_piece = TRoadPiece(mouse_x, mouse_y, piece.rect.width, piece.rect.height)

                            selected_piece.dragging = True
                            offset_x = selected_piece.rect.x - mouse_x
                            offset_y = selected_piece.rect.y - mouse_y
                            break

            elif event.button == 3:  # Botón derecho
                for piece in placed_pieces:
                    if piece.rect.collidepoint(event.pos):
                        placed_pieces.remove(piece)
                        del piece
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_piece:
                print("Pieza ya seleccionada")
                selected_piece.dragging = False
                snap_to_closest(selected_piece, placed_pieces) # Encaja la pieza
                if selected_piece not in placed_pieces:
                    # Intentar encajar la pieza en el tablero
                    if selected_piece.rect.colliderect(pygame.Rect(0, 0, WIDTH - CATALOG_WIDTH, HEIGHT)):
                        placed_pieces.append(selected_piece)
                selected_piece = None

        elif event.type == pygame.MOUSEMOTION:
            if selected_piece and selected_piece.dragging:
                mouse_x, mouse_y = event.pos
                selected_piece.rect.x = mouse_x + offset_x
                selected_piece.rect.y = mouse_y + offset_y

    # Llenar la ventana con un color de fondo para el tablero (lado izquierdo)
    window.fill(WHITE)

    # Dibujar la sección del catálogo (lado derecho)
    pygame.draw.rect(window, BLUE, (WIDTH - CATALOG_WIDTH, 0, CATALOG_WIDTH, CATALOG_HEIGHT))

    # Dibujar una línea divisoria entre el tablero y el catálogo
    pygame.draw.line(window, DARK_GRAY, (WIDTH - CATALOG_WIDTH, 0), (WIDTH - CATALOG_WIDTH, HEIGHT), 5)

    # Dibujar el título "Catálogo" en la parte superior del catálogo
    catalog_text = font.render("Catálogo", True, BLACK)
    window.blit(catalog_text, (WIDTH - CATALOG_WIDTH + 40, 10))

    # Dibujar el título "Tablero" en la parte superior del área de juego
    board_text = font.render("Tablero", True, BLACK)
    window.blit(board_text, (20, 10))

    # Dibujar el catálogo de piezas en el lado derecho
    for piece in catalog:
        piece.draw_catalog(window)

    # Dibujar las piezas que ya están colocadas en el tablero
    for piece in placed_pieces:
        if piece.rect.right > 0 and piece.rect.left < WIDTH - CATALOG_WIDTH and piece.rect.bottom > 0 and piece.rect.top < HEIGHT:
            piece.draw(window)

    if selected_piece:
        selected_piece.draw(window)

    pygame.display.update()

pygame.quit()

sys.exit()
