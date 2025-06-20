import pygame
import random
import math
from .circleshape import CircleShape

class Explosion(CircleShape):
    def __init__(self, x, y, size="medium"):
        # Set radius based on size
        size_map = {"small": 15, "medium": 25, "large": 40}
        radius = size_map.get(size, 25)
        
        super().__init__(x, y, radius)
        self.size = size
        self.lifetime = 0.8  # Total duration
        self.max_lifetime = self.lifetime
        self.particles = []
        
        # Asset management
        self._sprite_image = None
        self._load_sprite()
        
        # Create particles
        self._create_particles()

    def _load_sprite(self):
        """Load the explosion sprite from asset manager."""
        try:
            from ..assets import get_asset_manager
            asset_manager = get_asset_manager()
            self._sprite_image = asset_manager.get_image("explosion")
        except ImportError:
            self._sprite_image = None

    def _create_particles(self):
        """Create explosion particles."""
        # Handle legacy "normal" size
        size_map = {"small": 8, "medium": 12, "large": 20, "normal": 12}
        num_particles = size_map.get(self.size, 12)
        
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(30, 80)
            velocity = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
            
            particle = {
                'position': pygame.Vector2(self.position),
                'velocity': velocity,
                'color': random.choice([
                    (255, 255, 0),   # Yellow
                    (255, 165, 0),   # Orange  
                    (255, 69, 0),    # Red-orange
                    (255, 255, 255), # White
                ]),
                'size': random.uniform(2, 4),
                'lifetime': random.uniform(0.3, 0.8)
            }
            self.particles.append(particle)

    def update(self, dt):
        self.lifetime -= dt
        
        # Update particles
        for particle in self.particles[:]:  # Copy list to avoid modification during iteration
            particle['position'] += particle['velocity'] * dt
            particle['lifetime'] -= dt
            particle['size'] *= 0.98  # Shrink over time
            
            # Remove dead particles
            if particle['lifetime'] <= 0 or particle['size'] < 0.5:
                self.particles.remove(particle)
        
        # Remove explosion when done
        if self.lifetime <= 0:
            self.kill()
    
    def is_finished(self):
        """Check if explosion is finished (for backward compatibility)."""
        return self.lifetime <= 0 and len(self.particles) == 0

    def draw(self, screen):
        if self._sprite_image:
            # Use sprite image if available - scale based on animation progress
            progress = 1 - (self.lifetime / self.max_lifetime)
            scale = 0.5 + progress * 1.5  # Grows from 0.5x to 2x size
            alpha = int(255 * (self.lifetime / self.max_lifetime))  # Fade out
            
            try:
                from ..assets import get_asset_manager
                asset_manager = get_asset_manager()
                scaled_image = asset_manager.get_scaled_image("explosion", scale)
                
                if scaled_image:
                    # Apply alpha
                    temp_surface = scaled_image.copy()
                    temp_surface.set_alpha(alpha)
                    rect = temp_surface.get_rect(center=self.position)
                    screen.blit(temp_surface, rect)
                    return
            except ImportError:
                pass
        
        # Fallback: Draw particles
        for particle in self.particles:
            if particle['size'] > 0:
                pygame.draw.circle(
                    screen, 
                    particle['color'], 
                    particle['position'], 
                    int(particle['size'])
                ) 