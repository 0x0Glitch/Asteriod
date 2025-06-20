#!/usr/bin/env python3
"""
Asset Viewer Tool for Asteroids Game
View and manage all game assets in a convenient interface.
"""

import pygame
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from assets import get_asset_manager
from config.constants import *

class AssetViewer:
    """Asset viewer application."""
    
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        # Setup display
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Asteroids - Asset Viewer")
        
        # Load asset manager
        self.asset_manager = get_asset_manager()
        
        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # Colors
        self.bg_color = (20, 20, 30)
        self.text_color = (255, 255, 255)
        self.highlight_color = (100, 150, 255)
        self.border_color = (100, 100, 100)
        
        # Layout
        self.margin = 20
        self.card_width = 200
        self.card_height = 180
        self.cards_per_row = 5
        
        # Asset list
        self.assets = list(self.asset_manager.images.keys())
        self.selected_asset = 0
        
        # Game clock
        self.clock = pygame.time.Clock()
        self.running = True
        
        print("Asset Viewer initialized!")
        print(f"Found {len(self.assets)} assets: {', '.join(self.assets)}")
    
    def handle_events(self):
        """Handle input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_LEFT:
                    self.selected_asset = (self.selected_asset - 1) % len(self.assets)
                elif event.key == pygame.K_RIGHT:
                    self.selected_asset = (self.selected_asset + 1) % len(self.assets)
                elif event.key == pygame.K_r:
                    # Reload assets
                    self.asset_manager.reload_assets()
                    print("Assets reloaded!")
                elif event.key == pygame.K_l:
                    # List assets
                    self.asset_manager.list_assets()
                elif event.key == pygame.K_s:
                    # Save all assets to individual files
                    self.save_all_assets()
    
    def save_all_assets(self):
        """Save all assets as individual files."""
        output_dir = Path("exported_assets")
        output_dir.mkdir(exist_ok=True)
        
        for name, surface in self.asset_manager.images.items():
            filename = output_dir / f"{name}.png"
            pygame.image.save(surface, str(filename))
            print(f"Saved {filename}")
        
        print(f"All assets exported to {output_dir}/")
    
    def draw_asset_card(self, x, y, asset_name, is_selected=False):
        """Draw an asset preview card."""
        # Card background
        card_rect = pygame.Rect(x, y, self.card_width, self.card_height)
        
        if is_selected:
            pygame.draw.rect(self.screen, self.highlight_color, card_rect, 3)
            bg_color = (40, 50, 80)
        else:
            pygame.draw.rect(self.screen, self.border_color, card_rect, 1)
            bg_color = (30, 30, 40)
        
        pygame.draw.rect(self.screen, bg_color, card_rect)
        
        # Asset image
        image = self.asset_manager.get_image(asset_name)
        if image:
            # Scale image to fit in card
            img_rect = image.get_rect()
            max_size = 120
            
            if img_rect.width > max_size or img_rect.height > max_size:
                scale = min(max_size / img_rect.width, max_size / img_rect.height)
                new_size = (int(img_rect.width * scale), int(img_rect.height * scale))
                scaled_image = pygame.transform.scale(image, new_size)
            else:
                scaled_image = image
            
            # Center image in card
            img_x = x + (self.card_width - scaled_image.get_width()) // 2
            img_y = y + 20
            self.screen.blit(scaled_image, (img_x, img_y))
            
            # Image info
            info_y = img_y + scaled_image.get_height() + 10
            size_text = f"{img_rect.width}x{img_rect.height}"
            size_surface = self.font_small.render(size_text, True, self.text_color)
            size_x = x + (self.card_width - size_surface.get_width()) // 2
            self.screen.blit(size_surface, (size_x, info_y))
        
        # Asset name
        name_surface = self.font_medium.render(asset_name, True, self.text_color)
        name_x = x + (self.card_width - name_surface.get_width()) // 2
        name_y = y + self.card_height - 30
        self.screen.blit(name_surface, (name_x, name_y))
    
    def draw_detailed_view(self):
        """Draw detailed view of selected asset."""
        if not self.assets:
            return
        
        asset_name = self.assets[self.selected_asset]
        image = self.asset_manager.get_image(asset_name)
        
        if not image:
            return
        
        # Detailed view area
        detail_x = 50
        detail_y = 500
        detail_width = 1100
        detail_height = 250
        
        # Background
        detail_rect = pygame.Rect(detail_x, detail_y, detail_width, detail_height)
        pygame.draw.rect(self.screen, (20, 30, 50), detail_rect)
        pygame.draw.rect(self.screen, self.border_color, detail_rect, 2)
        
        # Large image preview
        img_rect = image.get_rect()
        max_preview_size = 200
        
        if img_rect.width > max_preview_size or img_rect.height > max_preview_size:
            scale = min(max_preview_size / img_rect.width, max_preview_size / img_rect.height)
            preview_image = pygame.transform.scale(image, 
                (int(img_rect.width * scale), int(img_rect.height * scale)))
        else:
            # Scale up small images
            scale = min(max_preview_size / img_rect.width, max_preview_size / img_rect.height)
            if scale > 1:
                preview_image = pygame.transform.scale(image,
                    (int(img_rect.width * scale), int(img_rect.height * scale)))
            else:
                preview_image = image
        
        preview_x = detail_x + 20
        preview_y = detail_y + 20
        self.screen.blit(preview_image, (preview_x, preview_y))
        
        # Asset information
        info_x = preview_x + preview_image.get_width() + 30
        info_y = preview_y
        
        info_lines = [
            f"Asset: {asset_name}",
            f"Original Size: {img_rect.width} x {img_rect.height}",
            f"Preview Scale: {scale:.2f}x",
            f"File: {asset_name}.png",
            "",
            "Rotated Previews:"
        ]
        
        for i, line in enumerate(info_lines):
            if line:  # Skip empty lines
                text_surface = self.font_medium.render(line, True, self.text_color)
                self.screen.blit(text_surface, (info_x, info_y + i * 25))
        
        # Rotated previews
        rotation_y = info_y + len(info_lines) * 25
        for i, angle in enumerate([0, 45, 90, 135, 180, 225, 270, 315]):
            rotated = pygame.transform.rotate(image, angle)
            rot_x = info_x + i * 60
            self.screen.blit(rotated, (rot_x, rotation_y))
            
            # Angle label
            angle_text = self.font_small.render(f"{angle}°", True, self.text_color)
            angle_x = rot_x + (rotated.get_width() - angle_text.get_width()) // 2
            self.screen.blit(angle_text, (angle_x, rotation_y + rotated.get_height() + 2))
    
    def draw_instructions(self):
        """Draw usage instructions."""
        instructions = [
            "Asset Viewer - Asteroids Game",
            "",
            "Controls:",
            "← → : Navigate assets",
            "R   : Reload assets",
            "L   : List assets in console",
            "S   : Save all assets to exported_assets/",
            "ESC : Exit",
        ]
        
        y = 20
        for line in instructions:
            if line == instructions[0]:  # Title
                surface = self.font_large.render(line, True, self.highlight_color)
            elif line.startswith("Controls:"):
                surface = self.font_medium.render(line, True, self.highlight_color)
            else:
                surface = self.font_medium.render(line, True, self.text_color)
            
            self.screen.blit(surface, (20, y))
            y += 30 if line == instructions[0] else 25
    
    def render(self):
        """Render the asset viewer."""
        self.screen.fill(self.bg_color)
        
        # Draw instructions
        self.draw_instructions()
        
        # Draw asset grid
        start_y = 280
        
        for i, asset_name in enumerate(self.assets):
            row = i // self.cards_per_row
            col = i % self.cards_per_row
            
            x = self.margin + col * (self.card_width + 10)
            y = start_y + row * (self.card_height + 10)
            
            is_selected = (i == self.selected_asset)
            self.draw_asset_card(x, y, asset_name, is_selected)
        
        # Draw detailed view
        self.draw_detailed_view()
        
        pygame.display.flip()
    
    def run(self):
        """Run the asset viewer."""
        print("\n=== ASSET VIEWER STARTED ===")
        print("Use arrow keys to navigate, R to reload, S to save, ESC to exit")
        
        while self.running:
            self.handle_events()
            self.render()
            self.clock.tick(60)
        
        pygame.quit()
        print("Asset viewer closed.")


def main():
    """Main entry point."""
    try:
        viewer = AssetViewer()
        viewer.run()
    except Exception as e:
        print(f"Error running asset viewer: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main() 