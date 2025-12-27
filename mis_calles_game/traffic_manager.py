import random
import pygame
from mis_calles_game.car import Car

class TrafficManager:
    def __init__(self, game_widget):
        self.game_widget = game_widget
        self.cars = pygame.sprite.Group()
        self.spawn_timer = 0
        self.SPAWN_RATE = 120 # Frames between spawn attempts
        self.active = True

    def set_active(self, active):
        self.active = active

    def update(self):
        self.cars.update()
        
        # Remove finished cars OR extend their path
        for car in self.cars:
            if car.finished:
                # Try to find a connecting path
                current_end_point = car.position
                next_path = self.get_next_path(current_end_point)
                
                if next_path:
                    car.extend_path(next_path)
                else:
                    car.kill()

        # Attempt spawn only if active
        if self.active:
            self.spawn_timer += 1
            if self.spawn_timer >= self.SPAWN_RATE:
                self.spawn_timer = 0
                self.spawn_car()

    def spawn_car(self):
        placed_pieces = self.game_widget.placed_pieces
        if not placed_pieces:
            return

        # Pick a random piece to start
        start_piece = random.choice(placed_pieces)
        
        # Check if piece has paths
        paths = start_piece.get_paths()
        if not paths:
            return

        # Pick a random path
        path_relative = random.choice(paths)
        
        # Convert path to global coordinates
        path_global = []
        for point in path_relative:
             path_global.append((start_piece.rect.x + point[0], start_piece.rect.y + point[1]))

        # Spawn car at start of path
        if path_global:
            new_car = Car(path_global[0], path_global)
            self.cars.add(new_car)

            new_car = Car(path_global[0], path_global)
            self.cars.add(new_car)

    def get_next_path(self, current_end_point):
        """
        Busca una pieza conectada y devuelve una nueva ruta aleatoria que comience cerca de current_end_point.
        """
        placed_pieces = self.game_widget.placed_pieces
        search_radius = 5 # Tolerance for connection
        
        valid_paths = []

        for piece in placed_pieces:
            # First check if piece is close enough to be worth checking paths (optimization)
            # Simple rect check expansion might be enough, but let's just check paths for simplicity relative to number of pieces
            
            paths = piece.get_paths()
            if not paths:
                continue
                
            for path in paths:
                # Convert first point of path to global
                start_point_local = path[0]
                start_point_global = (piece.rect.x + start_point_local[0], piece.rect.y + start_point_local[1])
                
                # Check distance
                dist = (start_point_global[0] - current_end_point[0])**2 + (start_point_global[1] - current_end_point[1])**2
                if dist < search_radius**2:
                    # Found a match! Add this path in global coords
                    path_global = []
                    for point in path:
                         path_global.append((piece.rect.x + point[0], piece.rect.y + point[1]))
                    valid_paths.append(path_global)
        
        if valid_paths:
            return random.choice(valid_paths)
        
        return None

    def draw(self, surface):
        for car in self.cars:
            car.draw(surface)
