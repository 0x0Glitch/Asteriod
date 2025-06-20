"""
Player entity for the Asteroids game.
"""

import pygame
from .circleshape import CircleShape
from .shot import Shot
from ..config.constants import *


class Player(CircleShape):
    """Player ship class."""
    
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.velocity = pygame.Vector2(0, 0)
        self.shoot_cooldown = 0
        self.lives = PLAYER_LIVES
        self.respawn_timer = 0
        self.is_respawning = False
        self.invulnerable_timer = 0
        
        # Asset management
        self._sprite_image = None
        self._load_sprite()

    def _load_sprite(self):
        """Load the player sprite from asset manager."""
        try:
            from ..assets import get_asset_manager
            asset_manager = get_asset_manager()
            self._sprite_image = asset_manager.get_image("player")
        except ImportError:
            # Fallback if asset manager is not available
            self._sprite_image = None

    def triangle(self):
        """Get triangle points for drawing."""
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(0, -1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        """Draw the player ship."""
        # Flash during invulnerability
        if self.invulnerable_timer > 0 and int(self.invulnerable_timer * 10) % 2:
            return  # Skip drawing to create flashing effect
        
        if not self.is_respawning:
            if self._sprite_image:
                # Use sprite image if available
                try:
                    from ..assets import get_asset_manager
                    asset_manager = get_asset_manager()
                    rotated_image = asset_manager.get_rotated_image("player", -self.rotation)
                    if rotated_image:
                        rect = rotated_image.get_rect(center=self.position)
                        screen.blit(rotated_image, rect)
                        return
                except ImportError:
                    pass
            
            # Fallback to drawing triangle
            pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        """Rotate the player ship."""
        self.rotation += dt * PLAYER_TURN_SPEED

    def move(self, dt):
        """Apply thrust to the player ship."""
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        self.velocity += forward * PLAYER_SPEED * dt

    def update(self, dt):
        """Update player state."""
        # Handle respawning
        if self.is_respawning:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.respawn()
            return

        # Update invulnerability
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt

        # Update shooting cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        # Apply velocity
        self.position += self.velocity * dt

        # Apply drag to slow down
        self.velocity *= 0.99

        # Wrap around screen
        self.wrap_around_screen()

    def shoot(self):
        """Shoot a projectile."""
        if self.shoot_cooldown > 0 or self.is_respawning:
            return None

        # Get the direction vector
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        
        # Spawn the shot at the tip of the triangle
        spawn_pos = self.position + forward * self.radius
        shot = Shot(spawn_pos.x, spawn_pos.y)
        
        # Set velocity in the forward direction
        shot.velocity = forward * PLAYER_SHOOT_SPEED
        
        # Set cooldown
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        
        return shot

    def take_damage(self):
        """Handle player taking damage."""
        if self.invulnerable_timer > 0 or self.is_respawning:
            return False  # Can't take damage while invulnerable or respawning

        self.lives -= 1
        if self.lives > 0:
            self.start_respawn()
        return True

    def start_respawn(self):
        """Start the respawn process."""
        self.is_respawning = True
        self.respawn_timer = PLAYER_RESPAWN_TIME
        # Move to center of screen
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.velocity = pygame.Vector2(0, 0)

    def respawn(self):
        """Complete the respawn process."""
        self.is_respawning = False
        self.invulnerable_timer = 2.0  # 2 seconds of invulnerability
        self.rotation = 0 