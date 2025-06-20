"""
Game state management system for the Asteroids game.
Handles game logic, scoring, lives, and game flow.
"""

import pygame
from enum import Enum
from typing import List, Dict, Any
from ..entities.explosion import Explosion


class GamePhase(Enum):
    """Different phases of the game."""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    HIGH_SCORE = "high_score"


class GameState:
    """Manages the overall game state and flow."""
    
    def __init__(self):
        self.reset_game()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        self.explosions = []
        self.phase = GamePhase.PLAYING
        self.high_scores = self.load_high_scores()
        
        # Game statistics
        self.stats = {
            'shots_fired': 0,
            'asteroids_destroyed': 0,
            'accuracy': 0.0,
            'time_played': 0.0,
            'power_ups_collected': 0
        }
    
    def reset_game(self):
        """Reset game state for a new game."""
        self.score = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.wave_complete = False
        self.wave_timer = 0.0
        self.bonus_multiplier = 1.0
        self.bonus_timer = 0.0
        
        # Reset statistics
        self.stats = {
            'shots_fired': 0,
            'asteroids_destroyed': 0,
            'accuracy': 0.0,
            'time_played': 0.0,
            'power_ups_collected': 0
        }
    
    def update(self, dt: float):
        """Update game state logic."""
        if self.phase == GamePhase.PLAYING and not self.paused:
            self.stats['time_played'] += dt
            
            # Update bonus multiplier
            if self.bonus_timer > 0:
                self.bonus_timer -= dt
                if self.bonus_timer <= 0:
                    self.bonus_multiplier = 1.0
            
            # Update wave timer
            if self.wave_complete:
                self.wave_timer += dt
                if self.wave_timer >= 3.0:  # 3 second delay between waves
                    self.start_next_wave()
        
        # Update explosions
        self.update_explosions(dt)
        
        # Update accuracy
        if self.stats['shots_fired'] > 0:
            self.stats['accuracy'] = (self.stats['asteroids_destroyed'] / self.stats['shots_fired']) * 100
    
    def add_score(self, points: int):
        """Add points to the score with multiplier."""
        bonus_points = int(points * self.bonus_multiplier)
        self.score += bonus_points
        return bonus_points
    
    def set_bonus_multiplier(self, multiplier: float, duration: float):
        """Set a temporary score multiplier."""
        self.bonus_multiplier = multiplier
        self.bonus_timer = duration
    
    def start_next_wave(self):
        """Start the next wave/level."""
        self.level += 1
        self.wave_complete = False
        self.wave_timer = 0.0
        
        # Bonus points for completing a wave
        wave_bonus = self.level * 100
        self.add_score(wave_bonus)
    
    def complete_wave(self):
        """Mark the current wave as complete."""
        self.wave_complete = True
        self.wave_timer = 0.0
    
    def pause_toggle(self):
        """Toggle pause state."""
        if self.phase == GamePhase.PLAYING:
            self.paused = not self.paused
    
    def set_game_over(self):
        """Set the game to game over state."""
        self.game_over = True
        self.phase = GamePhase.GAME_OVER
        
        # Check if it's a high score
        if self.is_high_score(self.score):
            self.phase = GamePhase.HIGH_SCORE
    
    def is_high_score(self, score: int) -> bool:
        """Check if the given score is a high score."""
        # If we have fewer than 10 scores, only consider it a high score if it's better than existing scores
        if len(self.high_scores) < 10:
            if len(self.high_scores) == 0:
                return True  # First score is always a high score
            return score > min(self.high_scores)
        return score > min(self.high_scores)
    
    def add_high_score(self, score: int, name: str = "PLAYER"):
        """Add a new high score."""
        self.high_scores.append(score)
        self.high_scores.sort(reverse=True)
        if len(self.high_scores) > 10:
            self.high_scores = self.high_scores[:10]
        self.save_high_scores()
    
    def load_high_scores(self) -> List[int]:
        """Load high scores from file."""
        try:
            with open('high_scores.txt', 'r') as f:
                scores = [int(line.strip()) for line in f.readlines()]
                return sorted(scores, reverse=True)[:10]
        except (FileNotFoundError, ValueError):
            return [1000, 800, 600, 400, 200]  # Default high scores
    
    def save_high_scores(self):
        """Save high scores to file."""
        try:
            with open('high_scores.txt', 'w') as f:
                for score in self.high_scores:
                    f.write(f"{score}\n")
        except IOError:
            pass  # Fail silently if we can't save
    
    def add_explosion(self, x: float, y: float, size: str = "normal"):
        """Add an explosion effect."""
        self.explosions.append(Explosion(x, y, size))
    
    def update_explosions(self, dt: float):
        """Update all explosion effects."""
        for explosion in self.explosions[:]:
            explosion.update(dt)
            if explosion.is_finished():
                self.explosions.remove(explosion)
    
    def draw_explosions(self, screen: pygame.Surface):
        """Draw all explosion effects."""
        for explosion in self.explosions:
            explosion.draw(screen)
    
    def draw_ui(self, screen: pygame.Surface, player):
        """Draw the game UI."""
        # Draw score
        score_text = self.font.render(f"Score: {self.score:,}", True, "white")
        screen.blit(score_text, (10, 10))
        
        # Draw level
        level_text = self.font.render(f"Level: {self.level}", True, "white")
        screen.blit(level_text, (10, 50))
        
        # Draw lives
        if player:
            lives_text = self.font.render(f"Lives: {player.lives}", True, "white")
            screen.blit(lives_text, (10, 90))
        
        # Draw bonus multiplier if active
        if self.bonus_multiplier > 1.0:
            multiplier_text = self.font.render(f"Bonus: x{self.bonus_multiplier:.1f}", True, "yellow")
            screen.blit(multiplier_text, (10, 130))
        
        # Draw pause indicator
        if self.paused:
            pause_text = self.large_font.render("PAUSED", True, "yellow")
            pause_rect = pause_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
            screen.blit(pause_text, pause_rect)
        
        # Draw wave complete message
        if self.wave_complete:
            wave_text = self.font.render(f"Wave {self.level-1} Complete! Next wave in {3.0-self.wave_timer:.1f}s", True, "green")
            wave_rect = wave_text.get_rect(center=(screen.get_width()//2, 100))
            screen.blit(wave_text, wave_rect)
        
        # Draw game over screen
        if self.phase == GamePhase.GAME_OVER:
            self.draw_game_over_screen(screen)
        elif self.phase == GamePhase.HIGH_SCORE:
            self.draw_high_score_screen(screen)
    
    def draw_game_over_screen(self, screen: pygame.Surface):
        """Draw the game over screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.large_font.render("GAME OVER", True, "red")
        game_over_rect = game_over_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 100))
        screen.blit(game_over_text, game_over_rect)
        
        # Final score
        final_score_text = self.font.render(f"Final Score: {self.score:,}", True, "white")
        score_rect = final_score_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 50))
        screen.blit(final_score_text, score_rect)
        
        # Statistics
        stats_y = screen.get_height()//2
        stats_texts = [
            f"Asteroids Destroyed: {self.stats['asteroids_destroyed']}",
            f"Shots Fired: {self.stats['shots_fired']}",
            f"Accuracy: {self.stats['accuracy']:.1f}%",
            f"Time Played: {self.stats['time_played']:.1f}s",
            f"Level Reached: {self.level}"
        ]
        
        for i, stat_text in enumerate(stats_texts):
            text = self.font.render(stat_text, True, "white")
            text_rect = text.get_rect(center=(screen.get_width()//2, stats_y + i * 30))
            screen.blit(text, text_rect)
        
        # Restart instruction
        restart_text = self.font.render("Press R to restart or ESC to quit", True, "yellow")
        restart_rect = restart_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 200))
        screen.blit(restart_text, restart_rect)
    
    def draw_high_score_screen(self, screen: pygame.Surface):
        """Draw the high score entry screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # High score text
        high_score_text = self.large_font.render("NEW HIGH SCORE!", True, "gold")
        high_score_rect = high_score_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 100))
        screen.blit(high_score_text, high_score_rect)
        
        # Score
        score_text = self.font.render(f"Score: {self.score:,}", True, "white")
        score_rect = score_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 50))
        screen.blit(score_text, score_rect)
        
        # Instructions
        instruction_text = self.font.render("Press R to continue", True, "white")
        instruction_rect = instruction_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 50))
        screen.blit(instruction_text, instruction_rect) 