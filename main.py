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
# ¡Importamos las nuevas funciones sin diálogo!
from file_manager import save_track, load_track 

# Inicializar Pygame
pygame.init()

# Definir tamaño de la ventana
WIDTH, HEIGHT = 1800, 1000
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

# Crear el catálogo de piezas
catalog = create_catalog()

# Lista de piezas que se han colocado en el tablero
placed_pieces = []

# Reloj para controlar la tasa de frames por segundo
clock = pygame.time.Clock()

# Monitoreo de uso de memoria
process = psutil.Process(os.getpid())

# Fuente para el texto
font = pygame.font.SysFont(None, 24) # Un poco más pequeño para más texto

# Bucle principal del juego
running = True
selected_piece = None
offset_x, offset_y = 0, 0

while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and selected_piece:
                selected_piece.rotate()
            
            # --- NUEVA LÓGICA DE GUARDADO Y CARGADO ---
            elif event.key == pygame.K_g: # Tecla G para Guardar
                print("Intentando guardar la pista...")
                save_track(placed_pieces)
            
            elif event.key == pygame.K_c: # Tecla C para Cargar
                print("Intentando cargar la pista...")
                loaded = load_track()
                if loaded is not None:
                    placed_pieces = loaded

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo
                mouse_x, mouse_y = event.pos
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
                selected_piece.dragging = False
                snap_to_closest(selected_piece, placed_pieces)
                if selected_piece not in placed_pieces:
                    if selected_piece.rect.colliderect(pygame.Rect(0, 0, WIDTH - CATALOG_WIDTH, HEIGHT)):
                        placed_pieces.append(selected_piece)
                selected_piece = None

        elif event.type == pygame.MOUSEMOTION:
            if selected_piece and selected_piece.dragging:
                mouse_x, mouse_y = event.pos
                selected_piece.rect.x = mouse_x + offset_x
                selected_piece.rect.y = mouse_y + offset_y

    # --- Sección de Dibujo ---
    window.fill(WHITE)
    pygame.draw.rect(window, BLUE, (WIDTH - CATALOG_WIDTH, 0, CATALOG_WIDTH, CATALOG_HEIGHT))
    pygame.draw.line(window, DARK_GRAY, (WIDTH - CATALOG_WIDTH, 0), (WIDTH - CATALOG_WIDTH, HEIGHT), 5)

    # Títulos y texto de ayuda
    catalog_text = font.render("Catálogo", True, BLACK)
    window.blit(catalog_text, (WIDTH - CATALOG_WIDTH + 65, 10))
    board_text = font.render("Tablero", True, BLACK)
    window.blit(board_text, (20, 10))
    
    # Nuevo texto de ayuda para guardar/cargar
    save_text = font.render("G = Guardar", True, BLACK)
    window.blit(save_text, (WIDTH - CATALOG_WIDTH + 50, HEIGHT - 60))
    load_text = font.render("C = Cargar", True, BLACK)
    window.blit(load_text, (WIDTH - CATALOG_WIDTH + 50, HEIGHT - 35))


    # Piezas del catálogo
    for piece in catalog:
        piece.draw_catalog(window)

    # Piezas colocadas
    for piece in placed_pieces:
        piece.draw(window)

    if selected_piece:
        selected_piece.draw(window)

    pygame.display.update()

pygame.quit()
sys.exit()