"""
Game configuration settings.
All game constants and settings are centralized here for easy modification.
"""

import pygame
from enum import Enum
from typing import Tuple, Dict

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)  # Black

# Player settings
PLAYER_RADIUS = 15
PLAYER_TURN_SPEED = 300  # degrees per second
PLAYER_SPEED = 400  # pixels per second
PLAYER_ACCELERATION = 800  # pixels per second squared
PLAYER_FRICTION = 0.98  # friction coefficient
PLAYER_LIVES = 3
PLAYER_RESPAWN_TIME = 2.0  # seconds
PLAYER_INVULNERABILITY_TIME = 3.0  # seconds
PLAYER_MAX_SPEED = 600  # maximum speed limit

# Asteroid settings
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 2.0  # seconds between spawns
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ASTEROID_SPEED_RANGE = (30, 120)  # min, max speed
ASTEROID_VERTICES = 12  # for lumpy asteroids

# Weapon settings
class WeaponType(Enum):
    NORMAL = "normal"
    RAPID_FIRE = "rapid_fire"
    SPREAD_SHOT = "spread_shot"
    LASER = "laser"

WEAPON_CONFIGS = {
    WeaponType.NORMAL: {
        "radius": 3,
        "speed": 600,
        "cooldown": 0.15,
        "damage": 1,
        "color": (255, 255, 255),  # White
        "lifetime": 2.0
    },
    WeaponType.RAPID_FIRE: {
        "radius": 2,
        "speed": 700,
        "cooldown": 0.05,
        "damage": 1,
        "color": (255, 255, 0),  # Yellow
        "lifetime": 1.5
    },
    WeaponType.SPREAD_SHOT: {
        "radius": 2,
        "speed": 500,
        "cooldown": 0.3,
        "damage": 1,
        "color": (0, 255, 255),  # Cyan
        "lifetime": 2.0,
        "spread_count": 5,
        "spread_angle": 30
    },
    WeaponType.LASER: {
        "radius": 1,
        "speed": 1000,
        "cooldown": 0.8,
        "damage": 3,
        "color": (255, 0, 0),  # Red
        "lifetime": 1.0
    }
}

# Bomb settings
BOMB_RADIUS = 150
BOMB_DAMAGE = 5
BOMB_COOLDOWN = 3.0
BOMB_EXPLOSION_DURATION = 1.0

# Power-up settings
class PowerUpType(Enum):
    SHIELD = "shield"
    SPEED_BOOST = "speed_boost"
    RAPID_FIRE = "rapid_fire"
    SPREAD_SHOT = "spread_shot"
    LASER = "laser"
    EXTRA_LIFE = "extra_life"
    BOMB = "bomb"

POWER_UP_CONFIGS = {
    PowerUpType.SHIELD: {
        "duration": 10.0,
        "color": (0, 255, 0),  # Green
        "spawn_chance": 0.15
    },
    PowerUpType.SPEED_BOOST: {
        "duration": 8.0,
        "multiplier": 1.5,
        "color": (255, 165, 0),  # Orange
        "spawn_chance": 0.2
    },
    PowerUpType.RAPID_FIRE: {
        "duration": 12.0,
        "color": (255, 255, 0),  # Yellow
        "spawn_chance": 0.2
    },
    PowerUpType.SPREAD_SHOT: {
        "duration": 10.0,
        "color": (0, 255, 255),  # Cyan
        "spawn_chance": 0.15
    },
    PowerUpType.LASER: {
        "duration": 8.0,
        "color": (255, 0, 0),  # Red
        "spawn_chance": 0.1
    },
    PowerUpType.EXTRA_LIFE: {
        "color": (255, 0, 255),  # Magenta
        "spawn_chance": 0.05
    },
    PowerUpType.BOMB: {
        "color": (128, 128, 128),  # Gray
        "spawn_chance": 0.15
    }
}

POWER_UP_RADIUS = 12
POWER_UP_SPAWN_CHANCE = 0.3  # Chance when asteroid is destroyed

# Scoring system
SCORE_VALUES = {
    "large_asteroid": 20,
    "medium_asteroid": 50,
    "small_asteroid": 100,
    "power_up_collected": 10
}

# Explosion settings
EXPLOSION_DURATION = 0.8
EXPLOSION_PARTICLES = 15
EXPLOSION_SPEED_RANGE = (50, 200)

# Shield settings
SHIELD_RADIUS_MULTIPLIER = 1.8
SHIELD_ALPHA = 100
SHIELD_PULSE_SPEED = 5.0

# Colors
COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "orange": (255, 165, 0),
    "gray": (128, 128, 128),
    "dark_gray": (64, 64, 64),
    "light_gray": (192, 192, 192)
}

# UI settings
UI_FONT_SIZE = 24
UI_LARGE_FONT_SIZE = 48
UI_MARGIN = 20
UI_TEXT_COLOR = COLORS["white"]
UI_HIGHLIGHT_COLOR = COLORS["yellow"]

# Input settings
INPUT_KEYS = {
    "turn_left": pygame.K_a,
    "turn_right": pygame.K_d,
    "thrust": pygame.K_w,
    "reverse": pygame.K_s,
    "shoot": pygame.K_SPACE,
    "bomb": pygame.K_x,
    "pause": pygame.K_p,
    "restart": pygame.K_r
}

# Audio settings (for future implementation)
AUDIO_ENABLED = True
MASTER_VOLUME = 0.7
SFX_VOLUME = 0.8
MUSIC_VOLUME = 0.5


class GameSettings:
    """Centralized game settings class."""
    
    def __init__(self):
        # Display settings
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.FPS = FPS
        self.BACKGROUND_COLOR = BACKGROUND_COLOR
        
        # Player settings
        self.PLAYER_RADIUS = PLAYER_RADIUS
        self.PLAYER_TURN_SPEED = PLAYER_TURN_SPEED
        self.PLAYER_SPEED = PLAYER_SPEED
        self.PLAYER_LIVES = PLAYER_LIVES
        
        # Asteroid settings
        self.ASTEROID_MIN_RADIUS = ASTEROID_MIN_RADIUS
        self.ASTEROID_MAX_RADIUS = ASTEROID_MAX_RADIUS
        self.ASTEROID_SPAWN_RATE = ASTEROID_SPAWN_RATE
        
        # Weapon settings
        self.WEAPON_CONFIGS = WEAPON_CONFIGS
        
        # Power-up settings
        self.POWER_UP_CONFIGS = POWER_UP_CONFIGS
        
        # Scoring
        self.SCORE_VALUES = SCORE_VALUES
        
        # UI settings
        self.UI_FONT_SIZE = UI_FONT_SIZE
        self.UI_LARGE_FONT_SIZE = UI_LARGE_FONT_SIZE
        self.UI_MARGIN = UI_MARGIN
        self.UI_TEXT_COLOR = UI_TEXT_COLOR
        self.UI_HIGHLIGHT_COLOR = UI_HIGHLIGHT_COLOR
        
        # Input settings
        self.INPUT_KEYS = INPUT_KEYS
        
        # Audio settings
        self.AUDIO_ENABLED = AUDIO_ENABLED
        self.MASTER_VOLUME = MASTER_VOLUME
        self.SFX_VOLUME = SFX_VOLUME
        self.MUSIC_VOLUME = MUSIC_VOLUME
        
        # Debug settings
        self.debug_mode = False
        self.show_fps = True
        self.show_collision_boxes = False
        
        # Performance settings
        self.vsync = True
        self.fullscreen = False
    
    def toggle_debug_info(self):
        """Toggle debug information display."""
        self.debug_mode = not self.debug_mode
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        self.fullscreen = not self.fullscreen
    
    def set_volume(self, master=None, sfx=None, music=None):
        """Set volume levels."""
        if master is not None:
            self.MASTER_VOLUME = max(0.0, min(1.0, master))
        if sfx is not None:
            self.SFX_VOLUME = max(0.0, min(1.0, sfx))
        if music is not None:
            self.MUSIC_VOLUME = max(0.0, min(1.0, music)) 