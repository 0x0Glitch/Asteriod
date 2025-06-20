import pygame
import sys
import traceback
from src.config.constants import *
from src.config.settings import GameSettings
from src.entities import Player, Asteroid, Shot, Explosion
from src.systems import AsteroidField, GameState, CollisionSystem, InputSystem
from src.systems.input_system import InputAction
from src.assets import get_asset_manager


class AsteroidsGame:
    """Main game class that handles the game loop and coordination."""
    
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.font.init()
        
        # Load settings
        self.settings = GameSettings()
        
        # Initialize asset manager
        self.asset_manager = get_asset_manager()
        
        # Setup display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Asteroids - Production Edition")
        
        # Game clock
        self.clock = pygame.time.Clock()
        
        # Sprite groups
        self.setup_sprite_groups()
        
        # Game systems
        self.game_state = GameState()
        self.collision_system = CollisionSystem()
        self.input_system = InputSystem()
        
        # Setup input callbacks
        self.setup_input_callbacks()
        
        # Game objects
        self.asteroid_field = None
        self.player = None
        
        # Performance tracking
        self.frame_count = 0
        self.fps_timer = 0.0
        self.current_fps = 60.0
        
        # Initialize game
        self.start_new_game()
    
    def setup_sprite_groups(self):
        """Initialize all sprite groups."""
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        
        # Set up containers for sprite classes
        AsteroidField.containers = (self.updatable,)
        Asteroid.containers = (self.updatable, self.drawable, self.asteroids)
        Shot.containers = (self.updatable, self.drawable, self.shots)
        Player.containers = (self.updatable, self.drawable)
    
    def setup_input_callbacks(self):
        """Setup input system callbacks."""
        # Continuous actions
        self.input_system.register_callback(InputAction.THRUST_FORWARD, self.player_thrust_forward)
        self.input_system.register_callback(InputAction.THRUST_BACKWARD, self.player_thrust_backward)
        self.input_system.register_callback(InputAction.TURN_LEFT, self.player_turn_left)
        self.input_system.register_callback(InputAction.TURN_RIGHT, self.player_turn_right)
        self.input_system.register_callback(InputAction.SHOOT, self.player_shoot)
        
        # Single actions
        self.input_system.register_callback(InputAction.PAUSE, self.toggle_pause)
        self.input_system.register_callback(InputAction.RESTART, self.restart_game)
        self.input_system.register_callback(InputAction.QUIT, self.quit_game)
        self.input_system.register_callback(InputAction.BOMB, self.player_bomb)
    
    def start_new_game(self):
        """Start a new game."""
        # Clear all sprites
        for sprite in self.updatable:
            sprite.kill()
        
        # Reset game state
        self.game_state.reset_game()
        
        # Create new game objects
        self.asteroid_field = AsteroidField()
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        
        # Add to groups
        self.updatable.add(self.player)
        self.drawable.add(self.player)
        
        print("New game started!")
    
    def player_thrust_forward(self, dt=None):
        """Player thrust forward callback."""
        if self.player and not self.game_state.paused:
            if dt is not None:
                self.player.move(dt)
            else:
                self.player.move(1/60)  # Fallback dt
    
    def player_thrust_backward(self, dt=None):
        """Player thrust backward callback."""
        if self.player and not self.game_state.paused:
            if dt is not None:
                self.player.move(-dt)
            else:
                self.player.move(-1/60)  # Fallback dt
    
    def player_turn_left(self, dt=None):
        """Player turn left callback."""
        if self.player and not self.game_state.paused:
            if dt is not None:
                self.player.rotate(-dt)
            else:
                self.player.rotate(-1/60)  # Fallback dt
    
    def player_turn_right(self, dt=None):
        """Player turn right callback."""
        if self.player and not self.game_state.paused:
            if dt is not None:
                self.player.rotate(dt)
            else:
                self.player.rotate(1/60)  # Fallback dt
    
    def player_shoot(self, dt=None):
        """Player shoot callback."""
        if self.player and not self.game_state.paused:
            shot = self.player.shoot()
            if shot:
                self.game_state.stats['shots_fired'] += 1
    
    def player_bomb(self):
        """Player bomb callback."""
        if self.player and not self.game_state.paused:
            # Implement bomb logic here
            print("Bomb activated!")
    
    def toggle_pause(self):
        """Toggle pause state."""
        self.game_state.pause_toggle()
        print(f"Game {'paused' if self.game_state.paused else 'unpaused'}")
    
    def restart_game(self):
        """Restart the game."""
        if self.game_state.game_over:
            self.start_new_game()
    
    def quit_game(self):
        """Quit the game."""
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        """Handle all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            else:
                self.input_system.handle_event(event)
    
    def update_game_logic(self, dt):
        """Update all game logic."""
        if self.game_state.paused or self.game_state.game_over:
            return
        
        # Update game state
        self.game_state.update(dt)
        
        # Update input system
        self.input_system.update(dt)
        
        # Update all game objects
        self.updatable.update(dt)
        
        # Handle collisions
        self.handle_collisions()
        
        # Check for wave completion
        if len(self.asteroids) == 0 and not self.game_state.wave_complete:
            self.game_state.complete_wave()
    
    def handle_collisions(self):
        """Handle all collision detection and response."""
        # Check shot-asteroid collisions
        shot_asteroid_collisions = self.collision_system.check_collisions_between_groups(
            self.shots, self.asteroids
        )
        
        for shot, asteroid in shot_asteroid_collisions:
            # Add explosion
            self.game_state.add_explosion(asteroid.position.x, asteroid.position.y)
            
            # Add score
            score = self.game_state.add_score(asteroid.get_score_value())
            
            # Update stats
            self.game_state.stats['asteroids_destroyed'] += 1
            
            # Remove shot and split asteroid
            shot.kill()
            asteroid.split()
        
        # Check player-asteroid collisions (only if not respawning)
        if self.player and not self.player.is_respawning:
            player_asteroid_collisions = self.collision_system.check_collisions_between_groups(
                [self.player], self.asteroids
            )
            
            for player, asteroid in player_asteroid_collisions:
                if player.take_damage():
                    # Add explosion at player position
                    self.game_state.add_explosion(player.position.x, player.position.y, "large")
                    
                    # Check for game over
                    if player.lives <= 0:
                        self.game_state.set_game_over()
                        print(f"Game Over! Final Score: {self.game_state.score}")
    
    def render(self):
        """Render all game graphics."""
        # Clear screen
        self.screen.fill("black")
        
        # Draw all drawable objects
        for obj in self.drawable:
            obj.draw(self.screen)
        
        # Draw explosions
        self.game_state.draw_explosions(self.screen)
        
        # Draw UI
        self.game_state.draw_ui(self.screen, self.player)
        
        # Draw performance info if enabled
        if self.settings.debug_mode:
            self.draw_debug_info()
        
        # Update display
        pygame.display.flip()
    
    def draw_debug_info(self):
        """Draw debug information."""
        font = pygame.font.Font(None, 24)
        
        debug_info = [
            f"FPS: {self.current_fps:.1f}",
            f"Asteroids: {len(self.asteroids)}",
            f"Shots: {len(self.shots)}",
            f"Input: {self.input_system.get_input_string()}",
        ]
        
        y_offset = SCREEN_HEIGHT - 120
        for i, info in enumerate(debug_info):
            text = font.render(info, True, "green")
            self.screen.blit(text, (10, y_offset + i * 25))
    
    def update_performance_tracking(self, dt):
        """Update performance tracking."""
        self.frame_count += 1
        self.fps_timer += dt
        
        if self.fps_timer >= 1.0:  # Update FPS every second
            self.current_fps = self.frame_count / self.fps_timer
            self.frame_count = 0
            self.fps_timer = 0.0
    
    def run(self):
        """Main game loop."""
        print("Starting Asteroids Game!")
        print(f"Screen: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        print("Controls: WASD/Arrows to move, Space to shoot, P to pause, ESC to quit")
        
        dt = 0
        running = True
        
        try:
            while running:
                # Handle events
                self.handle_events()
                
                # Update game logic
                self.update_game_logic(dt)
                
                # Render graphics
                self.render()
                
                # Update performance tracking
                self.update_performance_tracking(dt)
                
                # Control frame rate
                dt = self.clock.tick(self.settings.FPS) / 1000.0
                
        except KeyboardInterrupt:
            print("\nGame interrupted by user")
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
        finally:
            pygame.quit()
            print("Game ended. Thanks for playing!")


def main():
    """Main entry point."""
    try:
        game = AsteroidsGame()
        game.run()
    except Exception as e:
        print(f"Failed to start game: {e}")
        traceback.print_exc()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())