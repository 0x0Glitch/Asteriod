import pygame
from .circleshape import CircleShape
from ..config.constants import *

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.lifetime = 3.0  # Remove shots after 3 seconds
        # Don't initialize velocity here - it will be set by the player
        
        # Asset management
        self._sprite_image = None
        self._load_sprite()

    def _load_sprite(self):
        """Load the shot sprite from asset manager."""
        try:
            from ..assets import get_asset_manager
            asset_manager = get_asset_manager()
            self._sprite_image = asset_manager.get_image("shot")
        except ImportError:
            self._sprite_image = None

    def update(self, dt):
        # Move in a straight line at constant speed
        self.position += self.velocity * dt
        
        # Wrap around screen
        self.wrap_around_screen()
        
        # Remove shot after lifetime expires
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen):
        if self._sprite_image:
            # Use sprite image if available
            rect = self._sprite_image.get_rect(center=self.position)
            screen.blit(self._sprite_image, rect)
        else:
            # Fallback to drawing circle
            pygame.draw.circle(screen, "white", self.position, self.radius, 2) 