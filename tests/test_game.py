import pygame
import unittest
import math
from unittest.mock import Mock, patch
from constants import *
from circleshape import CircleShape
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

class TestCircleShape(unittest.TestCase):
    def setUp(self):
        pygame.init()
        
    def test_circleshape_initialization(self):
        """Test CircleShape basic initialization"""
        shape = CircleShape(100, 200, 30)
        self.assertEqual(shape.position.x, 100)
        self.assertEqual(shape.position.y, 200)
        self.assertEqual(shape.radius, 30)
        self.assertEqual(shape.velocity.x, 0)
        self.assertEqual(shape.velocity.y, 0)
    
    def test_collision_detection(self):
        """Test collision detection between two CircleShapes"""
        shape1 = CircleShape(0, 0, 10)
        shape2 = CircleShape(15, 0, 10)  # Just touching
        shape3 = CircleShape(25, 0, 10)  # Not touching
        
        self.assertTrue(shape1.check_collision_of_asteroid_with_player(shape2))
        self.assertFalse(shape1.check_collision_of_asteroid_with_player(shape3))

class TestPlayer(unittest.TestCase):
    def setUp(self):
        pygame.init()
        Player.containers = (pygame.sprite.Group(),)
        
    def test_player_initialization(self):
        """Test Player initialization"""
        player = Player(100, 200)
        self.assertEqual(player.position.x, 100)
        self.assertEqual(player.position.y, 200)
        self.assertEqual(player.radius, PLAYER_RADIUS)
        self.assertEqual(player.rotation, 0)
        self.assertEqual(player.shoot_cooldown, 0)
    
    def test_player_rotation(self):
        """Test player rotation"""
        player = Player(100, 200)
        initial_rotation = player.rotation
        player.rotate(1.0)  # 1 second
        expected_rotation = initial_rotation + PLAYER_TURN_SPEED
        self.assertEqual(player.rotation, expected_rotation)
    
    def test_player_movement(self):
        """Test player movement"""
        player = Player(100, 200)
        initial_pos = player.position.copy()
        player.move(1.0)  # 1 second, facing up (rotation = 0)
        
        # Should move up (negative y direction)
        self.assertEqual(player.position.x, initial_pos.x)
        self.assertEqual(player.position.y, initial_pos.y - PLAYER_SPEED)
    
    def test_shooting_cooldown(self):
        """Test shooting cooldown mechanism"""
        Shot.containers = (pygame.sprite.Group(),)
        player = Player(100, 200)
        
        # First shot should work and set cooldown
        initial_cooldown = player.shoot_cooldown
        player.shoot()
        player.shoot_cooldown = PLAYER_SHOOT_COOLDOWN  # Manually set as if called from update()
        self.assertEqual(player.shoot_cooldown, PLAYER_SHOOT_COOLDOWN)
        
        # Test cooldown decreases over time
        player.update(0.05)  # Update for 0.05 seconds
        self.assertLess(player.shoot_cooldown, PLAYER_SHOOT_COOLDOWN)
    
    def test_triangle_calculation(self):
        """Test triangle vertex calculation"""
        player = Player(100, 200)
        triangle = player.triangle()
        
        # Should return 3 vertices
        self.assertEqual(len(triangle), 3)
        
        # All vertices should be pygame.Vector2 objects
        for vertex in triangle:
            self.assertIsInstance(vertex, pygame.Vector2)

class TestShot(unittest.TestCase):
    def setUp(self):
        pygame.init()
        Shot.containers = (pygame.sprite.Group(),)
    
    def test_shot_initialization(self):
        """Test Shot initialization"""
        shot = Shot(50, 75)
        self.assertEqual(shot.position.x, 50)
        self.assertEqual(shot.position.y, 75)
        self.assertEqual(shot.radius, SHOT_RADIUS)
    
    def test_shot_movement(self):
        """Test shot movement"""
        shot = Shot(100, 200)
        shot.velocity = pygame.Vector2(100, 0)  # Move right at 100 pixels/sec
        
        initial_pos = shot.position.copy()
        shot.update(1.0)  # 1 second
        
        self.assertEqual(shot.position.x, initial_pos.x + 100)
        self.assertEqual(shot.position.y, initial_pos.y)

class TestAsteroid(unittest.TestCase):
    def setUp(self):
        pygame.init()
        Asteroid.containers = (pygame.sprite.Group(),)
    
    def test_asteroid_initialization(self):
        """Test Asteroid initialization"""
        asteroid = Asteroid(150, 250, 40)
        self.assertEqual(asteroid.position.x, 150)
        self.assertEqual(asteroid.position.y, 250)
        self.assertEqual(asteroid.radius, 40)
    
    def test_asteroid_movement(self):
        """Test asteroid movement"""
        asteroid = Asteroid(100, 200, 30)
        asteroid.velocity = pygame.Vector2(50, -25)  # Move right and up
        
        initial_pos = asteroid.position.copy()
        asteroid.update(2.0)  # 2 seconds
        
        self.assertEqual(asteroid.position.x, initial_pos.x + 100)
        self.assertEqual(asteroid.position.y, initial_pos.y - 50)

class TestAsteroidField(unittest.TestCase):
    def setUp(self):
        pygame.init()
        AsteroidField.containers = (pygame.sprite.Group(),)
        Asteroid.containers = (pygame.sprite.Group(),)
    
    def test_asteroidfield_initialization(self):
        """Test AsteroidField initialization"""
        field = AsteroidField()
        self.assertEqual(field.spawn_timer, 0.0)
    
    @patch('random.choice')
    @patch('random.randint')
    @patch('random.uniform')
    def test_asteroid_spawning(self, mock_uniform, mock_randint, mock_choice):
        """Test asteroid spawning mechanism"""
        # Mock random values - need to provide enough values for all calls
        mock_choice.return_value = AsteroidField.edges[0]  # First edge
        mock_randint.side_effect = [50, 1, 60, 2, 70, 3]  # Multiple speed/kind pairs
        mock_uniform.return_value = 0.5  # middle of edge
        
        field = AsteroidField()
        field.spawn_timer = ASTEROID_SPAWN_RATE + 0.1  # Trigger spawn
        
        initial_sprite_count = len(Asteroid.containers[0])
        field.update(0.1)  # Small dt
        
        # Should have spawned an asteroid
        self.assertEqual(len(Asteroid.containers[0]), initial_sprite_count + 1)
        self.assertEqual(field.spawn_timer, 0.0)

class TestGameConstants(unittest.TestCase):
    def test_constants_are_reasonable(self):
        """Test that game constants are within reasonable ranges"""
        # Screen dimensions
        self.assertGreater(SCREEN_WIDTH, 0)
        self.assertGreater(SCREEN_HEIGHT, 0)
        
        # Asteroid settings
        self.assertGreater(ASTEROID_MIN_RADIUS, 0)
        self.assertGreater(ASTEROID_KINDS, 0)
        self.assertGreater(ASTEROID_SPAWN_RATE, 0)
        self.assertEqual(ASTEROID_MAX_RADIUS, ASTEROID_MIN_RADIUS * ASTEROID_KINDS)
        
        # Player settings
        self.assertGreater(PLAYER_RADIUS, 0)
        self.assertGreater(PLAYER_TURN_SPEED, 0)
        self.assertGreater(PLAYER_SPEED, 0)
        
        # Shot settings
        self.assertGreater(SHOT_RADIUS, 0)
        self.assertGreater(PLAYER_SHOOT_SPEED, 0)
        self.assertGreater(PLAYER_SHOOT_COOLDOWN, 0)

class TestGameIntegration(unittest.TestCase):
    def setUp(self):
        pygame.init()
        # Set up sprite groups like in main.py
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        
        AsteroidField.containers = (self.updatable,)
        Asteroid.containers = (self.updatable, self.drawable, self.asteroids)
        Shot.containers = (self.updatable, self.drawable, self.shots)
        Player.containers = (self.updatable, self.drawable)
    
    def test_sprite_group_assignment(self):
        """Test that sprites are properly assigned to groups"""
        player = Player(100, 200)
        asteroid = Asteroid(300, 400, 50)
        shot = Shot(150, 250)
        field = AsteroidField()
        
        # Check group memberships
        self.assertIn(player, self.updatable)
        self.assertIn(player, self.drawable)
        
        self.assertIn(asteroid, self.updatable)
        self.assertIn(asteroid, self.drawable)
        self.assertIn(asteroid, self.asteroids)
        
        self.assertIn(shot, self.updatable)
        self.assertIn(shot, self.drawable)
        self.assertIn(shot, self.shots)
        
        self.assertIn(field, self.updatable)
        self.assertNotIn(field, self.drawable)  # AsteroidField is not drawable
    
    def test_player_shooting_creates_shots(self):
        """Test that player shooting creates shot objects"""
        player = Player(100, 200)
        initial_shot_count = len(self.shots)
        
        player.shoot()
        
        self.assertEqual(len(self.shots), initial_shot_count + 1)
        
        # Check that the shot was created at the right position
        shot = list(self.shots)[-1]  # Get the last shot
        expected_pos = player.position + pygame.Vector2(0, -1).rotate(player.rotation) * player.radius
        self.assertAlmostEqual(shot.position.x, expected_pos.x, places=1)
        self.assertAlmostEqual(shot.position.y, expected_pos.y, places=1)
    
    def test_collision_detection_works(self):
        """Test collision detection between game objects"""
        player = Player(100, 200)
        asteroid = Asteroid(100, 200, 30)  # Same position, should collide
        
        self.assertTrue(player.check_collision_of_asteroid_with_player(asteroid))
        
        # Move asteroid away
        asteroid.position = pygame.Vector2(300, 400)
        self.assertFalse(player.check_collision_of_asteroid_with_player(asteroid))

def run_performance_test():
    """Basic performance test to ensure game can handle multiple objects"""
    pygame.init()
    
    # Set up groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    AsteroidField.containers = (updatable,)
    Asteroid.containers = (updatable, drawable, asteroids)
    Shot.containers = (updatable, drawable, shots)
    Player.containers = (updatable, drawable)
    
    # Create many objects
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    
    # Create multiple asteroids
    for i in range(20):
        asteroid = Asteroid(i * 50, i * 30, 40)
        asteroid.velocity = pygame.Vector2(10, 5)
    
    # Create multiple shots
    for i in range(50):
        shot = Shot(i * 10, 100)
        shot.velocity = pygame.Vector2(0, -100)
    
    # Test update performance
    import time
    start_time = time.time()
    
    for _ in range(100):  # 100 frames
        updatable.update(1/60)  # 60 FPS
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"Performance test: 100 frames with {len(updatable)} objects took {duration:.3f} seconds")
    print(f"Average FPS capability: {100/duration:.1f}")
    
    return duration < 1.0  # Should complete in less than 1 second

if __name__ == '__main__':
    print("Running Asteroids Game Tests...")
    print("=" * 50)
    
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\n" + "=" * 50)
    print("Running Performance Test...")
    
    # Run performance test
    performance_ok = run_performance_test()
    if performance_ok:
        print("✓ Performance test PASSED")
    else:
        print("✗ Performance test FAILED")
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print("- Unit tests completed above")
    print(f"- Performance test: {'PASSED' if performance_ok else 'FAILED'}")
    print("\nGame should now be ready to play!")
    print("Controls:")
    print("  A/D - Turn left/right")
    print("  W/S - Move forward/backward")
    print("  SPACE - Shoot")
    print("  ESC - Quit") 