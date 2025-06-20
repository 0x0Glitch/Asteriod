"""
Base entity class for all game objects.
"""

import pygame
from abc import ABC, abstractmethod
from typing import Optional, List, Any

from ..config.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from ..utils.math_utils import wrap_position, check_collision_circles


class BaseEntity(pygame.sprite.Sprite, ABC):
    """
    Base class for all game entities.
    Provides common functionality like position, velocity, collision detection, etc.
    """
    
    def __init__(self, x: float, y: float, radius: float):
        super().__init__()
        
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.alive = True
        self.age = 0.0  # Time since creation
        
        # For sprite groups
        if hasattr(self, "containers"):
            for container in self.containers:
                container.add(self)
    
    @abstractmethod
    def update(self, dt: float) -> None:
        """Update the entity. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the entity. Must be implemented by subclasses."""
        pass
    
    def wrap_around_screen(self) -> None:
        """Make the entity wrap around screen edges."""
        self.position = wrap_position(self.position, SCREEN_WIDTH, SCREEN_HEIGHT, self.radius)
    
    def is_off_screen(self, margin: float = 100) -> bool:
        """Check if entity is off screen with margin."""
        return (self.position.x < -margin or self.position.x > SCREEN_WIDTH + margin or
                self.position.y < -margin or self.position.y > SCREEN_HEIGHT + margin)
    
    def check_collision(self, other: 'BaseEntity') -> bool:
        """Check collision with another entity."""
        return check_collision_circles(self.position, self.radius, other.position, other.radius)
    
    def destroy(self) -> None:
        """Destroy the entity."""
        self.alive = False
        self.kill()
    
    def get_center(self) -> pygame.Vector2:
        """Get the center position of the entity."""
        return self.position.copy()
    
    def move(self, dt: float) -> None:
        """Move the entity based on its velocity."""
        self.position += self.velocity * dt
    
    def apply_force(self, force: pygame.Vector2, dt: float) -> None:
        """Apply a force to the entity (changes velocity)."""
        self.velocity += force * dt
    
    def set_position(self, x: float, y: float) -> None:
        """Set the entity's position."""
        self.position.x = x
        self.position.y = y
    
    def set_velocity(self, vx: float, vy: float) -> None:
        """Set the entity's velocity."""
        self.velocity.x = vx
        self.velocity.y = vy
    
    def get_distance_to(self, other: 'BaseEntity') -> float:
        """Get distance to another entity."""
        return self.position.distance_to(other.position)
    
    def get_direction_to(self, other: 'BaseEntity') -> pygame.Vector2:
        """Get normalized direction vector to another entity."""
        direction = other.position - self.position
        if direction.length() > 0:
            return direction.normalize()
        return pygame.Vector2(0, 0)


class TriangularEntity(BaseEntity):
    """
    Base class for entities with triangular collision detection.
    """
    
    def __init__(self, x: float, y: float, radius: float):
        super().__init__(x, y, radius)
        self.rotation = 0.0  # Rotation in degrees
        self._triangle_points: List[pygame.Vector2] = []
    
    @abstractmethod
    def get_triangle_points(self) -> List[pygame.Vector2]:
        """Get the triangle points for collision detection."""
        pass
    
    def check_collision_triangular(self, other: BaseEntity) -> bool:
        """
        Check collision using triangular hitbox instead of circular.
        For now, we'll use a simplified approach with multiple circle checks.
        """
        points = self.get_triangle_points()
        
        # Check collision with each vertex of the triangle
        for point in points:
            if check_collision_circles(point, self.radius * 0.3, other.position, other.radius):
                return True
        
        # Also check center collision as fallback
        return self.check_collision(other)
    
    def rotate(self, angle_delta: float) -> None:
        """Rotate the entity by the given angle delta."""
        self.rotation += angle_delta
        self.rotation = self.rotation % 360  # Keep angle between 0-360 