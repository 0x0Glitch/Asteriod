"""
Tests for game systems.
"""

import unittest
import pygame
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.systems import GameState, CollisionSystem, InputSystem
from src.systems.input_system import InputAction
from src.entities import Player, Asteroid
from src.config.constants import *


class TestGameState(unittest.TestCase):
    """Test cases for game state management."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game_state = GameState()
    
    def test_initial_state(self):
        """Test initial game state."""
        self.assertEqual(self.game_state.score, 0)
        self.assertEqual(self.game_state.level, 1)
        self.assertFalse(self.game_state.game_over)
        self.assertFalse(self.game_state.paused)
        self.assertEqual(self.game_state.bonus_multiplier, 1.0)
    
    def test_score_addition(self):
        """Test score addition with multipliers."""
        initial_score = self.game_state.score
        points_added = self.game_state.add_score(100)
        
        self.assertEqual(self.game_state.score, initial_score + 100)
        self.assertEqual(points_added, 100)
        
        # Test with multiplier
        self.game_state.set_bonus_multiplier(2.0, 5.0)
        points_added = self.game_state.add_score(100)
        self.assertEqual(points_added, 200)
    
    def test_bonus_multiplier(self):
        """Test bonus multiplier mechanics."""
        self.game_state.set_bonus_multiplier(1.5, 2.0)
        self.assertEqual(self.game_state.bonus_multiplier, 1.5)
        self.assertEqual(self.game_state.bonus_timer, 2.0)
        
        # Update and check timer decreases
        self.game_state.update(1.0)
        self.assertEqual(self.game_state.bonus_timer, 1.0)
        
        # Update past timer and check multiplier resets
        self.game_state.update(2.0)
        self.assertEqual(self.game_state.bonus_multiplier, 1.0)
    
    def test_wave_progression(self):
        """Test wave/level progression."""
        initial_level = self.game_state.level
        self.game_state.complete_wave()
        
        self.assertTrue(self.game_state.wave_complete)
        
        # Simulate time passing
        self.game_state.update(3.5)  # Should trigger next wave
        self.assertEqual(self.game_state.level, initial_level + 1)
        self.assertFalse(self.game_state.wave_complete)
    
    def test_pause_toggle(self):
        """Test pause functionality."""
        self.assertFalse(self.game_state.paused)
        self.game_state.pause_toggle()
        self.assertTrue(self.game_state.paused)
        self.game_state.pause_toggle()
        self.assertFalse(self.game_state.paused)
    
    def test_game_over(self):
        """Test game over state."""
        self.assertFalse(self.game_state.game_over)
        self.game_state.set_game_over()
        self.assertTrue(self.game_state.game_over)
    
    def test_high_score_detection(self):
        """Test high score detection."""
        # Should be high score with default scores
        self.assertTrue(self.game_state.is_high_score(2000))
        self.assertFalse(self.game_state.is_high_score(100))
    
    def test_explosion_management(self):
        """Test explosion effect management."""
        initial_count = len(self.game_state.explosions)
        self.game_state.add_explosion(100, 100)
        self.assertEqual(len(self.game_state.explosions), initial_count + 1)
        
        # Update explosions over time
        for _ in range(100):  # Simulate time passing
            self.game_state.update_explosions(0.1)
        
        # Should eventually clear all explosions
        self.assertEqual(len(self.game_state.explosions), 0)


class TestCollisionSystem(unittest.TestCase):
    """Test cases for collision detection system."""
    
    @classmethod
    def setUpClass(cls):
        """Initialize pygame for testing."""
        pygame.init()
        pygame.display.set_mode((1, 1))  # Minimal display for testing
    
    def setUp(self):
        """Set up test fixtures."""
        self.collision_system = CollisionSystem()
        self.player = Player(100, 100)
        self.asteroid1 = Asteroid(100, 100, 30)  # Overlapping with player
        self.asteroid2 = Asteroid(200, 200, 20)  # Not overlapping
    
    def test_collision_detection(self):
        """Test basic collision detection."""
        # Should collide (same position, overlapping radii)
        self.assertTrue(self.collision_system.check_collision(self.player, self.asteroid1))
        
        # Should not collide (different positions)
        self.assertFalse(self.collision_system.check_collision(self.player, self.asteroid2))
    
    def test_group_collision_detection(self):
        """Test collision detection between groups."""
        group1 = pygame.sprite.Group()
        group2 = pygame.sprite.Group()
        
        group1.add(self.player)
        group2.add(self.asteroid1, self.asteroid2)
        
        collisions = self.collision_system.check_collisions_between_groups(group1, group2)
        
        # Should find one collision (player with asteroid1)
        self.assertEqual(len(collisions), 1)
        self.assertEqual(collisions[0][0], self.player)
        self.assertEqual(collisions[0][1], self.asteroid1)
    
    def test_collision_resolution(self):
        """Test collision resolution."""
        collision_info = self.collision_system.resolve_collision(self.player, self.asteroid1)
        
        self.assertIn('entity1', collision_info)
        self.assertIn('entity2', collision_info)
        self.assertIn('collision_point', collision_info)
        self.assertIn('normal', collision_info)
        self.assertIn('distance', collision_info)
    
    def test_entity_separation(self):
        """Test entity separation after collision."""
        # Place entities at exact same position
        self.asteroid1.position = self.player.position.copy()
        
        initial_distance = self.player.position.distance_to(self.asteroid1.position)
        self.collision_system.separate_entities(self.player, self.asteroid1)
        final_distance = self.player.position.distance_to(self.asteroid1.position)
        
        # Should be farther apart after separation
        self.assertGreater(final_distance, initial_distance)


class TestInputSystem(unittest.TestCase):
    """Test cases for input system."""
    
    @classmethod
    def setUpClass(cls):
        """Initialize pygame for testing."""
        pygame.init()
        pygame.display.set_mode((1, 1))  # Minimal display for testing
    
    def setUp(self):
        """Set up test fixtures."""
        self.input_system = InputSystem()
        self.callback_called = False
        self.callback_dt = None
    
    def test_callback_registration(self):
        """Test callback registration and unregistration."""
        def test_callback():
            self.callback_called = True
        
        # Register callback
        self.input_system.register_callback(InputAction.SHOOT, test_callback)
        self.assertIn(InputAction.SHOOT, self.input_system.action_callbacks)
        
        # Unregister callback
        self.input_system.unregister_callback(InputAction.SHOOT)
        self.assertNotIn(InputAction.SHOOT, self.input_system.action_callbacks)
    
    def test_key_mapping(self):
        """Test key mapping functionality."""
        # Test default mapping
        self.assertEqual(self.input_system.key_mappings[pygame.K_w], InputAction.THRUST_FORWARD)
        
        # Test remapping
        self.input_system.remap_key(pygame.K_t, InputAction.THRUST_FORWARD)
        self.assertEqual(self.input_system.key_mappings[pygame.K_t], InputAction.THRUST_FORWARD)
        
        # Test reverse lookup
        key = self.input_system.get_key_for_action(InputAction.THRUST_FORWARD)
        self.assertIsNotNone(key)
    
    def test_key_state_tracking(self):
        """Test key state tracking."""
        # Simulate key press
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w)
        self.input_system.handle_event(event)
        
        self.assertTrue(self.input_system.is_key_pressed(pygame.K_w))
        self.assertTrue(self.input_system.is_key_just_pressed(pygame.K_w))
        
        # Update to clear just_pressed state
        self.input_system.update(0.1)
        self.assertTrue(self.input_system.is_key_pressed(pygame.K_w))
        self.assertFalse(self.input_system.is_key_just_pressed(pygame.K_w))
        
        # Simulate key release
        event = pygame.event.Event(pygame.KEYUP, key=pygame.K_w)
        self.input_system.handle_event(event)
        
        self.assertFalse(self.input_system.is_key_pressed(pygame.K_w))
        self.assertTrue(self.input_system.is_key_just_released(pygame.K_w))
    
    def test_action_state_tracking(self):
        """Test action state tracking."""
        def test_callback(dt=None):
            self.callback_called = True
            self.callback_dt = dt
        
        self.input_system.register_callback(InputAction.THRUST_FORWARD, test_callback)
        
        # Simulate key press for continuous action
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w)
        self.input_system.handle_event(event)
        
        self.assertTrue(self.input_system.is_action_active(InputAction.THRUST_FORWARD))
        self.assertTrue(self.input_system.is_action_just_activated(InputAction.THRUST_FORWARD))
        
        # Update should trigger continuous callback
        self.input_system.update(0.1)
        self.assertTrue(self.callback_called)
        self.assertIsNotNone(self.callback_dt)
    
    def test_input_history(self):
        """Test input history tracking."""
        initial_history_length = len(self.input_system.get_input_history())
        
        # Simulate key press
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w)
        self.input_system.handle_event(event)
        
        history = self.input_system.get_input_history()
        self.assertGreater(len(history), initial_history_length)
        self.assertIn("w", history[-1].lower())  # Should contain the key name
    
    def test_input_reset(self):
        """Test input system reset."""
        # Simulate some input
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w)
        self.input_system.handle_event(event)
        
        self.assertTrue(self.input_system.is_key_pressed(pygame.K_w))
        self.assertGreater(len(self.input_system.get_input_history()), 0)
        
        # Reset and verify clean state
        self.input_system.reset()
        self.assertFalse(self.input_system.is_key_pressed(pygame.K_w))
        self.assertEqual(len(self.input_system.get_input_history()), 0)


if __name__ == '__main__':
    unittest.main() 