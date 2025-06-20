"""
Mathematical utility functions for the game.
"""

import math
import random
import pygame
from typing import List, Tuple


def wrap_position(position: pygame.Vector2, screen_width: int, screen_height: int, radius: float) -> pygame.Vector2:
    """
    Wrap a position around screen boundaries.
    
    Args:
        position: Current position
        screen_width: Screen width
        screen_height: Screen height
        radius: Object radius for proper wrapping
        
    Returns:
        Wrapped position
    """
    x, y = position.x, position.y
    
    if x < -radius:
        x = screen_width + radius
    elif x > screen_width + radius:
        x = -radius
        
    if y < -radius:
        y = screen_height + radius
    elif y > screen_height + radius:
        y = -radius
        
    return pygame.Vector2(x, y)


def distance_between(pos1: pygame.Vector2, pos2: pygame.Vector2) -> float:
    """Calculate distance between two positions."""
    return pos1.distance_to(pos2)


def normalize_angle(angle: float) -> float:
    """Normalize angle to be between 0 and 360 degrees."""
    return angle % 360


def angle_to_vector(angle: float) -> pygame.Vector2:
    """Convert angle in degrees to unit vector."""
    rad = math.radians(angle)
    return pygame.Vector2(math.cos(rad), math.sin(rad))


def vector_to_angle(vector: pygame.Vector2) -> float:
    """Convert vector to angle in degrees."""
    return math.degrees(math.atan2(vector.y, vector.x))


def generate_lumpy_asteroid_points(center: pygame.Vector2, base_radius: float, vertices: int) -> List[pygame.Vector2]:
    """
    Generate points for a lumpy asteroid shape.
    
    Args:
        center: Center position
        base_radius: Base radius
        vertices: Number of vertices
        
    Returns:
        List of points forming the asteroid shape
    """
    points = []
    angle_step = 360 / vertices
    
    for i in range(vertices):
        angle = i * angle_step
        # Add some randomness to make it lumpy
        radius_variation = random.uniform(0.7, 1.3)
        radius = base_radius * radius_variation
        
        rad = math.radians(angle)
        x = center.x + radius * math.cos(rad)
        y = center.y + radius * math.sin(rad)
        points.append(pygame.Vector2(x, y))
    
    return points


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamp a value between min and max."""
    return max(min_value, min(value, max_value))


def lerp(start: float, end: float, t: float) -> float:
    """Linear interpolation between start and end."""
    return start + (end - start) * t


def random_vector(min_length: float = 0, max_length: float = 1) -> pygame.Vector2:
    """Generate a random vector with length between min_length and max_length."""
    angle = random.uniform(0, 2 * math.pi)
    length = random.uniform(min_length, max_length)
    return pygame.Vector2(math.cos(angle) * length, math.sin(angle) * length)


def is_point_in_circle(point: pygame.Vector2, center: pygame.Vector2, radius: float) -> bool:
    """Check if a point is inside a circle."""
    return distance_between(point, center) <= radius


def check_collision_circles(pos1: pygame.Vector2, radius1: float, pos2: pygame.Vector2, radius2: float) -> bool:
    """Check collision between two circles."""
    return distance_between(pos1, pos2) <= radius1 + radius2 