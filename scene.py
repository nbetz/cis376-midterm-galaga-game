"""Game scene for managing gameobjects for a game engine.

Provides basic functions of a game scene for creating games.

Typical usage example:
  game_scene = scene.Scene()
  engine.add_scene(game_scene)
"""

import game_object
import pygame
import random
import engine


class Scene:
    """Scene class providing basic info for managing a set of GameObjects in a game scene

    Intended to be extended by other classes to provide a base for creating game objects.

    Attributes:
    game_objects: list of game objects in the scene.
    groups: dictionary storing all the sprite groups and their string names.
    rand: random number generator
    user_object: GameObject of the player
    tile_size: int representing how large of a square each sprite should be.
    """
    def __init__(self, tile_size: int):
        all_sprites = pygame.sprite.Group()
        self.game_objects = []
        self.groups = {"all_sprites": all_sprites}
        self.rand = random.Random
        self.user_object: game_object.GameObject
        self.tile_size = tile_size

    def update_all_objects(self, *args, **kwargs):
        """calls update() method for all updatable game objects in scene

            Args:
                *args: A tuple of arguments to be passed to each updatable object.
                **kwargs: A dictionary of named arguments to be passed to each updatable object.
            """
        all_sprites = self.groups.get("all_sprites")
        all_sprites.update(*args, **kwargs)

    def draw(self):
        """calls pygame draw function for all objects in scene
        """
        self.groups.get("all_sprites").draw(engine.Engine.screen)

    def check_win(self) -> bool:
        """checks if win condition is met in scene.

        Returns:
            boolean representing if the win condition has been met. Defaults to always being False
        """
        return False

    def initial_grid(self, **kwargs):
        """initializes board upon being set. Only implemented in child classes.

        Args:
            **kwargs: A dictionary of named arguments to be used as initialization parameters.
        """
        pass
