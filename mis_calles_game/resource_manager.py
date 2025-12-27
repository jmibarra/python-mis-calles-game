import pygame

class ResourceManager:
    _images_cache = {}
    _sounds_cache = {}

    @classmethod
    def get_image(cls, path):
        """Loads an image from the given path, caching it for future use."""
        if path not in cls._images_cache:
            try:
                if path:
                    original_image = pygame.image.load(path).convert_alpha()
                    cls._images_cache[path] = original_image
                else:
                    cls._images_cache[path] = None
            except (pygame.error, FileNotFoundError) as e:
                print(f"Error loading image '{path}': {e}")
                cls._images_cache[path] = None
        
        return cls._images_cache[path]

    @classmethod
    def get_sound(cls, path):
        """Loads a sound from the given path, caching it for future use."""
        if path not in cls._sounds_cache:
            try:
                if path:
                    sound = pygame.mixer.Sound(path)
                    cls._sounds_cache[path] = sound
                else:
                    cls._sounds_cache[path] = None
            except (pygame.error, FileNotFoundError) as e:
                print(f"Error loading sound '{path}': {e}")
                cls._sounds_cache[path] = None
        
        return cls._sounds_cache[path]

    @classmethod
    def clear_cache(cls):
        """Clears the image and sound caches."""
        cls._images_cache.clear()
        cls._sounds_cache.clear()
