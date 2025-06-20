"""
Game entities module for Asteroids game.
Contains all game objects like player, asteroids, shots, etc.
"""

from .base_entity import BaseEntity
from .player import Player
from .asteroid import Asteroid
from .shot import Shot
from .explosion import Explosion
from .circleshape import CircleShape

__all__ = [
    'BaseEntity',
    'Player',
    'Asteroid', 
    'Shot',
    'Explosion',
    'CircleShape'
] 