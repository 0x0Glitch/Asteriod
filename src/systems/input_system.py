"""
Input system for the Asteroids game.
Handles all keyboard and mouse input processing.
"""

import pygame
from typing import Dict, Set, Callable, Optional
from enum import Enum


class InputAction(Enum):
    """Available input actions in the game."""
    THRUST_FORWARD = "thrust_forward"
    THRUST_BACKWARD = "thrust_backward"
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"
    SHOOT = "shoot"
    BOMB = "bomb"
    PAUSE = "pause"
    RESTART = "restart"
    QUIT = "quit"
    SHIELD = "shield"


class InputSystem:
    """Handles input processing and key mapping."""
    
    def __init__(self):
        # Default key mappings
        self.key_mappings = {
            pygame.K_w: InputAction.THRUST_FORWARD,
            pygame.K_s: InputAction.THRUST_BACKWARD,
            pygame.K_a: InputAction.TURN_LEFT,
            pygame.K_d: InputAction.TURN_RIGHT,
            pygame.K_SPACE: InputAction.SHOOT,
            pygame.K_x: InputAction.BOMB,
            pygame.K_p: InputAction.PAUSE,
            pygame.K_r: InputAction.RESTART,
            pygame.K_ESCAPE: InputAction.QUIT,
            pygame.K_LSHIFT: InputAction.SHIELD,
            pygame.K_RSHIFT: InputAction.SHIELD,
        }
        
        # Alternative WASD + Arrow keys support
        self.alternative_mappings = {
            pygame.K_UP: InputAction.THRUST_FORWARD,
            pygame.K_DOWN: InputAction.THRUST_BACKWARD,
            pygame.K_LEFT: InputAction.TURN_LEFT,
            pygame.K_RIGHT: InputAction.TURN_RIGHT,
        }
        
        # Combine mappings
        self.key_mappings.update(self.alternative_mappings)
        
        # Action callbacks
        self.action_callbacks: Dict[InputAction, Callable] = {}
        self.continuous_actions: Set[InputAction] = {
            InputAction.THRUST_FORWARD,
            InputAction.THRUST_BACKWARD,
            InputAction.TURN_LEFT,
            InputAction.TURN_RIGHT,
            InputAction.SHOOT,
            InputAction.SHIELD
        }
        
        # Input state tracking
        self.pressed_keys: Set[int] = set()
        self.just_pressed: Set[int] = set()
        self.just_released: Set[int] = set()
        
        # Action state tracking
        self.active_actions: Set[InputAction] = set()
        self.just_activated: Set[InputAction] = set()
        self.just_deactivated: Set[InputAction] = set()
        
        # Input history for debugging
        self.input_history = []
        self.max_history = 100
    
    def register_callback(self, action: InputAction, callback: Callable):
        """Register a callback function for an input action."""
        self.action_callbacks[action] = callback
    
    def unregister_callback(self, action: InputAction):
        """Unregister a callback function for an input action."""
        if action in self.action_callbacks:
            del self.action_callbacks[action]
    
    def remap_key(self, key: int, action: InputAction):
        """Remap a key to a different action."""
        self.key_mappings[key] = action
    
    def get_key_for_action(self, action: InputAction) -> Optional[int]:
        """Get the primary key mapped to an action."""
        for key, mapped_action in self.key_mappings.items():
            if mapped_action == action:
                return key
        return None
    
    def handle_event(self, event: pygame.event.Event):
        """Process a pygame event."""
        if event.type == pygame.KEYDOWN:
            self.just_pressed.add(event.key)
            self.pressed_keys.add(event.key)
            
            # Track input history
            self.input_history.append(f"KEY_DOWN: {pygame.key.name(event.key)}")
            if len(self.input_history) > self.max_history:
                self.input_history.pop(0)
            
            # Handle single-press actions
            if event.key in self.key_mappings:
                action = self.key_mappings[event.key]
                if action not in self.continuous_actions:
                    self.trigger_action(action)
                else:
                    self.active_actions.add(action)
                    self.just_activated.add(action)
        
        elif event.type == pygame.KEYUP:
            if event.key in self.pressed_keys:
                self.pressed_keys.remove(event.key)
            self.just_released.add(event.key)
            
            # Handle continuous action release
            if event.key in self.key_mappings:
                action = self.key_mappings[event.key]
                if action in self.active_actions:
                    self.active_actions.remove(action)
                    self.just_deactivated.add(action)
    
    def update(self, dt: float):
        """Update input system state."""
        # Process continuous actions
        for action in self.active_actions:
            self.trigger_action(action, continuous=True, dt=dt)
        
        # Clear frame-specific state
        self.just_pressed.clear()
        self.just_released.clear()
        self.just_activated.clear()
        self.just_deactivated.clear()
    
    def trigger_action(self, action: InputAction, continuous: bool = False, dt: float = 0.0):
        """Trigger an action callback if registered."""
        if action in self.action_callbacks:
            callback = self.action_callbacks[action]
            if continuous:
                # Pass dt for continuous actions
                try:
                    callback(dt)
                except TypeError:
                    # Fallback for callbacks that don't accept dt
                    callback()
            else:
                callback()
    
    def is_action_active(self, action: InputAction) -> bool:
        """Check if an action is currently active."""
        return action in self.active_actions
    
    def is_action_just_activated(self, action: InputAction) -> bool:
        """Check if an action was just activated this frame."""
        return action in self.just_activated
    
    def is_action_just_deactivated(self, action: InputAction) -> bool:
        """Check if an action was just deactivated this frame."""
        return action in self.just_deactivated
    
    def is_key_pressed(self, key: int) -> bool:
        """Check if a key is currently pressed."""
        return key in self.pressed_keys
    
    def is_key_just_pressed(self, key: int) -> bool:
        """Check if a key was just pressed this frame."""
        return key in self.just_pressed
    
    def is_key_just_released(self, key: int) -> bool:
        """Check if a key was just released this frame."""
        return key in self.just_released
    
    def get_input_string(self) -> str:
        """Get a string representation of current input state."""
        active_keys = [pygame.key.name(key) for key in self.pressed_keys]
        active_actions = [action.value for action in self.active_actions]
        return f"Keys: {', '.join(active_keys)} | Actions: {', '.join(active_actions)}"
    
    def get_input_history(self) -> list:
        """Get the input history for debugging."""
        return self.input_history.copy()
    
    def clear_input_history(self):
        """Clear the input history."""
        self.input_history.clear()
    
    def reset(self):
        """Reset all input state."""
        self.pressed_keys.clear()
        self.just_pressed.clear()
        self.just_released.clear()
        self.active_actions.clear()
        self.just_activated.clear()
        self.just_deactivated.clear()
        self.clear_input_history() 