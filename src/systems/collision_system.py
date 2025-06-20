"""
Collision detection system for the Asteroids game.
Handles all collision logic between game entities.
"""

import pygame
from typing import List, Tuple, Optional
from ..entities.base_entity import BaseEntity


class CollisionSystem:
    """Handles collision detection between game entities."""
    
    def __init__(self):
        self.collision_pairs = []
    
    def check_collision(self, entity1: BaseEntity, entity2: BaseEntity) -> bool:
        """
        Check if two circular entities are colliding.
        
        Args:
            entity1: First entity to check
            entity2: Second entity to check
            
        Returns:
            True if entities are colliding, False otherwise
        """
        if not hasattr(entity1, 'position') or not hasattr(entity2, 'position'):
            return False
        if not hasattr(entity1, 'radius') or not hasattr(entity2, 'radius'):
            return False
            
        distance = entity1.position.distance_to(entity2.position)
        return distance <= (entity1.radius + entity2.radius)
    
    def check_collisions_between_groups(self, group1: pygame.sprite.Group, 
                                      group2: pygame.sprite.Group) -> List[Tuple]:
        """
        Check collisions between all entities in two groups.
        
        Args:
            group1: First group of entities
            group2: Second group of entities
            
        Returns:
            List of collision pairs (entity1, entity2)
        """
        collisions = []
        for entity1 in group1:
            for entity2 in group2:
                if entity1 != entity2 and self.check_collision(entity1, entity2):
                    collisions.append((entity1, entity2))
        return collisions
    
    def check_collisions_within_group(self, group: pygame.sprite.Group) -> List[Tuple]:
        """
        Check collisions between all entities within a single group.
        
        Args:
            group: Group of entities to check
            
        Returns:
            List of collision pairs (entity1, entity2)
        """
        collisions = []
        entities = list(group)
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i+1:]:
                if self.check_collision(entity1, entity2):
                    collisions.append((entity1, entity2))
        return collisions
    
    def resolve_collision(self, entity1: BaseEntity, entity2: BaseEntity) -> dict:
        """
        Resolve collision between two entities and return collision info.
        
        Args:
            entity1: First entity in collision
            entity2: Second entity in collision
            
        Returns:
            Dictionary with collision information
        """
        collision_info = {
            'entity1': entity1,
            'entity2': entity2,
            'collision_point': (entity1.position + entity2.position) / 2,
            'distance': entity1.position.distance_to(entity2.position)
        }
        
        # Calculate collision normal
        if collision_info['distance'] > 0:
            collision_info['normal'] = (entity2.position - entity1.position).normalize()
        else:
            collision_info['normal'] = pygame.Vector2(1, 0)
            
        return collision_info
    
    def separate_entities(self, entity1: BaseEntity, entity2: BaseEntity):
        """
        Separate two overlapping entities.
        
        Args:
            entity1: First entity to separate
            entity2: Second entity to separate
        """
        distance = entity1.position.distance_to(entity2.position)
        min_distance = entity1.radius + entity2.radius
        
        if distance < min_distance:
            if distance > 0:
                # Calculate separation vector
                separation = (entity2.position - entity1.position).normalize()
                overlap = min_distance - distance
                
                # Move entities apart
                entity1.position -= separation * (overlap / 2)
                entity2.position += separation * (overlap / 2)
            else:
                # Entities are at exact same position, separate them arbitrarily
                separation = pygame.Vector2(1, 0)  # Separate horizontally
                overlap = min_distance
                
                # Move entities apart
                entity1.position -= separation * (overlap / 2)
                entity2.position += separation * (overlap / 2) 