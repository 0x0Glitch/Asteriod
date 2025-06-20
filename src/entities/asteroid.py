import pygame
from .circleshape import CircleShape
from ..config.constants import *
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self._sprite_image = None
        self._load_sprite()

    def _load_sprite(self):
        """Load the appropriate asteroid sprite based on size."""
        try:
            from ..assets import get_asset_manager
            asset_manager = get_asset_manager()
            
            # Choose sprite based on size
            if self.radius >= ASTEROID_MAX_RADIUS:
                self._sprite_image = asset_manager.get_image("asteroid_large")
            elif self.radius >= ASTEROID_MIN_RADIUS * 2:
                self._sprite_image = asset_manager.get_image("asteroid_medium")
            else:
                self._sprite_image = asset_manager.get_image("asteroid_small")
        except ImportError:
            self._sprite_image = None

    def draw(self, screen):
        if self._sprite_image:
            # Use sprite image if available
            try:
                from ..assets import get_asset_manager
                asset_manager = get_asset_manager()
                
                # Scale the image to match the asteroid size
                scale = (self.radius * 2) / self._sprite_image.get_width()
                scaled_image = asset_manager.get_scaled_image(
                    "asteroid_large" if self.radius >= ASTEROID_MAX_RADIUS else
                    "asteroid_medium" if self.radius >= ASTEROID_MIN_RADIUS * 2 else
                    "asteroid_small", 
                    scale
                )
                
                if scaled_image:
                    rect = scaled_image.get_rect(center=self.position)
                    screen.blit(scaled_image, rect)
                    return
            except ImportError:
                pass
        
        # Fallback to drawing circle
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        # Wrap around screen
        self.wrap_around_screen()

    def get_score_value(self):
        """Return score value based on asteroid size"""
        if self.radius >= ASTEROID_MAX_RADIUS:
            return SCORE_LARGE_ASTEROID
        elif self.radius >= ASTEROID_MIN_RADIUS * 2:
            return SCORE_MEDIUM_ASTEROID
        else:
            return SCORE_SMALL_ASTEROID

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        angle = random.uniform(20, 50)
        a = self.velocity.rotate(angle)
        b = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        new_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid1.velocity = a * 1.2

        new_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid2.velocity = b * 1.2

            

            
            

            
         

