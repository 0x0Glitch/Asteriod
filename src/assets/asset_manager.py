"""
Asset Manager for the Asteroids game.
Handles loading, caching, and management of all game assets.
"""

import pygame
import os
import json
from typing import Dict, Optional, Tuple
from pathlib import Path


class AssetManager:
    """Centralized asset management system."""
    
    def __init__(self):
        self.images: Dict[str, pygame.Surface] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.fonts: Dict[str, pygame.font.Font] = {}
        
        # Asset paths
        self.base_path = Path(__file__).parent
        self.images_path = self.base_path / "images"
        self.sounds_path = self.base_path / "sounds"
        
        # Ensure directories exist
        self.images_path.mkdir(exist_ok=True)
        self.sounds_path.mkdir(exist_ok=True)
        
        # Asset definitions
        self.asset_definitions = {
            "player": {
                "type": "procedural",
                "size": (30, 30),
                "color": (255, 255, 255),
                "shape": "triangle"
            },
            "asteroid_large": {
                "type": "procedural", 
                "size": (60, 60),
                "color": (150, 150, 150),
                "shape": "lumpy_circle"
            },
            "asteroid_medium": {
                "type": "procedural",
                "size": (40, 40), 
                "color": (150, 150, 150),
                "shape": "lumpy_circle"
            },
            "asteroid_small": {
                "type": "procedural",
                "size": (20, 20),
                "color": (150, 150, 150), 
                "shape": "lumpy_circle"
            },
            "shot": {
                "type": "procedural",
                "size": (6, 6),
                "color": (255, 255, 0),
                "shape": "circle"
            },
            "explosion": {
                "type": "procedural",
                "size": (20, 20),
                "color": (255, 100, 0),
                "shape": "star"
            },
            "power_up": {
                "type": "procedural",
                "size": (24, 24),
                "color": (0, 255, 255),
                "shape": "diamond"
            }
        }
        
        # Initialize assets
        self.load_all_assets()
    
    def load_all_assets(self):
        """Load all game assets."""
        # Load or generate images
        for asset_name, definition in self.asset_definitions.items():
            if definition["type"] == "procedural":
                self.images[asset_name] = self.generate_procedural_image(asset_name, definition)
            else:
                self.load_image(asset_name, definition.get("file"))
        
        # Load fonts
        self.load_fonts()
        
        print(f"✓ Loaded {len(self.images)} images")
        print(f"✓ Loaded {len(self.fonts)} fonts")
    
    def generate_procedural_image(self, name: str, definition: dict) -> pygame.Surface:
        """Generate a procedural image based on definition."""
        size = definition["size"]
        color = definition["color"]
        shape = definition["shape"]
        
        # Create surface with per-pixel alpha
        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))  # Transparent background
        
        center_x, center_y = size[0] // 2, size[1] // 2
        
        if shape == "triangle":
            # Player ship triangle
            points = [
                (center_x, 2),  # Top point
                (center_x - 12, size[1] - 4),  # Bottom left
                (center_x + 12, size[1] - 4)   # Bottom right
            ]
            pygame.draw.polygon(surface, color, points, 2)
            
        elif shape == "lumpy_circle":
            # Lumpy asteroid
            import math
            import random
            
            # Set seed based on name for consistent generation
            random.seed(hash(name) % 1000)
            
            radius = min(size) // 2 - 2
            points = []
            num_points = 12
            
            for i in range(num_points):
                angle = (2 * math.pi * i) / num_points
                # Add some randomness to radius for lumpy effect
                r = radius + random.randint(-radius//4, radius//4)
                x = center_x + int(r * math.cos(angle))
                y = center_y + int(r * math.sin(angle))
                points.append((x, y))
            
            pygame.draw.polygon(surface, color, points, 2)
            
        elif shape == "circle":
            # Simple circle (for shots)
            radius = min(size) // 2 - 1
            pygame.draw.circle(surface, color, (center_x, center_y), radius)
            
        elif shape == "star":
            # Star shape for explosions
            import math
            
            outer_radius = min(size) // 2 - 2
            inner_radius = outer_radius // 2
            points = []
            num_points = 8
            
            for i in range(num_points * 2):
                angle = (2 * math.pi * i) / (num_points * 2)
                if i % 2 == 0:
                    r = outer_radius
                else:
                    r = inner_radius
                x = center_x + int(r * math.cos(angle))
                y = center_y + int(r * math.sin(angle))
                points.append((x, y))
            
            pygame.draw.polygon(surface, color, points)
            
        elif shape == "diamond":
            # Diamond shape for power-ups
            points = [
                (center_x, 2),  # Top
                (size[0] - 2, center_y),  # Right
                (center_x, size[1] - 2),  # Bottom
                (2, center_y)  # Left
            ]
            pygame.draw.polygon(surface, color, points, 2)
        
        # Save the generated image
        image_path = self.images_path / f"{name}.png"
        pygame.image.save(surface, str(image_path))
        
        return surface
    
    def load_image(self, name: str, filename: Optional[str] = None) -> Optional[pygame.Surface]:
        """Load an image from file."""
        if filename is None:
            filename = f"{name}.png"
        
        image_path = self.images_path / filename
        
        if image_path.exists():
            try:
                surface = pygame.image.load(str(image_path)).convert_alpha()
                self.images[name] = surface
                return surface
            except pygame.error as e:
                print(f"Warning: Could not load image {filename}: {e}")
        
        return None
    
    def load_fonts(self):
        """Load game fonts."""
        try:
            # Default system fonts
            self.fonts["small"] = pygame.font.Font(None, 24)
            self.fonts["medium"] = pygame.font.Font(None, 36)
            self.fonts["large"] = pygame.font.Font(None, 48)
            self.fonts["huge"] = pygame.font.Font(None, 72)
        except Exception as e:
            print(f"Warning: Could not load fonts: {e}")
            # Fallback to default font
            self.fonts["small"] = pygame.font.Font(None, 24)
            self.fonts["medium"] = pygame.font.Font(None, 36)
            self.fonts["large"] = pygame.font.Font(None, 48)
            self.fonts["huge"] = pygame.font.Font(None, 72)
    
    def get_image(self, name: str) -> Optional[pygame.Surface]:
        """Get an image by name."""
        return self.images.get(name)
    
    def get_font(self, name: str) -> Optional[pygame.font.Font]:
        """Get a font by name."""
        return self.fonts.get(name)
    
    def get_scaled_image(self, name: str, scale: float) -> Optional[pygame.Surface]:
        """Get a scaled version of an image."""
        original = self.get_image(name)
        if original is None:
            return None
        
        new_size = (int(original.get_width() * scale), int(original.get_height() * scale))
        return pygame.transform.scale(original, new_size)
    
    def get_rotated_image(self, name: str, angle: float) -> Optional[pygame.Surface]:
        """Get a rotated version of an image."""
        original = self.get_image(name)
        if original is None:
            return None
        
        return pygame.transform.rotate(original, angle)
    
    def create_text_surface(self, text: str, font_name: str = "medium", 
                           color: Tuple[int, int, int] = (255, 255, 255)) -> pygame.Surface:
        """Create a text surface."""
        font = self.get_font(font_name)
        if font is None:
            font = pygame.font.Font(None, 36)  # Fallback
        
        return font.render(text, True, color)
    
    def reload_assets(self):
        """Reload all assets (useful for development)."""
        self.images.clear()
        self.sounds.clear()
        self.fonts.clear()
        self.load_all_assets()
    
    def list_assets(self):
        """List all loaded assets."""
        print("=== LOADED ASSETS ===")
        print(f"Images ({len(self.images)}):")
        for name in sorted(self.images.keys()):
            print(f"  - {name}")
        print(f"Fonts ({len(self.fonts)}):")
        for name in sorted(self.fonts.keys()):
            print(f"  - {name}")


# Global asset manager instance
asset_manager = None

def get_asset_manager() -> AssetManager:
    """Get the global asset manager instance."""
    global asset_manager
    if asset_manager is None:
        asset_manager = AssetManager()
    return asset_manager 