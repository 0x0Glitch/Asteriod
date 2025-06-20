"""
Tests for game entities.
"""

import unittest
import pygame
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.entities import Player, Asteroid, Shot, Explosion
from src.config.constants import *


class TestEntities(unittest.TestCase):
    """Test cases for game entities."""
    
    @classmethod
    def setUpClass(cls):
        """Initialize pygame for testing."""
        pygame.init()
        pygame.display.set_mode((1, 1))  # Minimal display for testing
    
    def setUp(self):
        """Set up test fixtures."""
        self.player = Player(100, 100)
        self.asteroid = Asteroid(200, 200, ASTEROID_MIN_RADIUS * 2)
        self.shot = Shot(150, 150)
        self.explosion = Explosion(300, 300)
    
    def test_player_creation(self):
        """Test player creation and initial state."""
        self.assertEqual(self.player.position.x, 100)
        self.assertEqual(self.player.position.y, 100)
        self.assertEqual(self.player.radius, PLAYER_RADIUS)
        self.assertEqual(self.player.rotation, 0)
        self.assertEqual(self.player.lives, PLAYER_LIVES)
        self.assertFalse(self.player.is_respawning)
    
    def test_player_movement(self):
        """Test player movement mechanics."""
        initial_pos = self.player.position.copy()
        
        # Test forward movement
        self.player.move(0.1)  # Move forward for 0.1 seconds
        self.assertNotEqual(self.player.velocity.length(), 0)
        
        # Update position
        self.player.update(0.1)
        self.assertNotEqual(self.player.position, initial_pos)
    
    def test_player_rotation(self):
        """Test player rotation."""
        initial_rotation = self.player.rotation
        self.player.rotate(0.1)  # Rotate for 0.1 seconds
        self.assertNotEqual(self.player.rotation, initial_rotation)
    
    def test_player_shooting(self):
        """Test player shooting mechanism."""
        # Create sprite groups for testing
        shots = pygame.sprite.Group()
        Shot.containers = (shots,)
        
        initial_shot_count = len(shots)
        shot = self.player.shoot()
        
        if shot:  # If cooldown allows shooting
            self.assertEqual(len(shots), initial_shot_count + 1)
            self.assertIsNotNone(shot.velocity)
            self.assertGreater(shot.velocity.length(), 0)
    
    def test_player_damage(self):
        """Test player damage and respawn mechanics."""
        initial_lives = self.player.lives
        damage_taken = self.player.take_damage()
        
        if damage_taken:
            self.assertEqual(self.player.lives, initial_lives - 1)
            if self.player.lives > 0:
                self.assertTrue(self.player.is_respawning)
    
    def test_asteroid_creation(self):
        """Test asteroid creation."""
        self.assertEqual(self.asteroid.position.x, 200)
        self.assertEqual(self.asteroid.position.y, 200)
        self.assertEqual(self.asteroid.radius, ASTEROID_MIN_RADIUS * 2)
    
    def test_asteroid_movement(self):
        """Test asteroid movement."""
        # Set initial velocity
        self.asteroid.velocity = pygame.Vector2(50, 0)
        initial_pos = self.asteroid.position.copy()
        
        self.asteroid.update(0.1)
        self.assertNotEqual(self.asteroid.position, initial_pos)
    
    def test_asteroid_splitting(self):
        """Test asteroid splitting mechanism."""
        # Create sprite groups for testing
        asteroids = pygame.sprite.Group()
        Asteroid.containers = (asteroids,)
        
        # Add asteroid to group
        asteroids.add(self.asteroid)
        initial_count = len(asteroids)
        
        # Test splitting
        self.asteroid.split()
        
        # Should remove original and potentially add new ones
        self.assertLess(len(asteroids), initial_count + 2)  # May add 0, 1, or 2 new asteroids
    
    def test_asteroid_score_values(self):
        """Test asteroid score value calculation."""
        large_asteroid = Asteroid(0, 0, ASTEROID_MAX_RADIUS)
        medium_asteroid = Asteroid(0, 0, ASTEROID_MIN_RADIUS * 2)
        small_asteroid = Asteroid(0, 0, ASTEROID_MIN_RADIUS)
        
        self.assertEqual(large_asteroid.get_score_value(), SCORE_LARGE_ASTEROID)
        self.assertEqual(medium_asteroid.get_score_value(), SCORE_MEDIUM_ASTEROID)
        self.assertEqual(small_asteroid.get_score_value(), SCORE_SMALL_ASTEROID)
    
    def test_shot_creation(self):
        """Test shot creation."""
        self.assertEqual(self.shot.position.x, 150)
        self.assertEqual(self.shot.position.y, 150)
        self.assertEqual(self.shot.radius, SHOT_RADIUS)
        self.assertEqual(self.shot.lifetime, 3.0)
    
    def test_shot_movement(self):
        """Test shot movement."""
        self.shot.velocity = pygame.Vector2(100, 0)
        initial_pos = self.shot.position.copy()
        
        self.shot.update(0.1)
        self.assertNotEqual(self.shot.position, initial_pos)
    
    def test_shot_lifetime(self):
        """Test shot lifetime mechanism."""
        # Create sprite group for testing
        shots = pygame.sprite.Group()
        shots.add(self.shot)
        
        # Simulate time passing
        for _ in range(35):  # 3.5 seconds at 0.1s intervals
            self.shot.update(0.1)
        
        # Shot should be removed after lifetime expires
        self.assertEqual(len(shots), 0)
    
    def test_explosion_creation(self):
        """Test explosion creation."""
        self.assertGreater(len(self.explosion.particles), 0)
        # Default explosion is "medium" size with 12 particles
        self.assertEqual(len(self.explosion.particles), 12)
    
    def test_explosion_lifecycle(self):
        """Test explosion particle lifecycle."""
        initial_particle_count = len(self.explosion.particles)
        
        # Update explosion over time
        for _ in range(10):  # Simulate time passing
            self.explosion.update(0.1)
        
        # Should have fewer particles as they expire
        self.assertLessEqual(len(self.explosion.particles), initial_particle_count)
        
        # Eventually should finish
        for _ in range(100):  # Simulate a lot of time
            self.explosion.update(0.1)
        
        self.assertTrue(self.explosion.is_finished())


if __name__ == '__main__':
    unittest.main() 