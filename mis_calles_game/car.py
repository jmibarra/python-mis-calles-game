import pygame
import math

class Car(pygame.sprite.Sprite):
    def __init__(self, start_pos, path, speed=2):
        super().__init__()
        self.image = pygame.Surface((20, 10), pygame.SRCALPHA)
        self.image.fill((0, 0, 255)) # Blue car
        self.rect = self.image.get_rect(center=start_pos)
        
        self.path = path # List of (x, y) tuples
        self.current_target_index = 1
        self.speed = speed
        self.position = list(start_pos)
        
        self.finished = False

    def update(self):
        if self.finished:
            return

        if self.current_target_index >= len(self.path):
            self.finished = True
            return

        target = self.path[self.current_target_index]
        dx = target[0] - self.position[0]
        dy = target[1] - self.position[1]
        distance = math.sqrt(dx**2 + dy**2)

        if distance < self.speed:
            self.position = list(target)
            self.current_target_index += 1
        else:
            angle = math.atan2(dy, dx)
            move_x = self.speed * math.cos(angle)
            move_y = self.speed * math.sin(angle)
            self.position[0] += move_x
            self.position[1] += move_y
            
            # Rotation (visual only for now)
            angle_degrees = math.degrees(-angle)
            self.image = pygame.transform.rotate(pygame.Surface((20, 10), pygame.SRCALPHA), angle_degrees)
            self.image.fill((0, 0, 255)) # Re-fill after rotate creates new surface
            # Note: real rotation requires keeping original image, skipping for simple prototype

        self.rect.center = (int(self.position[0]), int(self.position[1]))

    def extend_path(self, new_path):
        """Extends the car's path with a new sequence of points."""
        self.path = new_path
        self.current_target_index = 0
        self.finished = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
